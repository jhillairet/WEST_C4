shotnr=53983

%%% Data are coming from /Imas_public/public/equilibrium_data_shift_time/west/0/
%load('data_IMAS_equi_Shot54461_Run0000_Occ0_imas_public_west_3P8P6.mat')

datapath='/Imas_public/public/equilibrium_data_shift_time/west/0/';
dataimas=['data_IMAS_equi_Shot' num2str(shotnr) '_Run0000_Occ0_imas_public_west_3P8P6.mat'];

load([datapath dataimas])

% time should be time_imas - 32
% 32 is the assumed T_IGNITRON
ti=47; % Index of the time slice

R=interp2D__r;
Z=interp2D__z;

MF.R=R(:,1)';
MF.Z=Z(1,:);

MF.MF=squeeze(interp2D__psi(ti,:,:)).';

RX=xPoint(ti,1);
ZX=xPoint(ti,2);

R0=vacuum_toroidal_field__r0;
B0=vacuum_toroidal_field__b0(ti);

MF.GEOM.B0=B0;
MF.GEOM.R0=R0;
MF.GEOM.RX=RX;
MF.GEOM.ZX=ZX;

Ip=global_quantities__ip(ti);
MF.GEOM.Ip=Ip;

MF.GEOM.WALL=wall;

filename=[num2str(shotnr),'_t7p5s.mat']
save(filename,'MF')


