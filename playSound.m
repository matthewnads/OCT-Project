function playSound()
    [y,Fs] = audioread('handel.wav');
    sound(y,Fs)
end