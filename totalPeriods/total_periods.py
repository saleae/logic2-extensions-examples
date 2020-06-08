import math
import numpy

from saleae.range_measurements import DigitalMeasurer

TOTAL_PERIODS = 'totalPeriods'


class TotalPeriodMeasurer(DigitalMeasurer):
    supported_measurements = [TOTAL_PERIODS]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.edges_rising = 0
        self.edges_falling = 0
        self.first_transition_type = None
        self.first_transition_time = None
        self.next_transition_time = None


        self.pos_pulse_min = None
        self.total_periods = 0

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        for t, bitstate in data:
            if self.first_transition_type is None:
                self.first_transition_type = bitstate
                self.first_transition_time = t

            elif self.first_transition_type == bitstate:
                current_pulse = t - (self.next_transition_time if self.next_transition_time is not None else self.first_transition_time)
                self.next_transition_time = t

                self.total_periods += 1
            
            if bitstate:
                self.edges_rising += 1
            else:
                self.edges_falling += 1

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

        if TOTAL_PERIODS in self.requested_measurements:
            if self.total_periods is not None:
                values[TOTAL_PERIODS] = self.total_periods

        return values
