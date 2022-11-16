%$Author: TRAN NGOC THUY DUNG$
clear all, close all, clc

M = 1.08; %(kg)0.5;%
m = 0.36; %(kg)7/4;%
l = 0.204; %(m)0.5;%
g = 9.81; %(m/s^2)10;%
% F = 2; % -20 <= F <= 2 (N) % F: konstante Eingangsgröß
[A,b] = Matrix_A_b(M,m,l,g);
f = [-7, -8.75, -10.5, -12.25]*0.5; 

K = place(A,b,f);

t = 0:.005:2.5;
x0 = [0;0;0.5*pi/180;0];
x_neu = [2;0;0;0];


[t,x] = ode45(@(t,x)linearisierung(x,M,m,g,l,-K*(x-x_neu)),t,x0);
F = [];
j  = 1;
for i =1:length(t)
    
    F(j) = -K*(x(i,:).'-x_neu);
    j = j+1;
end

pend_plotten(0,t,x(:,1),x(:,3),F,"ode45",f)

