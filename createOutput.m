function [output] = createOutput(type, fs, fName) %params: fs, type, sine freq, stop time, f0, f1
    
    if ~exist('fName','var')
     % third parameter does not exist, so default it to something
      fName = 'handel.wav';
    end

    switch type
        case 0 %tone
            dt = 1/fs;                   % seconds per sample
            StopTime = 0.20;             % seconds
            t = (0:dt:StopTime-dt)';     % seconds
            F = 5000;                    % Sine wave frequency (hertz)
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
        case 1 %chirp
            dt = 1/fs;                   % seconds per sample
            StopTime = 0.10;             % seconds
            t = (0:dt:StopTime-dt)'; 
            f0 = 1000;
            f1 = 20000;
            x = chirp(t,f0,t(end),f1);
            output = x,fs;
        case 2
            [output, Fs] = audioread(fName);
    end
end