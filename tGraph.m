function tGraph()
    sine_F = 5000;
    fs = 44000;
    amp= 2;
    StopTime = 0.1;
    offset = 1;
    dt = 1/fs;                   % seconds per sample
    t = (0:dt:StopTime-dt)';     % seconds
    tramp = StopTime/3;
    tsil = StopTime/9;
    F = sine_F;                    % Sine wave frequency (hertz)
    output = amp*sin(2*pi*F*t);
                
    %define envelope
    % env = ones(length(tone),1);
   
    output = pulstran(t,offset,'rectpuls',fs);

    plot(t, output)
end