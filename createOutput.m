% function [output] = createOutput(type, fs, amp, tsil, tramp, offset, StopTime, period, sine_F, f0, f1, square_F)
function [output] = createOutput(type, fs, amp, tsil, tramp, offset, varargin)

    % seconds StopTime

    %main params: type, sampling frequency (khz), amp (v), tsilence (ms),
    %t-ramp (ms), offset (0 default, in volts), stop time (s)
    %optional args: duty cycle, period, f0, f1 (chirp), sine 
    
    if ~exist('offset','var')%default values if unpopulated
        offset = 0;
    end
    if ~exist('amp','var')
        amp = 1;
    end
    if ~exist('StopTime', 'var')
        StopTime = 1;
    end

    tramp = tramp/1000;
    tsil = tsil/1000;

    dt = 1/fs;                   % seconds per sample
    t = (0:dt:StopTime-dt)';

    switch type
        case 0 %pulse
           if ~exist('dtcycle','var')
                dtcycle = 0.5;
           end
           if ~exist('period','var')
                period = StopTime/10;
           end
           pulses = ceil(StopTime/period);
        
           pulsewidth = period*dtcycle;
           pulseperiods = [0: pulses]*period;
        
           output = pulstran(t,pulseperiods,@rectpuls,pulsewidth);
        
           output = output.*amp;
        case 1 %noise
            lb = -(amp/2); %change
            ub = (amp/2); % 
            samp = fs*StopTime;
            output = lb + rand(1,samp)*(ub - lb);
            output = rot90(output);
        case 2 %chirp
            f0 = varargin{1};
            f1 = varargin{2};
            if ~exist('f0','var')
                f0 = 1000;
            end
            if ~exist('f1','var')
                f1 = 20000;
            end 
            x = chirp(t,f0,t(end),f1);
            output = x,fs;
        case 3 %sine
            sine_F = varargin{1}*1000; %khz to hz
            if ~exist('sine_F','var')
                sine_F = 5000;
            end 
            output = sin(2*pi*sine_F.*t);
        
        case 4 %periodic/square
            %???? not right
            f0 = varargin{1};
            f1 = varargin{2};
            if ~exist('square_F','var')
                square_F = 5000;
            end
            F = square_F;                    % Sine wave frequency (hertz)
            output = sin(2*pi*F*t);
            
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
             
    output=amp.*output.*env + offset;

%     plot(t,output)

end