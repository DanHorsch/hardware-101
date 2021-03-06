"""
This module shows how to use an 5x7 led matrix. It contains a class LedMatrix
that can be used to easily access a matrix.

Pinout of the matrix:

1 +---+ 12
2 |   | 11
3 |   | 10
4 |   | 9
5 |   | 8
6 +---+ 7

Connections: Electrical current travels from columns to rows.

     1
   13078
12 ooooo ^
11 ooooo |
 2 ooooo |
 9 ooooo |
 4 ooooo |
 5 ooooo |
 7 ooooo |
   ---->
"""

import RPi.GPIO as GPIO
import time


class LedMatrix:

    def __init__(self, boardmode=GPIO.BCM):
        """Create an led matrix. Use the connect-method afterwards to connect
        led matrix pins with GPIO pins on the Raspberry Pi."""

        # a dictionary that holds led pins of the matrix and corresponding
        # GPIO pin on the Raspberry Pi.
        self.led_gpio = {}

        # default pins on a 5x7 matrix
        self.x_pins = [1, 3, 10, 7, 8]
        self.y_pins = [12, 11, 2, 9, 4, 5, 6]

        # using the given numbering scheme
        GPIO.setmode(boardmode)

    def connect_pins(self, ledpin, gpiopin):
        """Connect a Pin of the LED Matrix with a GPIO pin on the Raspberry
        Pi."""
        self.led_gpio[ledpin] = gpiopin

        # configure all pins as output
        GPIO.setup(gpiopin, GPIO.OUT)

    def led(self, x, y, on_off):
        """Turn the led at coordinate (x,y) on or off. Starting with (0,0) at
        top left. Multiple LEDs that are not all in one row/column cannot be
        handled this way. Use multiplexing instead - as described here
        https://www.mikrocontroller.net/articles/LED-Matrix#Multiplexbetrieb"""

        # electric current can only travel from column (y) to row (x)
        if on_off:
            ledpin_lo = self.x_pins[x]
            ledpin_hi = self.y_pins[y]
        else:
            ledpin_hi = self.x_pins[x]
            ledpin_lo = self.y_pins[y]

        # determine GPIO pins for led pins
        gpio_hi, gpio_lo = self.led_gpio[ledpin_hi], self.led_gpio[ledpin_lo]

        GPIO.output(gpio_hi, GPIO.HIGH)
        GPIO.output(gpio_lo, GPIO.LOW)


def main():
    ledmat = LedMatrix()
    # connect pins of the led-matrix to GPIO-pins
    ledmat.connect_pins(ledpin=1, gpiopin=17)
    ledmat.connect_pins(ledpin=3, gpiopin=18)
    ledmat.connect_pins(ledpin=11, gpiopin=23)
    ledmat.connect_pins(ledpin=12, gpiopin=22)

    # turn on each of the 4 LEDs from top left to bottom right - for 5 seconds
    start = time.time()
    while time.time() - start < 5:
        for y in (0, 1):
            for x in (0, 1):
                ledmat.led(x, y, True)
                time.sleep(0.2)
                ledmat.led(x, y, False)
                time.sleep(0.2)

    # turning on two leds at (0,0) and (0,1) using multiplexing
    while True:
        for x in (0, 1):
            for y in (0, 1):
                if (x, y) in [(0, 0), (1, 1)]:
                    ledmat.led(x, y, True)
                    time.sleep(0.001)
                    ledmat.led(x, y, False)


if __name__ == "__main__":
    main()
