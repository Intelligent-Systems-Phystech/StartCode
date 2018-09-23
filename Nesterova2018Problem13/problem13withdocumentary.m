% Problem 13
% Here we investigate documents by SVD method. We make dictionary of words.
% Create matrix of docs and words in which cells is frequency of meeting
% words in docs. Then by SVD methos we dole this matrix on U - docs and
% themes matrix and V - themes and words matrix. So we devide docs on
% themes.


mydir = 'C:\Program Files\MATLAB\problem13\'; % Working directory
fileID_1 = [mydir,'ball.txt']; % Adresses of working files
fileID_2 = [mydir,'bull.txt'];   
fileID_3 = [mydir,'rabbit.txt'];
dicID = [mydir,'dictionary.txt'];  % Your dictionary
doc_1 = importdata(fileID_1);    % Importing working files
doc_2 = importdata(fileID_2);
doc_3 = importdata(fileID_3);
word = importdata(dicID);

m = 3;  %Number of working files
n = length(word)    %Nabber of words in dictionary
mat = zeros(m,n);   %Matrix of docs and words

%Cycles which write in cells number of meeting words in docs, cycle for each doc
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
   
     % SVD-method
   [U, S, V] = svd(mat);
   % Here U - matrix of docs and themes
   % Here V - matrix of themes and words