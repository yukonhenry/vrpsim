# Vehicle Routing Problem Simulator
Python/Simpy-based simulation platform to prototype Vehicle Routing Problem models and algorithms.  Initial implementation driven by focus on following three areas:

1. Statistical modeling of arrival rates for work orders, especially with respect to time-varying demands and modeling of transitions between busy/non-busy time periods.
2. Closed-form (or near closed-form) first-order resource planning based on demand forecast and simplifying assumptions.
3. Implementation of on-demand route planning with and without apriori statistical knowledge of demand and performance comparison between various implementations.

Entry points:
- (main) src/simstart.py
  - resource json files in src/resources directory
  - library config info in src/configinfo.md
  - Both main/test entry points instantiate SimulationAdmin objects, which initiates the simpy simulation environment https://simpy.readthedocs.org/en/latest/ which in turn initiates the various simulation processes and models that make up the elements of the VRP simulation model.
- (test) test/test_producer.py
  - utilizes py.test test frameork
  - library config info in src/configinfo.md
- (notebook) Not an entry point, but ipython notebook has experiments on arrival processes
  - time-varying rate characterization for non-homogeneous poisson process

Configuration:
- Adjust parameters JSON files in resources/ directory.  Parameters can be configured for vehicle, producers/goods manufacturers, and order arrival rates.  Variables such as consumer locations are randomly generated.
- Simulation lengths configured in main/test entry files as simulation admin instantiation parameter.
