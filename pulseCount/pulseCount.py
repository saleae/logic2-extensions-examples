# import math
# import numpy

from saleae.range_measurements import DigitalMeasurer

POSITIVE_PULSES = 'positivePulses'
NEGATIVE_PULSES = 'negativePulses'

class PosNegPulseMeasurer(DigitalMeasurer):
    supported_measurements = [POSITIVE_PULSES, NEGATIVE_PULSES]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.edges_rising = 0
        self.edges_falling = 0
        self.positive_pulses = 0;
        self.negative_pulses = 0;
    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        for t, bitstate in data:
            if bitstate:
                self.edges_rising += 1
            else:
                self.edges_falling += 1
            if self.edges_rising == self.edges_falling and bitstate:
                self.positive_pulses = self.edges_rising - 1
                self.negative_pulses = self.edges_falling
            elif self.edges_rising == self.edges_falling:
                self.positive_pulses = self.edges_rising
                self.negative_pulses = self.edges_falling - 1
            elif self.edges_rising > self.edges_falling:
                self.positive_pulses = self.edges_falling 
                self.negative_pulses = self.edges_falling
            elif self.edges_falling > self.edges_rising:
                self.positive_pulses = self.edges_rising
                self.negative_pulses = self.edges_falling - 1


    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

        if POSITIVE_PULSES in self.requested_measurements:
            values[POSITIVE_PULSES] = self.positive_pulses

        if NEGATIVE_PULSES in self.requested_measurements:
            values[NEGATIVE_PULSES] = self.negative_pulses
            
        return values
