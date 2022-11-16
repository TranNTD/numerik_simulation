function dx = linearisierung(x, M, m, g, l, F)
%$Author: TRAN NGOC THUY DUNG$
a = 4*M+m;
b = (3*m*g)/a;
c = 3*g*(M+m)/(l*a);


dx(1,1) = x(2);
dx(2,1) = b*x(3)+(4/a)*F;
dx(3,1) = x(4);
dx(4,1) = c*x(3)+(3/(l*a))*F;
