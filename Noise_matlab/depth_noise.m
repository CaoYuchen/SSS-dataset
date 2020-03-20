clear
clc
close all

% img = imread('.\0030.png');

noisyImg = im2double(img) * 20.0;
sigmaDisp = 0.2;
sigmaD = 1/2;
sigmaS = 1/2;
focalLength_pixel = 24/(35/2) * size(noisyImg,2);
baseline = 0.025;
disparityFactor = baseline * focalLength_pixel * 5;
depthBaseline = 0.025;
sigmaDc = 1/8;


Directory = 'D:\Learning\Blenders\room3\rgb2\';
dataFiles = dir(fullfile(Directory,'*.png'));

tic

for i = 1:numel(dataFiles)
% for i = 30:30
    dataFile = fullfile(Directory, dataFiles(i).name);
    img = imread(dataFile);
    
    % lateral depth noise
    cannyImg = edge(img, 'Canny');
    [Gmag, Gdir] = imgradient(img);

    X = (repmat([1:size(img,2)],[size(img,1),1]) - size(img,1)/2) / focalLength_pixel;
    Y = (repmat([1:size(img,1)]',[1,size(img,2)]) - size(img,2)/2) / focalLength_pixel;
    [nX,nY,nZ] = surfnorm(X,Y,noisyImg);
    % surfnorm(X,Y,noisyImg);

    crX = X;
    crY = Y;
    crZ = zeros(size(noisyImg))+0.024;

    form1 = nX .* crX + nY .* crY + nZ .* crZ;
    form2 = sqrt(nX .^2 + nY .^2 + nZ .^2);
    form3 = sqrt(crX .^2 + crY .^2 + crZ .^2);
    theta = acosd(form1./(form2.*form3));

    % noise = 0.0012 + 0.0019* (noisyImg -0.4) .^2 + 0.0001./sqrt(noisyImg) .* (theta.^2./(pi/2-theta).^2);
    % noise = (0.8 + 0.035 * theta ./ (pi/2-theta)) .* noisyImg * 1/focalLength_pixel / 0.024;
    % noise = normrnd(0,noise);

    laterImg = noisyImg;
    laterImg(theta>=95)=0;
    laterImg(cannyImg)=0;
    % laterImg = im2double(laterImg) + noise;
    laterImg = uint16(round(laterImg * 65535 / 20.0,0));
    % imshow(laterImg)

    srcPixel = laterImg(cannyImg);
    mag = normrnd(1,ones(size(Gdir))*1);
    driftX = sin(Gdir/180*pi) .* mag;
    driftY = cos(Gdir/180*pi) .* mag;

    num=floor(max(max(mag)));
    for i = 1:num  
        index = find(cannyImg == 1);
        iX = mod(index,size(img,1)) - round(driftX(index),0);
        iX = max(min(iX,ones(size(iX))*size(img,1)),ones(size(iX)));
        iY = floor(index/size(img,1)) + round(driftY(index),0);
        iY = max(min(iY,ones(size(iY))*size(img,2)),ones(size(iY)));
        index_new = iX + iY*size(img,1);
        index_new = max(min(index_new,ones(size(index_new))*size(img,2)*size(img,1)),ones(size(index_new)));
        laterImg(index_new)=srcPixel;

        mag(mag<1 & mag>-1)=0;
        mag(mag<0) = mag(mag<0)+1;
        mag(mag>0) = mag(mag>0)-1;
        driftX = sin(Gdir/180*pi) .* mag;
        driftY = cos(Gdir/180*pi) .* mag; 
    end

    % imshow(laterImg)
    laterImg = im2double(laterImg) * 20.0;

    % baseline noise
    dcImg = inf(size(img));
    disTable = dcImg;

    for r=1:size(laterImg,1)
        for c=1:size(laterImg,2)
            disparity_x = depthBaseline * focalLength_pixel / laterImg(r,c) + c;
            dis_rectified = max(1,disparity_x);
            dis_rectified2 = min(dis_rectified, size(laterImg,2));
            disparity_x = round(dis_rectified2);
            dcImg(r,disparity_x) = min(laterImg(r,c),dcImg(r,disparity_x));
        end
    end

    [ix,iy] = find(dcImg==inf);
    for i=1:size(ix,1)
        iy_low = max(iy(i)-1,1);
        iy_high = min(iy(i)+1,size(laterImg,2));
        val = abs(dcImg(ix(i),iy_low) - dcImg(ix(i),iy_high))/min(dcImg(ix(i),iy_low), dcImg(ix(i),iy_high));
        if val < 0.05
            dcImg(ix(i),iy(i)) = (dcImg(ix(i),iy_low) + dcImg(ix(i),iy_high))/2;
        end
    end

    dcImg(dcImg==inf)=0;

    % camera axis noise
    for r=1:size(noisyImg,1)
        for c=1:size(noisyImg,2)
            pixcoordinate= [c;r];
            dispDisturbance = normrnd(0,sigmaS,[2,1]);
            noisyImg(r,c) = disparityFactor / ( disparityFactor /bilinearInt(dcImg,pixcoordinate+dispDisturbance) + normrnd(0,sigmaD) + sigmaDisp);
        end
    end

    noisyImg = uint16(round(noisyImg / 20 * 65535, 0));
    % imshow(noisyImg)
    
    imwrite(noisyImg,'./depth_noise/'+dataFiles(i).name,'png');
    
    toc
end
