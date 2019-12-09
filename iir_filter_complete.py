import scipy.signal as signal
import numpy as np


class IIR(object):
    """
    At the instantiation of the filter the following parameters are compulsory:
    Attributes:
    Comulsory:
        @:param order: positive integer
            Can be odd or even order as this class creates a chain of second
            order filters and an extra first order one if necessary.
        @:param cutoff: array/positive float
            Depending on the desired filter 1 cutoff frequency is to be
            enetered as a positive float for low/highpass filters or
            2 cutoff frequenices to be entered in an array as positive floats
            for bandstop and bandpass filters. These cutoff frequencies can be
            either entered as normalised to the Nyquist frequency (1 =
            Nyquist frequency) or as Hz (0 < f < Nyquist), but in this case fs,
            the sampling frequency has to be passed too.
        @:param filterType: string
            lowpass, highpass, bandpass, bandstop
    Non-compulsory:
        @:param design:
            Different types of coefficient generations
            can be chosen. The three available filters are Butterworth,
            Chebyshev type 1 or type 2.
            butter, cheby1, cheby2.
            If left unspecified the default value is butter.
        @:param rp: positive float
            Only for cheby1, it defines the maximum allowed passband ripples in decibels.
            If unspecified the default is 1.
        @:param rs: positive float
            Only for cheby2, it defines the minimum required stopband attenuation in decibels.
            If unspecified the default is 1.

        For the filtering of the signal, an IIR filter was implemented in the class IIR:
        IIR(order,cutoff,filterType,design='butter',rp=1,rs=1,fs=0)
        This class calculate the IIR filter coefficients for a given filter type ( Butter, Cheby1 or Cheby2)
        and then, the class function "filter" does the filtering to a given value.
    """
    def __init__(self, order, cutoff, filterType, design='butter', rp=1, rs=1,fs=0):
        for i in range(len(cutoff)):
            cutoff[i] = cutoff[i] / fs * 2
        if design == 'butter':
            self.coeff = signal.butter(order, cutoff, filterType, output='sos')
        elif design == 'cheby1':
            self.coeff = signal.cheby1(order, rp, cutoff, filterType, output='sos')
        elif design == 'cheby2':
            self.coeff = signal.cheby2(order, rs, cutoff, filterType, output='sos')
        else:
            self.error = 0
        self.acc_input = np.zeros(len(self.coeff))
        self.acc_output = np.zeros(len(self.coeff))
        self.buffer1 = np.zeros(len(self.coeff))
        self.buffer2 = np.zeros(len(self.coeff))
        self.input = 0
        self.output = 0
        self.error = 1

    def doFilter(self, input):
        """
        From the coefficients calculated in the constructor of the class, the filter is created as chains of IIR filters
        to obtain any order IIR filter. This is important as if order 8 IIR filter is required, it can be calculated as
        a chain of 4 2nd order IIR filters.
        :param input: input value from the reading in real time to be processed.
        :return: processed value.
        """
        self.input = input
        self.output = 0

        """ 
        This loop creates  any order filter by concatenating second order filters.
        If it is needed a 8th order filter, the loop will be executed 4 times obtaining
        a chain of 4 2nd order filters.
        """
        for i in range(len(self.coeff)):
            self.FIRcoeff = self.coeff[i][0:3]
            self.IIRcoeff = self.coeff[i][3:6]

            """
            IIR Part of the filter:
            The accumulated input are the values of the IIR coefficients multiplied
            by the variables of the filter:delay buffers weighed by the IIR coefficients.
            """
            self.acc_input[i] = (self.input + self.buffer1[i]
                                 * -self.IIRcoeff[1] + self.buffer2[i] * -self.IIRcoeff[2])

            """
            FIR Part of the filter:
            The accumulated output are the values of the FIR coefficients multiplied
            by the variables of the filter: input and the values from the delay bufferes 
            weighed by the FIR coefficients.
            """
            self.acc_output[i] = (self.acc_input[i] * self.FIRcoeff[0]
                                  + self.buffer1[i] * self.FIRcoeff[1] + self.buffer2[i]
                                  * self.FIRcoeff[2])

            # Shifting the values on the delay line: acc_input->buffer1->buffer2
            self.buffer2[i] = self.buffer1[i]
            self.buffer1[i] = self.acc_input[i]
            self.input = self.acc_output[i]

        self.output = self.acc_output[i]
        return self.output
