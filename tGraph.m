function [y,Fs,tt] = tGraph(fName)

    [y,Fs] = audioread(fName);
    
    info = audioinfo(fName);

    tt = info.Duration;

    t = 0:seconds(1/Fs):seconds(info.Duration);
    t = t(1:end-1);

    t = 0 : 1/1e6 : .01;         
    d = 0 : 1/5 : .01           
    y = pulstran(t,d,@rectpuls);
    plot(t,y); 
    axis([0 0.001 0 1.5])
    
    %plot(t,y)
    %xlabel('Time')
    %ylabel('Audio Signal')
end