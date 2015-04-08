# Copyright YukonTR 2015
import simpy
from math import exp
from random import expovariate
from core_utilities.sim_exceptions import CodeLogicError, ConfigurationError

HP = "hp"  # homoegeneous poisson
NHP_L = "nhp_l" # non-homogeneous poisson, logistics func
NHP_GL = "nhp_gl" # non-homogeneous poisson, generalized logistics func
class ArrivalStochastics(object):
    def __init__(self, env=None, lambd_rate=0.0, dist_type="p", customer_loc_list=None, pid=-1, producer_action=None):
        self.env = env if env else simpy.Environment()
        # assign producer id that this arrival process is attached to
        self.pid = pid
        self.lambd_rate = lambd_rate
        self._arrival_history = list()
        if dist_type == HP:
            dist_func = lambda x: lambd_rate
        elif dist_type == NHP_L:
            dist_func = lambda x: self.logistics_deriv_func(NHP_L, x, x0=500, L=100, k=0.01)
        elif dist_type == NHP_GL:
            dist_func = lambda x: self.logistics_deriv_func(NHP_GL, x, x0=500, L=100, k=0.01, alpha=1.0)
        else:
            raise ConfigurationError("JSON configuration does not have correct statistics distribution type %s" %
                                     (dist_type,))
        if not producer_action:
            raise CodeLogicError("producer action needs to be declared for arrival process")
        else:
            self.env.process(self.arrival_generate(self.env, dist_func, producer_action, iter(customer_loc_list)))


    def run(self, timeinterval):
        self.env.run(until=timeinterval)
        return self._arrival_history
    '''
    Model quiescence, growth, then saturation.
    Ref standard logistics function http://en.wikipedia.org/wiki/Logistic_function
    See ipython Notebook under notebook dir for parameter experimentation
    f(x) = L/(1+exp(-k*(x-x0))
    More generalized logistic function defined by
    f(x) = L/(1+alpha*exp(-k*(x-x0))

    Derivatives (with respect to x (or time) for both standard and generalized logistics function is
    f'(x) = k*f(x)(1-f(x/L))
    x0 = the x-value of the sigmoid's midpoint,
    L = the curve's maximum value, and
    k reflects the steepness of the curve
    alpha affects curve inflection point for generalized logistics function
    '''
    def logistics_func(self, x, x0, L, k):
        return L/(1+exp(-k*(x-x0)))

    # more generalized logistics function
    def gen_logistics_func(x, x0, L, k, alpha):
        return L/(1+alpha*exp(-k*(x-x0)))

    def logistics_deriv_func(self, dist_type, x, x0, L, k, alpha=None):
        f_x = self.logistics_func(x, x0, L, k) if dist_type==NHP_L else self.gen_logistics_func(x, x0, L, k, alpha)
        return k*f_x*(1.0-f_x/L)

    def arrival_generate(self, env, dist_func, producer_action, customer_loc_iter):
        while True:
            # define arrival event
            arrival_event = env.event()
            arrival_event.callbacks.append(producer_action)
            # get effective poisson rate based on current specified distribution function
            effective_rate = dist_func(env.now)
            print "time= %f producer=%d effective rate= %f" % (env.now, self.pid, effective_rate)
            arrival_duration = expovariate(effective_rate)
            yield env.timeout(arrival_duration)
            print "time=%f producer=%d arrival duration=%f" % (env.now, self.pid, arrival_duration)
            try:
                customer_loc = customer_loc_iter.next()
                # arrival event only completes if there is a valid customer order
                arrival_event.succeed(value=customer_loc)
            except StopIteration:
                customer_loc = None
            #interrupt_process.interrupt(customer_loc)
            # append to history after the arrival time has actually occurred
            self._arrival_history.append(arrival_duration)

    @property
    def arrival_history(self):
        return self._arrival_history