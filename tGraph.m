function y = tGraph(fName)
    disp(fName);

    [y,Fs] = audioread(fName);
    y = y.';

    
    %info = audioinfo(fName);

    %t = 0:seconds(1/Fs):seconds(info.Duration);
    %t = t(1:end-1);
    
    %plot(t,y)
    %xlabel('Time')
    %ylabel('Audio Signal')
end