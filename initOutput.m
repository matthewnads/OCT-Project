function [names, dirdaq, channels, devID, defMode] = initOutput(samp_Rate)%dirni
    %dt = daqvendorlist;
    
    %dirdaq = daq("directsound");
    dirdaq = daq("ni");

    %dq = daqlist("directsound");
    dq = daqlist("ni");

    names = dq.Model;
    %size = height(dq);

    %devID = dq.DeviceID(5);
    devID = dq.DeviceID(1);

    %devInfo = dq.DeviceInfo(5);
    devInfo = dq.DeviceInfo(1);

    %channels = devInfo.Subsystems.ChannelNames
    channels = devInfo.Subsystems(2).ChannelNames;
    defMode = devInfo.Subsystems.DefaultMeasurementType;

    dirdaq.Rate = samp_Rate;
    

    %dq.DeviceInfo.Subsystems

    %io = [];
    %idx = length(io);

    %for i = 1:size
    %    if contains(dev(i), "directsound") == 1
    %        if contains(model(i), "Speaker") == 1 || contains(model(i), "Headphones") == 1
    %            [io, idx] = addoutput(dirdaq, dq.DeviceID(i), 1:2, "Audio");
    %            names(idx) = dq.Model(i);
    %        end
    %        if contains(model(i), "Microphone") == 1
    %            [io, idx] = addinput(dirdaq, dq.DeviceID(i), 1:2, "Audio");
    %            names(idx) = dq.Model(i);
    %        end
    %        idx = idx + 1;
    %    end
    %end
    
    %names = rot90(names);
    %channels = dirdaq.Channels;

 end