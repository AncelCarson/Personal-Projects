clear all;
clc;

FID = fopen('nameList.txt','r+')
[data] = textscan(FID,'%s')
[rows,cols] = size(data{1})
for r = 1:rows

end
