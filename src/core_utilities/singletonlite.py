# Copyright YukonTR 2015
# module-based ssingleton to implement globals
# define enums
from enum import Enum
DestType = Enum('DestType', 'Producer Consumer')
VehicleState = Enum('VehicleState', 'Idle PickingUp Delivering')
WorkOrderType = Enum('WorkOrderType', 'PickUp Delivery')