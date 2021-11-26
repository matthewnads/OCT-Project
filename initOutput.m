function [names, dirdaq, channels] = initOutput()%return channels
    %dt = daqvendorlist;
    
    dirdaq = daq("directsound");
    dirni = daq("ni");
    info = audiodevinfo;
    dq = daqlist;
    dev = dq.VendorID;
    model = dq.Model;
    size = height(dq);

    io = [];
    idx = length(io);

    for i = 1:size
        if contains(dev(i), "directsound") == 1
            if contains(model(i), "Speaker") == 1 || contains(model(i), "Headphones") == 1
                [io, idx] = addoutput(dirdaq, dq.DeviceID(i), 1:2, "Audio");
                names(idx) = dq.Model(i);
            end
            if contains(model(i), "Microphone") == 1
                [io, idx] = addinput(dirdaq, dq.DeviceID(i), 1:2, "Audio");
                names(idx) = dq.Model(i);
            end
            idx = idx + 1;
        end
    end
    
    names = rot90(names);
    channels = dirdaq.Channels;

 end