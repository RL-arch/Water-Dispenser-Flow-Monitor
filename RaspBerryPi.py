import pyfirmata2
import time, sys

# Adjust that the port match your system, see samples below:
# On Linux: /dev/tty.usbserial-A6008rIF, /dev/ttyACM0,
# On Windows: \\.\COM1, \\.\COM2
PORT =  pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT)

PIN= 13 #pin
rate_cnt = 0
tot_cnt = 0
time_zero = 0.0
time_end = 0.0
gpio_last = 0
pulses = 0
constant = 1.79

print('Water Flow - Approximate')
print('Control C to exit')

time_zero = time.time()
while True:
    rate_cnt = 0
    pulses = 0
    time_start = time.time()
    while pulses <= 5:
        gpio_cur = board.digital[PIN]
        if gpio_cur != 0 and gpio_cur != gpio_last:
            pulses += 1
        gpio_last = gpio_cur
        try:
            #print(board.digital[PIN], end='')
            None
        except KeyboardInterrupt:
            print('\nCTRL C - Exciting nicely')
            #GPIO.cleanup()
            print('Done')
            sys.exit()

    rate_cnt += 1
    tot_cnt += 1
    time_end = time.time()

    print('\nLiters /min',
          round((rate_cnt * constant)/(time_end - time_start),2),
          'approximate')
    print('Total Liters ', round(tot_cnt * constant, 1))
    print('Time (min & clock)',
          round((time.time()-time_zero)/60,2),'\t',
          time.asctime(time.localtime(time.time())),'\n')
