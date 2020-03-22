clc
clear
close all

% parameters setting
crf = load('./crf.mat').crfunction;
EV = 0;
fps = 30;
ISO = 640;
Aperture = 11.0;
shutterTime = 100 * Aperture^2 ./ (ISO * 2.^(9.67-EV));
orign_shutterTime = 100 * Aperture^2 ./ (ISO * 2.^(9.67-0));
num = max(round(fps*shutterTime),1);
sigmaS = 1/20;
sigmaC = 1/50;
sigmaQ = 1/2;
alpha = shutterTime/orign_shutterTime;

% varies for different scene
rectifyFactor = 0.3854;
D1 = "D:\Learning\Blenders\room_combined\";
D2 = "rgb2\";
Directory = D1+D2;
dataFiles = dir(fullfile(Directory,'*.png'));

tic
for i = 1:numel(dataFiles)
% for i = 30:30
    dataFile = fullfile(Directory, dataFiles(i).name);
    img = imread(dataFile);
    noisyImg = revertCrf(img,crf);
    for j = 1:num-1
        dataFile = fullfile(Directory, dataFiles(i+j).name);
        img = imread(dataFile);
        noisyImg = noisyImg +  revertCrf(img,crf);        
    end
    noisyImg = alpha*noisyImg/num + normrnd(0,sigmaS * sqrt(alpha*noisyImg/num)) + normrnd(0,sigmaC);
    imgNew = crfGo(noisyImg,crf);  
%     imshow(imgNew)
    imwrite(imgNew, D1 + "rgb_noise\"+dataFiles(i).name,"png");
    
    toc
end


function rawImg = revertCrf(img, crfunction)
    rawImg = zeros(size(img));
    img = img + 1;
    arrayNumber = [numel(img(:,:,1)),1];
    imgR = reshape(img(:,:,1),arrayNumber);
    imgG = reshape(img(:,:,2),arrayNumber);
    imgB = reshape(img(:,:,3),arrayNumber);

    indexR = sub2ind([size(crfunction),1],imgR);
    indexG = sub2ind([size(crfunction),1],imgG);
    indexB = sub2ind([size(crfunction),1],imgB);

    rawImg(:,:,1) = reshape(crfunction(indexR),size(img,[1 2]));
    rawImg(:,:,2) = reshape(crfunction(indexG),size(img,[1 2]));
    rawImg(:,:,3) = reshape(crfunction(indexB),size(img,[1 2]));
    rawImg = 2 .^ rawImg / 1.966;
end

function imgNew = crfGo(img,ref)
    img = log(img * 1.966);
    imgNew = zeros(size(img));
    for r = 1:size(img,1)
        for c = 1:size(img,2)
            for n = 1:size(img,3)
                [~, index] = min(abs(ref(:,n)-img(r,c,n)),[],'all','linear');
                imgNew(r,c,n) = index - 1;
            end
        end
    end
    imgNew = uint8(imgNew);
end