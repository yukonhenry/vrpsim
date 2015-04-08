# Copyright YukonTR 2015
from input.jsoninput import read_json
from operation.simulation_admin import SimulationAdmin

def main():
    sa = SimulationAdmin(worldsize=200.0)
    plist = read_json("resources/producer_spec.json", "producerinfo_list")
    vlist = read_json("resources/vehicle_spec.json", "vehicleinfo_list")
    olist = read_json("resources/order_spec.json", "orderinfo_list")
    sa.prepare_simulation(producerinfo_list=plist, vehicleinfo_list=vlist,
                          orderinfo_list=olist)
    sa.simulation_run(100.0)
    sa.export_results()

if __name__ == '__main__':
    main()