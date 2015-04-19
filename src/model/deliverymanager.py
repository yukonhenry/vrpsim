# Copyright YukonTR 2015
from operator import itemgetter


class DeliveryManager(object):
    ''' Delivery Manager manages vehicle resources and their routes
    '''
    def __init__(self, env):
        # simulation environment
        self.env = env
        self._vehicle_list = None
        self.vindexerGet = lambda x: dict((p.vid,i) for i,p in enumerate(
            self.vehicle_list)).get(x)
        self.dashboard_run_process = env.process(self.dashboard_run(env))

    def set_workorder(self, workorder, remaining_workorder):
        # workorder ia assigned from producer (after producer receives workorder event after arrival rate expiration
        print "*******************"
        print "workorder received at %f for producer %d at %s ready by %f customer location=%s" % \
              (self.env.now, workorder.dest_id, workorder.location, workorder.ready_time,
               remaining_workorder.location)
        plocation = workorder.location
        closest_dict = self.find_closest_available_vehicle(plocation)
        closest_vid = closest_dict["vid"]
        dist_to_producer = closest_dict["dist"]
        closest_vehicle = self._vehicle_list[self.vindexerGet(closest_vid)]
        closest_vehicle.dispatch(dest=plocation, wtype=workorder.wtype, dist=dist_to_producer,
                                 ready_time=workorder.ready_time,
                                 remaining_workorder=remaining_workorder)

    def find_closest_available_vehicle(self, plocation):
        distance_list = [{"vid":x.vid, "dist":x.location.distance_to(plocation)}
                         for x in self.vehicle_list if x.drive_event and x.has_space()]
        min_dict = min(distance_list, key=itemgetter("dist"))
        return min_dict

    def dashboard_run(self, env):
        pass

    @property
    def vehicle_list(self):
        return self._vehicle_list

    @vehicle_list.setter
    def vehicle_list(self, value):
        self._vehicle_list = value
