# CopyRight YukonTR 2015
from core_utilities.singletonlite import DestType, VehicleState, WorkOrderType


class Vehicle(object):
    def __init__(self, env, vid, initial_location, capacity=5, velocity=10.0):
        self._vid = vid
        self._location = initial_location
        self.capacity = capacity
        self._state = VehicleState.Idle
        # fiexed vehicle velocity value for now
        self.velocity = velocity
        self.env = env
        self.current_load = 0
        self.current_workorder = None
        # ref https://simpy.readthedocs.org/en/latest/topical_guides/process_interaction.html
        # car driving process initiated when Vehicle object created
        self.engine_run = env.process(self.engine_run(env))
        self.drive_event = self.env.event()


    def dispatch(self, dest, wtype, dist, remaining_workorder, ready_time=None):
        ''' dispactch called from delivery manager '''
        print "dispatched workorder %s" % (wtype,)
        self.current_drive = {"dest":dest, "dist":dist, "wtype":wtype, "ready_time":ready_time}
        self.next_drive = remaining_workorder
        self.drive_event.succeed()
        self.drive_event = self.env.event()

    def engine_run(self, env):
        ''' drive vehicle specified distance; there can be an interrupt from manager
            to change plans '''
        while True:
            # yield until drive activation
            print "Vehicle %d idle and waiting for workorder at time %f" % (self._vid, env.now)
            yield self.drive_event
            distance = self.current_drive["dist"]
            wtype = self.current_drive["wtype"]
            destination = self.current_drive["dest"]
            ready_time = self.current_drive["ready_time"]
            print "Vehicle %d heading for location %s at distance %f for type %s at time %f" %\
                  (self._vid, destination, distance, wtype, env.now)
            yield env.process(self.drive(env, destination, distance, wtype, ready_time))
            if self.next_drive:
                destination = self.next_drive.location
                distance = self._location.distance_to(destination)
                wtype = self.next_drive.wtype
                print "Vehicle %d heading automatically for location %s at distance %f for type %s at time %f" %\
                      (self._vid, destination, distance, wtype, env.now)
                yield env.process(self.drive(env, destination, distance, wtype))

    def drive(self, env, destination, distance, wtype, ready_time=None):
        '''
        :param env: simulation env
        :param destination: destination location
        :param distance: estimated distance
        :param wtype: workorder type
        :return:
        Make drive to next destination
        '''
        expected_transit_time = distance/self.velocity
        self._state = VehicleState.PickingUp if wtype == WorkOrderType.PickUp else VehicleState.Delivering
        yield env.timeout(expected_transit_time)
        print "Vehicle %d arrives at %s at time %s" % (self._vid, destination, env.now)
        self._location = destination
        if wtype == WorkOrderType.PickUp:
            if ready_time:
                if ready_time > env.now:
                    print "Vehicle %d at location, but product not ready until %f" % (self._vid, ready_time)
                    yield env.timeout(ready_time-env.now)
            print "Vehicle %d picking up at %s" % (self._vid, destination)
            self.current_load += 1
        else:
            print "Vehicle %d delivering at %s" % (self._vid, destination)
            self.current_load -= 1

    @property
    def location(self):
        return self._location

    @property
    def vid(self):
        return self._vid
