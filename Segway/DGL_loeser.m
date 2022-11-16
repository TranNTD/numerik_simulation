function x_lsg = DGL_loeser(x0,t0,t,A,b,F,c,T) 
%$Author: TRAN NGOC THUY DUNG$
%%% Es geht nur für eine diagonalisierbare Matrix(n x n) (n verschiedene Eigenwerte)

[V,W] = eig(A); % V: Eigenvektoren Matrix, W: Eigenwerte Matrix

vektor_1 = transpose(V(:,1));
vektor_2 = transpose(V(:,2));
vektor_3 = transpose(V(:,3));
vektor_4 = transpose(V(:,4));

EW_1 = W(1,1);
EW_2 = W(2,2);
EW_3 = W(3,3);
EW_4 = W(4,4);

if rank(W) == rank(A)
    x_h = @(t) transpose([vektor_1*exp(EW_1*t); vektor_2*exp(EW_2*t); vektor_3*exp(EW_3*t); vektor_4*exp(EW_4*t)]);
else
    w = [ 1 1 0 0];
    x_h = @(t) transpose([vektor_1*exp(EW_1*t); (t*vektor_2 + w)*exp(EW_2*t); vektor_3*exp(EW_3*t); vektor_4*exp(EW_4*t)]);
end
e_tA = @(t,t0) x_h(t)/x_h(t0); % =e^((t-t0)*A)
e_sA = @(s) x_h(-s)/(x_h(0));  % =e^(-s*A)
e_sA2 = @(s) (x_h(-s)/(x_h(0)))*c.*T(s);
Integr = @(t,t0)integral(e_sA, t0, t,'ArrayValued',true); %integral von t0 bis t
Integr2 = @(t,t0)integral(e_sA2, t0, t,'ArrayValued',true); %integral von t0 bis t
x_lsg = e_tA(t,t0)*x0 + e_tA(t,0)*Integr(t,t0)*b.*F+ e_tA(t,0)*Integr2(t,t0); % falls F=0: homogene Lösung
