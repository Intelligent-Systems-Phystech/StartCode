%Here we've made 1 layer neyron net wit 2 attribute
% neyron net was educated by hands and matlab and lust 1 itteration
% dataset from https://www.kaggle.com/neuromusic/avocado-prices

%Determine working directiryand importing data
mydir = 'C:\Program Files\MATLAB\avocado\';
fileID = [mydir,'avocado.xls'];
doc = importdata(fileID);

%Determine working data, answers - y  and two atributes - x2 and x
x = doc.textdata(2:51, 1:1);
x2 = doc.data(2:51, 4:4);
y = doc.data(2:51, 3:3);

% Convert text data of type YYYY-MM-DD in number data MM b-e every avocado
% of  2015 year
for i = 1:50
   z = cell2mat(x(i,1));
   c = strsplit(z,'-');
   x1(i,1) = str2num(cell2mat(c(1,2)));
end


% Using excel we determine 2 dependences
% as old avocado as low its price
% as big avocado as low its price
%a(x) = 1*f1(x1)*f2(x2);
%f1(x1) = 0.0185x1+0.9773
%f2(x2) = 1,539 - 5*10^-6 * x2

for i = 1:50
    f1 = 0.02*x1(i,1) + 1;
    f2 = 1.5 - x2(i,1)/200000; 
    a(i,1) = 1*f1*f2;
end

%graphics
hold on;
title('Comparison of answers and my model')
plot(y);
plot(a, 'Color', 'm');
legend('Y - Answers', 'A - my model');
hold off; 

hold on;
title('Total Difference between Y and A');
plot(y-a);
hold off;

hold on;
title('Relative Difference between Y and A');
plot(1-a/y);
hold off;
hold off;



