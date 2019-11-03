%You may write any matlab code here to control your sim
clear all;
cla;
rootpath='/tools/projects/kosta/TheSDK/Simulations/f2_adc_test'
picpath=[rootpath '/Pics'];
matpath=[rootpath '/Matlab/Matfiles'];
addpath(genpath('/tools/projects/kosta/TheSDK'))
if (~isempty(mfilename))
    statusfile=[ rootpath '/Matlab/' mfilename '.status' ];
    delete(statusfile)
end
%Just to test if these run in parallel.
parfor i=1:2
    s(i)=inv_sim;
    s(i).models= { 'matlab' 'vhdl' 'sv' 'sv' 'vhdl' 'matlab' }
    s(i).init;
    s(i).printpath=picpath;
    s(i).run_simple;
end
%plot only the results of the first one
s(1).plot;
s(1).print;

if (~isempty(mfilename))
    fprintf(1,'Printing statusfile %s\n', statusfile);
    fid=fopen(statusfile,'w');
    fprintf(fid, 'Succesfully executed %s.m on %s.\n' , mfilename, datestr(now));
end

