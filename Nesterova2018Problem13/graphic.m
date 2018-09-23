erS1 = [0.5858, 0, 0];
erS2 = [1.0353, 0, 0];
erSinf = [2.5858, 0, 0];
erU1= [0.5858, 0, 0];
erU2= [1.0353, 0, 0];
erUinf = [2.5858, 0, 0];
erV1 = [0, 0, 0, 0, 0, 0, 0, 0, 0];
erV2 = [0, 0, 0, 0, 0, 0, 0, 0, 0];
erVinf = [0, 0, 0, 0, 0, 0, 0, 0, 0];
normM1=2;
normM2=2.4495;
normMinf=4;
er1 = [0.5858, 0, 0, 0.5858, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
er2 = [1.0353, 0, 0, 1.0353, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
erinf = [2.5858, 0, 0, 2.5858, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
x =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];

for i=1:15
    er1(1,i) = er1(1,i)/normM1;
end

for i=1:15
    er2(1,i) = er2(1,i)/normM2;
end

for i=1:15
    erinf(1,i) = erinf(1,i)/normMinf;
end

hold on;
grid minor;
title('Errors of missing 1 cell for 3 kind of norms');
stem(x, erinf,'LineWidth', 5, 'Color', 'g', 'Marker', 'none');
stem(x, er2,'LineWidth', 5, 'Color', 'm', 'Marker', 'none');
stem(x, er1,'LineWidth', 5, 'Marker', 'none');
legend('Infinite Norm', 'Second Norm', 'First Norm');
hold off;
