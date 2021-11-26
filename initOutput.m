function [dev, names, size, dInfo] = initOutput()%return channels
    %dt = daqvendorlist;
    
    info = audiodevinfo
    dq = daqlist
    dev = dq.VendorID;
    names = dq.Model;
    size = height(dq);
    dq.DeviceInfo(1)

end