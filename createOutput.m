function [output] = createOutput(type, fs, amp, tsil, tramp, StopTime, dtcycle, sine_F, f0, f1) 
    % seconds StopTime

    %main params: type, sampling frequency (khz), amp (v), tsilence (ms),
    %t-ramp (ms), offset (0 default, in volts)
    %optional args: duty cycle, f0, f1 (chirp), sine 

    if ~exist('offset','var')
        offset = 0;
    end
    if ~exist('amp','var')
        amp = 1;
    end

    switch type
        case 0 %pulse
           if ~exist('dtcycle','var')
                dtcycle = 50;
           end
           if ~exist('dtcycle','var')
                dtcycle = 50;
           end
           dt = 1/fs;
       
           t = (0:dt:StopTime-dt)'; 
           output = pulstran(t,offset,x);
        case 1 %noise
            lb = -(amp/2) + offset; %change
            ub = (amp/2) + offset; % 
            samp = fs*StopTime;
            output = lb + rand(1,samp)*(ub - lb);
            output = rot90(output);
        case 2 %chirp
            if ~exist('f0','var')
                f0 = 1000;
            end
            if ~exist('f1','var')
                f1 = 20000;
            end

            dt = 1/fs;                   % seconds per sample
            t = (0:dt:StopTime-dt)'; 
            x = chirp(t,f0,t(end),f1);
            output = x,fs;
        case 3 %sine
            if ~exist('sine_F','var')
                sine_F = 5000;
            end 
            dt = 1/fs;                   % seconds per sample
            t = (0:dt:StopTime-dt)';     % seconds
            F = sine_F;                    % Sine wave frequency (hertz)
            output = sin(2*pi*F*t);
        
        case 4 %periodic/square
            
    end

    %define envelope

    rat = tramp/StopTime;
    silp = tsil/StopTime;

    sil_rep = ceil(length(output)*silp);
    ramp_rep = ceil(length(output)*rat);

    rep_sz = length(output) - 2*ramp_rep - 2*sil_rep;

    ramp = 0: 1/(ramp_rep) : 1 - (1/ramp_rep);

    env=[];
    temp(1:sil_rep) = zeros(sil_rep,1);
    firstramp = sil_rep+length(ramp);
    temp(sil_rep+1:firstramp) = ramp;
    signal_sz = firstramp + rep_sz;
    temp(firstramp+1:signal_sz) = ones(rep_sz,1);
    lastramp = signal_sz + length(ramp);
    temp(signal_sz+1:lastramp) = flip(ramp);
    temp(lastramp+1:length(output)) = zeros(sil_rep,1);

    temp = rot90(temp);
    env = vertcat(env,temp);   
             
    output=output.*env + offset;

end