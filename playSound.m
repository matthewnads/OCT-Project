function playSound(fName) %select channel using bit numbers?
    %select channel number(s)
    % - 
    %select which waveform for each type
    %output to daq board

    %d = daq("ni"); %data acquisition object for NI-USB 6363
    %d = daq("directsound"); %Windows sound

    [dev, names, devInfo] = initOutput()
    
    %addoutput(d, "Audio5", "1", "Audio")% add channels

    %add channels

    
    
    [y,Fs] = audioread(fName);
    
end