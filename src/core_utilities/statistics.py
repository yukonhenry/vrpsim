# Copyright YukonTR 2015

from numpy import mean, std
from collections import namedtuple

class Statistics(object):
    def __init__(self):
        pass

    def calc_mean(self, data_array):
        return mean(data_array)

    def calc_stddev(self, data_array):
        return std(data_array)

    def calc_meanstd(self, data_array):
        mean = self.calc_mean(data_array)
        std = self.calc_stddev(data_array)
        Mean_Std = namedtuple("Mean_Std", "mean std")
        return Mean_Std(mean, std)
