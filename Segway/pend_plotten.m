function pend_plotten(t0,time,x,w,F, FigureName,f)
%$Author: TRAN NGOC THUY DUNG$
theta = w*180/pi; % Bogenmaß in Grad

time = reshape(time,[],1);
position = reshape(x,[],1);
winkel = reshape(theta,[],1);
kraft = reshape(F,[],1);
 

list = [position,winkel,kraft];
name = ["Position","Winkel ","Kraft"];
label_y = ["x (m)","{\alpha}({\circ})","F (N)"];
fig = figure;
fig.Position = [200 30 700 500];

for i = 1:length(name)
    subplot(length(name),1,i)
    plot(time,list(:,i),'LineWidth',1.1)
    xline(t0,'r')
    title(name{i})
    xlabel('t (Sekunde)')
    ylabel(label_y{i})
    legend(label_y{i},"Stoerung")
    grid on
    hold off
    
end
set(gcf, 'Name', FigureName)
sgtitle(sprintf("f=[%.2f;%.2f;%.2f;%.2f] und x0 = [0;0;0.5*pi/180;0]",f(1),f(2),f(3),f(4)))
% saveas(fig,FigureName+'.png')
