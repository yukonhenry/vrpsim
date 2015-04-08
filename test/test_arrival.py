__author__ = 'henry'

from model.arrival_stochastics import ArrivalStochastics
from core_utilities.exportplot import ExportPlot
from core_utilities.statistics import Statistics


def test_exponential_arrival():
    arrival_mean = 2.0
    lambd = 1.0/arrival_mean
    s = ArrivalStochastics(lambd_rate=lambd, dist_type="p")
    arrival_history = s.run(1000)
    e = ExportPlot(filename_base="exponential")
    e.simple_plot(arrival_history)
    e.hist_plot(arrival_history)
    st = Statistics()
    mstd = st.calc_meanstd(arrival_history)
    print "expected mean=%f variance=%f" % (arrival_mean, arrival_mean**2)
    print 'mean=%f std=%f variance=%f' % (mstd.mean, mstd.std, mstd.std**2)
    assert True

def test_nonhomogeneous_arrival():
    # implement non-homogenous poisson process arrival
    # arrival rate is non-constant and governed by (deterministic)
    # derivative of logistic(sigmoid) function
    time_constant = 50
    lambd = 1.0/time_constant
    s = ArrivalStochastics(lambd_rate=lambd, dist_type="d")
    arrival_history = s.run(1000)
    e = ExportPlot(filename_base="logistics")
    e.simple_plot(arrival_history)
    e.hist_plot(arrival_history)
    st = Statistics()
    mstd = st.calc_meanstd(arrival_history)
    print 'mean=%f std=%f variance=%f' % (mstd.mean, mstd.std, mstd.std**2)
    assert True
