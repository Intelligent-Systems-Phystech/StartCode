mydir = 'C:\Program Files\MATLAB\problem13\';
fileID_1 = [mydir,'ball.txt'];
fileID_2 = [mydir,'bull.txt'];
fileID_3 = [mydir,'rabbit.txt'];
dicID = [mydir,'dictionary.txt'];
doc_1 = importdata(fileID_1);
doc_2 = importdata(fileID_2);
doc_3 = importdata(fileID_3);
word = importdata(dicID);

m = 3;
n = length(word);
mat = zeros(m,n);

   for j =1:4
    for i=1:n
        k = findstr(doc_1{j,1}, word{i,1});
        x = isempty(k);
        y = 1 - x;
        z = mat(1,i);
        mat(1,i) = z + y;
    end
   end
   
    for j =1:4
    for i=1:n
        k = findstr(doc_2{j,1}, word{i,1});
        x = isempty(k);
        y = 1 - x;
        z = mat(2,i);
        mat(2,i) = z + y;
    end
    end
   
     for j =1:4
    for i=1:n
        k = findstr(doc_3{j,1}, word{i,1});
        x = isempty(k);
        y = 1 - x;
        z = mat(3,i);
        mat(3,i) = z + y;
    end
     end
   
   [U, S, V] = svd(mat);