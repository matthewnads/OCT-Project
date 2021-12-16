function playSound(Fs, signal) %select channel
%    params - Fs - sampling frequency, data
%    optional params - channel

    %d = daq("ni"); %data acquisition object for NI-USB 6363
    %d = daq("directsound"); %Windows sound

    if (size(signal, 2) > 1) %ensures that signal array is correct in dim
        signal = rot90(signal);
    end

    [names, dq, channels, devID, defMode] = initOutput(Fs);

    %addinput(dirdaq, devID, channels(1), defMode) % add outputs
    %addoutput(dirdaq, devID, channels(1), defMode)
    %addoutput(dq, devID, channels(channel), defMode);
    
    %start(dq,"RepeatOutput")%repeat output
    

    %dq.NumDigitalTriggersPerRun = 1; %specifies number of triggers to
    %watch for
    %dq.DigitalTriggerTimeout = 60; %time out

    %addinput(dq, devID, channels(1), defMode)
    addoutput(dq, devID, channels(1), defMode)
%     addoutput(dq, devID, channels(2), defMode)


    %trig = addtrigger(dq, "Digital", "StartTrigger", "External", strcat(devID,"/PFI0"));
    %adds trigger

    write(dq, signal) %writes signal
    %pause(1)
    %stop(dq) 

end