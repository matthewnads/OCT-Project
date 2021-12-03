function playSound(channel) %select channel
    %select channel number(s)
    % - 
    %select which waveform for each type
    %output to daq board

    %d = daq("ni"); %data acquisition object for NI-USB 6363
    %d = daq("directsound"); %Windows sound

    Fs = 44000;

    signal = createOutput(0, Fs);
    [names, dq, channels, devID, defMode] = initOutput(Fs);

    %addinput(dirdaq, devID, channels(1), defMode)
    %addoutput(dirdaq, devID, channels(1), defMode)
    addoutput(dq, devID, channels(channel), defMode);
    
    %start(dq,"RepeatOutput")%repeat output
    

    write(dq, signal)
    %pause(1)
    %stop(dq)

    %channels.Type
    %add channels    


    
    %

end