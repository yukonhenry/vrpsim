# Copyright YukonTR 2015

import pytest

from input.jsoninput import read_json
from model.producer import Producer
from operation.simulation_admin import SimulationAdmin

def test_producer():
    p = Producer(0, worldsize=100.0)
    print p
    assert True

@pytest.fixture(scope="module")
def simadmin():
    sa = SimulationAdmin(worldsize=200.0)
    # read spec's for producers and instantiate producer-related objects
    # with specified parameters
    plist = read_json("resources/producer_spec.json", "producerinfo_list")
    vlist = read_json("resources/vehicle_spec.json", "vehicleinfo_list")
    olist = read_json("resources/order_spec.json", "orderinfo_list")
    sa.prepare_simulation(producerinfo_list=plist, vehicleinfo_list=vlist,
                          orderinfo_list=olist)
    print sa
    assert len(sa.producer_list) == len(plist)
    assert len(sa.workorder_list) == len(olist)
    assert len(sa.vehicle_list) == len(vlist)
    return sa


def test_workorder_generate(simadmin):
    simadmin.simulation_run(100.0)
    simadmin.export_results()
    assert True
