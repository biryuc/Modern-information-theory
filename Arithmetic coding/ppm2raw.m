% clc;
% clear all;
% 
% fnamein = 'airplane80 (1).ppm';
% fnameout = 'airplane80.raw';
% 
% fID = fopen(fnamein,'rb');
% X = fread(fID,'uint8');
% size(X)
% fclose(fID);
% 
% X(1:16)=[];
% 
% fID = fopen(fnameout,'wb');
% fwrite(fID,X,'uint8');
% fclose(fID);

y = []
btf = 0
y = [ y 0 ones(1,btf)]
