%$Author: TRAN NGOC THUY DUNG$
close all
clear all
clc
%Kontant varable
M = 1.08; %(kg)
m = 0.36; %(kg)
l = 0.204; %(m)
g = 9.81; %(m/s^2)
F = 0.05; % -20 <= F <= 20 (N) % F: konstante Eingangsgröße

% initialisierung 
x0 = [0; 0; 0; 0];
t0 = 1;
[A,b] = Matrix_A_b(M,m,l,g);

schritt = 0.01;
beg = 0;
ende = 2;
time = linspace(beg,ende,(ende-beg)/schritt);
position = [];
winkel = [];
j=1;
T = @(t)0;

for t = time
    if t < t0
        x_t = [0; 0; 0; 0];
    else
     x_t=DGL_loeser(x0,t0,t,A,b,F,zeros(4,1), T);
    end
    position(j) = x_t(1);
    winkel(j) = x_t(3)*180/pi; % von Bogenmaß zum Gradmaß umrechnen
    j=j+1;
end

time = reshape(time,[],1);
position = reshape(position,[],1);
winkel = reshape(winkel,[],1);
T = table(time, position, winkel);
T.Properties.VariableNames ={'time','position', 'winkel'};
%disp(T)

% PLOT POSITION UND WINKEL VON INHOMOGENE DGL MIT F KONSTANT
f=figure;
f.Position = [200 100 850 240];

subplot(1,2,1)
plot(time,position,'LineWidth',1.1)
xline(t0,'r')
title("x(t) mit F0 = "+F+"(N) und t0 = "+t0+"(s)")
legend('x(t)','Stosszeit')
xlabel('t (Sekunde)')
ylabel('x (m)')
grid on

subplot(1,2,2)
plot(time,winkel,'LineWidth',1.1)
xline(t0,'r')
title("{\alpha}(t) mit F0 = "+F+"(N) und t0 = "+t0+"(s)")
legend('{\alpha}(t) ({\circ})','Stosszeit')
xlabel('t (Sekunde)')
ylabel('{\alpha} ({\circ})')
grid on
saveas(f,'mit_Kontante_F.png')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% VORGEGEBENE EIGENWERTE (Geschwindigkeit)
% f = [-7, -8.75, -10.5, -12.25]*0.5; %passt mit alle Fälle
% f = [-7, -8.75, -10.5, -12.25]; % passt mit Stabilizierung ohne Positionsänderung
% f = [-22, -27.5, -33, -38.5]*6; % passt nur mit Stabilizierung ohne
% Positionänderung und ohne Moment
% f = [-7, -8.75, -10.5, -12.25]*0.01; % schlecht mit allem
f = [-7, -8.75, -10.5, -12.25]*0.1; %passt mit alle Fälle

% VORGEGEBEN INITIALISIERUNG 
t0 = 2; %(s)
delta_t = 0.005; %(s)
x0 = [0;0;0.5*pi/180;0]; % Eingangswinkel in Bogenmaß 

k = 1;

% Sollposition
x_neu = [2;0;0;0];


sollpos2 = [];
sollwinkel2 = [];
kraft2 = [];

beg = 0;
ende = 15;
n = (ende-beg)/delta_t;
time = linspace(beg,ende,n);

% REGLER K
K = place(A,b,f);
A_stricht = A -b*K;

%Moment T
c = [0; 3/(l*(4*M+m)); 0; 3*(M+m)/((l^2)*m*(4*M+m))];

Amp = 0.01;
% t_imp = 0.5;
t_imp = 3;
impact = 0.1;

T= @(t) 1/((pi^(1/2))*Amp) *exp(-((t-t_imp)^2)/(Amp^2)) *impact; 
DD = @(t)0;
for t = time
    
%      T = DD(t);

    if t <= t0
       x_t = [0;0;0;0];
       x_t2 = [0;0;0;0];
       x_t3 = [0;0;0;0];
       x_t4 = [0;0;0;0];
       
       
       F_t = 0;
       F_t2 = 0;
       F_t3 = 0;
       F_t4 = 0;
       
    elseif t == t0+delta_t
        x_t = x0;
        F_t = K*(-x_t);
        
        x_t2 = x0;
        F_t2 = -K*(x_t2-x_neu);
        
        x_t3 = x0;
        F_t3 = -K*(x_t3);
        
        
        x_t4 = x0;
        F_t4 = -K*(x_t4-x_neu);
        
    else
        x_t = DGL_loeser(x0,t0,t,A_stricht,b,0,zeros(4,1),DD); % x'=A'x+0
        F_t=K*(-x_t);
        
        x_t2 = DGL_loeser(x0,t0,t,A_stricht,b,K*x_neu,zeros(4,1),DD);% x'=Ax + b*(-K*(x-xneu)=A'x+b*K*xneu
        F_t2=-K*(x_t2-x_neu);
        
        x_t3 = DGL_loeser(x0,t0,t,A_stricht,zeros(4,1),0,c, T );% x'=Ax + b*(-K*(x-xneu)=A'x+b*K*xneu
        F_t3=-K*(x_t3);
        
        x_t4 = DGL_loeser(x0,t0,t,A_stricht,b,K*x_neu,c,T );% x'=Ax + b*(-K*(x-xneu)=A'x+b*K*xneu
        F_t4=-K*(x_t4-x_neu);
        
    end
    sollpos(k) = x_t(1);
    sollwinkel(k) = x_t(3); 
    kraft(k) = F_t;
    
    sollpos2(k) = x_t2(1);
    sollwinkel2(k) = x_t2(3); 
    kraft2(k) = F_t2;
    
    sollpos3(k) = x_t3(1);
    sollwinkel3(k) = x_t3(3); 
    kraft3(k) = F_t3;
    
    sollpos4(k) = x_t4(1);
    sollwinkel4(k) = x_t4(3); 
    kraft4(k) = F_t4;
    
    k = k+1;
    
    
end
pend_plotten(t0,time,sollpos,sollwinkel,kraft,"Stabilizierung_ohne_Moment",f)

pend_plotten(t0,time,sollpos2,sollwinkel2,kraft2,"Positionsveraenderung_ohne_Moment",f)

pend_plotten(t0,time,sollpos3,sollwinkel3,kraft3,"Stabilizierung_mit_Moment",f)

pend_plotten(t0,time,sollpos4,sollwinkel4,kraft4,"Positionsveraenderung_mit_Moment",f)



%%% Der Kraft und die Geschwindigkeit hängt von die Eigenwerte ab

