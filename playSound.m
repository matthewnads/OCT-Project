function playSound(fName)
    [y,Fs] = audioread(fName);
    sound(y,Fs)
end