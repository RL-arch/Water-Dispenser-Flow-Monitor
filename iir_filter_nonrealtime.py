import matplotlib.pyplot as plt
import numpy as np
from iir_filter_complete import IIR2Filter

fs = 200
FilterMains = IIR2Filter(3,[45,55],'bandstop',design='cheby1',rp=0.01,fs=200)

impulse = np.zeros(1000)
impulse[0] = 1
impulseResponse = np.zeros(len(impulse))

for i in range(len(impulse)):
    impulseResponse[i] = FilterMains.filter(impulse[i])

# To obtain the frequency response from the impulse response the Fourier
# transform of the impulse response has to be taken. As it produces
# a mirrored frequency spectrum, it is enough to plot the first half of it.
freqResponse = np.fft.fft(impulseResponse)
freqResponse = abs(freqResponse[0:int(len(freqResponse)/2)])
xfF = np.linspace(0,fs/2,len(freqResponse))

plt.figure("Frequency Response")
plt.plot(xfF,np.real(freqResponse))
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.title("Bandstop")
