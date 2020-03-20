clc
clear
close all

% files = ['./rgb1.png','./rgb2.png','./rgb3.png','./rgb4.png','./rgb5.png','./rgb6.png','./rgb7.png','./rgb8.png','./rgb9.png'];
% EV = [0, 1, 2, 3, -1, -2, -3, -4, 4];
% files = ['./room3/rgb1.png','./room3/rgb2.png','./room3/rgb3.png','./room3/rgb4.png','./room3/rgb5.png','./room3/rgb6.png','./room3/rgb7.png','./room3/rgb8.png','./room3/rgb9.png','./room3/rgb10.png','./room3/rgb11.png'];
% EV = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5];
files = ['./room3.1/rgb1.png','./room3.1/rgb2.png','./room3.1/rgb3.png','./room3.1/rgb4.png','./room3.1/rgb5.png','./room3.1/rgb6.png','./room3.1/rgb7.png','./room3.1/rgb8.png','./room3.1/rgb9.png','./room3.1/rgb10.png','./room3.1/rgb11.png','./room3.1/rgb12.png','./room3.1/rgb13.png','./room3.1/rgb14.png','./room3.1/rgb15.png'];
% files = ['./room4/rgb1.png','./room4/rgb2.png','./room4/rgb3.png','./room4/rgb4.png','./room4/rgb5.png','./room4/rgb6.png','./room4/rgb7.png','./room4/rgb8.png','./room4/rgb9.png','./room4/rgb10.png','./room4/rgb11.png','./room4/rgb12.png','./room4/rgb13.png','./room4/rgb14.png','./room4/rgb15.png'];
EV = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5, -6, -7, -8, -9];

ISO = 640;
Aperture = 11.0;

shutterTime = 100 * Aperture^2 ./ (ISO * 2.^(9.67-EV));
crfunction = camresponse(files,'ExposureTimes',shutterTime);

save('./crf.mat','crfunction');

range = 0:length(crfunction)-1;
figure,
hold on
plot(crfunction(:,1),range,'--r','LineWidth',2);
plot(crfunction(:,2),range,'-.g','LineWidth',2);
plot(crfunction(:,3),range,'-.b','LineWidth',2);
xlabel('Log-Exposure');
ylabel('Image Intensity');
title('Camera Response Function');
grid on
axis('tight')
legend('R-component','G-component','B-component','Location','southeast')

set (gcf,'Position',[0,0,1024,768]);