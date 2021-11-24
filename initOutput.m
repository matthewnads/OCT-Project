function [dev, names, size, dInfo] = initOutput()%return channels
    %dt = daqvendorlist;
    
    info = audiodevinfo;
    dq = daqlist
    dev = dq.VendorID;
    names = dq.Model;
    size = height(dq);
    name = audiodevinfo(1) 

end