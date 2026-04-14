import math
import numpy

from saleae.range_measurements import AnalogMeasurer

PEAK_TO_PEAK = 'peakToPeak'

class VoltagePeakToPeak(AnalogMeasurer):
    supported_measurements = [PEAK_TO_PEAK]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.measure_peak = PEAK_TO_PEAK in self.requested_measurements
        if self.measure_peak:
            self.minimum_value = math.inf
            self.maximum_value = -math.inf

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get Voltage values, one per sample
    #   * `data.samples` is a numpy array of float32 voltages, one for each sample
    #   * `data.sample_count` is the number of samples (same value as `len(data.samples)` but more efficient if you don't need a numpy array)
    def process_data(self, data):
        if self.measure_peak:
            min_val = numpy.amin(data.samples)
            self.minimum_value = min(min_val, self.minimum_value)
            max_val = numpy.amax(data.samples)
            self.maximum_value = max(max_val, self.maximum_value)

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

        if self.measure_peak:
            values[PEAK_TO_PEAK] = self.maximum_value - self.minimum_value

        return values
