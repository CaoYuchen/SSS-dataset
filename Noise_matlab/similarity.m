clc
clear

crf = load('./crf2.mat').crfunction;
img = imread("./imgCF.png");
ref = imread("./rawCF.png");
rawImg = revertCrf(img,crf);
rawImg = uint8(round(rawImg * 0.3854 * 255,0));
imshow(rawImg)

s = ssim(rawImg,ref)
i = immse(rawImg,ref)
p = psnr(rawImg,ref)