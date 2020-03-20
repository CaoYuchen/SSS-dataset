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