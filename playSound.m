function playSound(channel) %select channel
    %select channel number(s)
    % - 
    %select which waveform for each type
    %output to daq board

    %d = daq("ni"); %data acquisition object for NI-USB 6363
    %d = daq("directsound"); %Windows sound

    Fs = 44000;

    signal = createOutput(2, Fs, 1);
    [names, dq, channels, devID, defMode] = initOutput(Fs);

    %addinput(dirdaq, devID, channels(1), defMode)
    %addoutput(dirdaq, devID, channels(1), defMode)
    %addoutput(dq, devID, channels(channel), defMode);
    
    %start(dq,"RepeatOutput")%repeat output
    

    dq.NumDigitalTriggersPerRun = 1;
    dq.DigitalTriggerTimeout = 60;

    %addinput(dq, devID, channels(1), defMode)
    addoutput(dq, devID, channels(1), defMode)

    trig = addtrigger(dq, "Digital", "StartTrigger", "External", strcat(devID,"/PFI0"));

    write(dq, signal)
    %pause(1)
    %stop(dq)

    %channels.Type
    %add channels    

end