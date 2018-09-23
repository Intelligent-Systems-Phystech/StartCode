% Problem 13
% Here we investigate documents by SVD method. We make dictionary of words.
% Create matrix of docs and words in which cells is frequency of meeting
% words in docs. Then by SVD methos we dole this matrix on U - docs and
% themes matrix and V - themes and words matrix.(???????) So we devide docs on
% themes. Then we investigate our method on errors.


mydir = 'C:\Program Files\MATLAB\problem13\'; % Working directory
fileID_1 = [mydir,'ball.txt']; % Adresses of working files
fileID_2 = [mydir,'bull.txt'];   
fileID_3 = [mydir,'rabbit.txt'];
dicID = [mydir,'dictionary.txt'];  % Your dictionary
doc_1 = importdata(fileID_1);    % Importing working files
doc_2 = importdata(fileID_2);
doc_3 = importdata(fileID_3);
word = importdata(dicID);

l = 3;  %Number of working files
n = length(word)    %Nabber of words in dictionary
M = zeros(l,n);   %Matrix of docs and words

%Cycles which write in cells number of meeting words in docs, cycle for each doc
   for j =1:4
        for i=1:n
            k = findstr(doc_1{j,1}, word{i,1});
            x = isempty(k);
            y = 1 - x;
            z = M(1,i);
            M(1,i) = z + y;
       end
   end
   
    for j =1:4
        for i=1:n
            k = findstr(doc_2{j,1}, word{i,1});
            x = isempty(k);
            y = 1 - x;
            z = M(2,i);
            M(2,i) = z + y;
        end
    end
   
    for j =1:4
        for i=1:n
            k = findstr(doc_3{j,1}, word{i,1});
            x = isempty(k);
            y = 1 - x;
            z = M(3,i);
            M(3,i) = z + y;
        end
     end
   
   % SVD-method
   [U, S, V] = svd(M);
   % Here U - matrix of docs and themes???
   % Here V - matrix of themes and words???
   
   
   % Here starts error research
   normM = norm(M,inf);
   erU = zeros(1,l);
   erS = zeros(1,l);
   erV = zeros(1,9);
    
   % Error research on matrix U
 
   U1 = U;
   U1(1,1) = 0;
   EM = U1*S*V;
   normEM = norm(EM,inf); 
   erU(1,1) = normM - normEM;
    
   U1 = U;
   U1(2,3) = 0;
   EM = U1*S*V;
   normEM = norm(EM,inf);
   erU(1,2) = normM - normEM;
    
   U1 = U;
   U1(3,2) = 0;
   EM = U1*S*V;
   normEM = norm(EM,inf);
   erU(1,3) = normM - normEM;
    
   %Error research on matrix S
 
    for i=1:l 
        S1 = S;
        S1(i,i) = 0;
        EM = U*S1*V;
        normEM = norm(EM,inf); 
        erS(1,i) = normM - normEM;
    end
    
    % Error researh on matrix V
    
    % as nonzeroes values have no regularities 
    % for better research you can create function to recognize witch of
    % cells nonzeros and make error research on each nonzeroes cell
    % more simple way if matrix is not big make by hands matrix of places
    % of nonzeroes cells and investigate
    % and the simplest  also if matrix isn't bigis that
    % I analysed places of non zeroes cells
    % and found out that from 4 to 12 every diagonal cell nonzero
    % i will investigate them
    
    for i = 4:12
        V1 = V;
        V1(i,i) = 0;
        EM = U*S*V1;
        normEM = norm(EM,inf); 
        erV(1,i - 3) = normM - normEM;
    end
    
    % So we analaysed how changes 2-norm (spectr-norm)
    % of the main matrix M if we skip one cell in any of matrix U, S, V
    % as the result we obtain
    % for matrix U: 1.0353 0 0
    % for matrix S: 1.0353 0 0 
    % for matrix V: 0 0 0 0 0 0 0 0 0
    % against normM = 2.4495
    % i.e among 15 experiments we have 13 with 0 - error and 2 with
    % approximately 43% of error
    % avarage error is about 6%
    
    %you also can investigate it with anothe norm
    
    % if we investigate 1-norm of matrix we will obtain
    % for matrix U: 0.5858 0 0
    % for matrix S: 0.5858 0 0 
    % for matrix V: 0 0 0 0 0 0 0 0 0
    % against normM = 2
    % i.e among 15 experiments we have 13 with 0 - error and 2 with
    % approximately 29% of error
    % avarage error is about 4%
    
     % if we investigate inf-norm of matrix we will obtain
    % for matrix U: 2.5858 0 0
    % for matrix S: 2.5858 0 0 
    % for matrix V: 0 0 0 0 0 0 0 0 0
    % against normM = 4
    % i.e among 15 experiments we have 13 with 0 - error and 2 with
    % approximately 65% of error
    % avarage error is about 9%
    
    %now we will do graphs
    %but in another file