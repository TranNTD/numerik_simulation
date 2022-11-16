function [A,b] = Matrix_A_b(M,m,l,g)
%$Author: TRAN NGOC THUY DUNG$
A = [0 1 0 0;
    0 0 (3*m*g)/(4*M+m) 0;
    0 0 0 1;
    0 0 (3*g*(M+m))/(l*(4*M+m)) 0];
b = [0; 4/(4*M+m); 0; 3/(l*(4*M+m))];