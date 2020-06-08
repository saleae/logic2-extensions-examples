import math
import numpy

from saleae.range_measurements import DigitalMeasurer

AVERAGE_PERIOD = 'averagePeriod'

class AveragePeriodMeasurer(DigitalMeasurer):
    supported_measurements = [AVERAGE_PERIOD]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        # We always need rising/falling edges
        self.edges_rising = 0
        self.edges_falling = 0
        self.first_transition_type = None
        self.first_transition_time = None
        self.last_transition_of_first_type_time = None

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
                current_period = t - (self.last_transition_of_first_type_time if self.last_transition_of_first_type_time is not None else self.first_transition_time)
                self.last_transition_of_first_type_time = t
            if bitstate:
                self.edges_rising += 1
            else:
                self.edges_falling += 1

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

    
        if AVERAGE_PERIOD in self.requested_measurements:
            if self.first_transition_time is not None and self.last_transition_of_first_type_time is not None:
                period_count = (self.edges_rising if self.first_transition_type else self.edges_falling) - 1
                values[AVERAGE_PERIOD] = 1 / (float(period_count) / (self.last_transition_of_first_type_time - self.first_transition_time))

        return values
