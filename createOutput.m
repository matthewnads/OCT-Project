function [output] = createOutput(type, fs, StopTime, dtcycle, sine_F, f0, f1) 
    % seconds StopTime

    %main params: type, sampling frequency, amp, t-silence, t-ramp, offset
    %optional args: duty cycle, pulse width (pulse), f0, f1 (chirp), sine 

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
           %d = (0:)
           output = pulstran(t,t,x);
           plot(t, output);
        case 1 %noise
            lb = -1; %change
            ub = 1; % 
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
                
            %define envelope
            % env = ones(length(tone),1);
            rep_no=5;
            rep_sz=length(output)/rep_no;
            hf_rep = rep_sz/2;
                
            env=[];
            for i = 1:5
                temp = vertcat(zeros(hf_rep,1), ones(hf_rep,1));
                env = vertcat(env,temp);   
            end
              
            output=output.*env;
        
        case 4 %periodic/square
            
    end
end