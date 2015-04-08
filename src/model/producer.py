# Copyright YukonTR 2015
import random
from model.location import Location
from model.workorder import WorkOrder
from core_utilities.singletonlite import WorkOrderType, DestType


class Producer(object):
    def __init__(self, pid, location=None, production_time=0, worldsize=100.0, env=None, deliverymgr=None):
        self._pid = pid
        if location is None:
            x = random.random()*worldsize
            y = random.random()*worldsize
            self.location = Location(x,y)
        else:
            self.location = location
        # workorder list for this producer
        self._workorder_list = None
        self.deliverymgr = deliverymgr
        # time required to produce product; if stochastic, indicates mean value
        self.production_time = production_time
        self.env = env

    def __str__(self):
        return "producer "+str(self._pid)+ " "+str(self.location)

    @property
    def pid(self):
        return self._pid

    # arrival rate triggers producer event
    def producer_action(self, event):
        print "-----------------------"
        print "event triggered customer_loc=%s val=%s" % (event, event.value)
        customer_loc = event.value
        producer_workorder = WorkOrder(env=self.env, dest_type=DestType.Producer, dest_id=self.pid,
                                       ready_time=self.env.now+self.production_time,
                                       location=self.location, wtype=WorkOrderType.PickUp)
        delivery_workorder = WorkOrder(env=self.env, dest_type=DestType.Consumer,
                                       location=customer_loc, wtype=WorkOrderType.Delivery)
        self.deliverymgr.set_workorder(workorder=producer_workorder, remaining_workorder=delivery_workorder)
