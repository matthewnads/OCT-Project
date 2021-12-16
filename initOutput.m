% this function initializes output devices.

function [names, dirdaq, channels, devID, defMode] = initOutput(samp_Rate)%dirni
    %dt = daqvendorlist;
    
%     dirdaq = daq("directsound");
    dirdaq = daq("ni");

%     dq = daqlist("directsound");
    dq = daqlist("ni");

    names = dq.Model;
    %size = height(dq);

%     devID = dq.DeviceID(5);
    devID = dq.DeviceID(1);

%      devInfo = dq.DeviceInfo(5);
    devInfo = dq.DeviceInfo(1);

%     channels = devInfo.Subsystems.ChannelNames;
    channels = devInfo.Subsystems(2).ChannelNames;
    defMode = devInfo.Subsystems.DefaultMeasurementType;

    dirdaq.Rate = samp_Rate;
    

    %dq.DeviceInfo.Subsystems

 end