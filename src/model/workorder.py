# Copyright YukonTR 2015

class WorkOrder(object):
    # workorder_id a class variable that keeps track of instance id number generation
    # Also equal to number of instantiations
    workorder_id = 0
    def __init__(self, env, dest_type, location, wtype, dest_id=None, ready_time=None, deadline_time=None):
        WorkOrder.workorder_id += 1
        # id for this workorder
        self.wid = WorkOrder.workorder_id
        self.env = env
        # id of destination (consumer may have none, only really applicable for producer)
        self.dest_id = dest_id
        self.dest_type = dest_type
        # minimum show-up time
        self.ready_time = ready_time
        # deadline for order to be completed, if applicable
        self.deadline_time = deadline_time
        self.location = location
        # workorder type
        self.wtype = wtype
