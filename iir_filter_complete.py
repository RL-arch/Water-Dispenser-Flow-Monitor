import scipy.signal as signal
import numpy as np



fs = 100

class IIR(object):
    """
    Given the proper parameters, this class calculates a filter (Butterworth, Chebyshev1 or Chebyshev2) and process an
    input value from the reading.
    Attributes:
        @:param order: Can be odd or even order as this class creates an IIR filter through the chain of second order filters and
        an extra first order at the end if odd order is required.
        @:param cutoff: For Lowpass and Highpass filters only one cutoff frequency is required while for Bandpass and Bandstop
        it is required an array of frequencies. The input values must be float or integer and the class will
        normalise them to the Nyquist frequency.
        @:param filterType: lowpass, highpass, bandpass, bandstop
        @:param design: butter, cheby1, cheby2.
        @:param rp: Only for cheby1, it defines the maximum allowed passband ripples in decibels.
        @:param rs: Only for cheby2, it defines the minimum required stopband attenuation in decibels.
        For the filtering of the signal, an IIR filter was implemented in the class IIR:
        IIR(order,cutoff,filterType,design='butter',rp=1,rs=1,fs=0)
        This class calculate the IIR filter coefficients for a given filter type ( Butter, Cheby1 or Cheby2)
        and then, the class function "filter" does the filtering to a given value.
    """
    def __init__(self, order, cutoff, filterType, design='butter', rp=1, rs=1):
        for i in range(len(cutoff)):
            cutoff[i] = cutoff[i] / fs * 2
        if design == 'butter':
            self.coefficients = signal.butter(order, cutoff, filterType, output='sos')
        elif design == 'cheby1':
            self.coefficients = signal.cheby1(order, rp, cutoff, filterType, output='sos')
        elif design == 'cheby2':
            self.coefficients = signal.cheby2(order, rs, cutoff, filterType, output='sos')
        self.acc_input = np.zeros(len(self.coefficients))
        self.acc_output = np.zeros(len(self.coefficients))
        self.buffer1 = np.zeros(len(self.coefficients))
        self.buffer2 = np.zeros(len(self.coefficients))
        self.input = 0
        self.output = 0

    def filter(self, input):
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
        for i in range(len(self.coefficients)):
            self.FIRcoeff = self.coefficients[i][0:3]
            self.IIRcoeff = self.coefficients[i][3:6]

            """
            IIR Part of the filter:
            The accumulated input are the values of the IIR coefficients multiplied
            by the variables of the filter: the input and the delay lines.
            """
            self.acc_input[i] = (self.input + self.buffer1[i]
                                 * -self.IIRcoeff[1] + self.buffer2[i] * -self.IIRcoeff[2])

            """
            FIR Part of the filter:
            The accumulated output are the values of the FIR coefficients multiplied
            by the variables of the filter: the input and the delay lines.
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

