function [y,Fs,tt] = tGraph(fName)

    [y,Fs] = audioread(fName);
    
    info = audioinfo(fName);

    tt = info.Duration;

    t = 0:seconds(1/Fs):seconds(info.Duration);
    t = t(1:end-1);
    
    %plot(t,y)
    %xlabel('Time')
    %ylabel('Audio Signal')
end