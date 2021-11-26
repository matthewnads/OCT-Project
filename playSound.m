function playSound(fName, name, channel) %select channel using bit numbers?
    %select channel number(s)
    % - 
    %select which waveform for each type
    %output to daq board

    %d = daq("ni"); %data acquisition object for NI-USB 6363
    %d = daq("directsound"); %Windows sound

    [names, dq, channels] = initOutput()
    
    %addoutput(d, "Audio5", "1", "Audio")% add channels
    %channels.Type
    %add channels    
    
    %[y,Fs] = audioread(fName);

    %[road,fs]=audioread(fName);
    %pad=zeros(length(road),1);     % blank channel
    %left=[road(:,1),pad];       % add blank channel so right is silent
    %right=[pad,road(:,1)];     % add blank channel so left is silent
    %soundsc(left,fs)       % sound only from left
    %soundsc(right,fs)    % sound only from right
end