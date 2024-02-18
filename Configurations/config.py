class Config:
    """
    Configuration class for the simulation.
    Time is in minutes i.e. 1 unit is 1 minute
    """
    SIMULATION_TIME: int = 1200  # Total simulation time.
    CONTAINERS_PER_VESSEL: int = 150  # Number of containers in a vessel
    TOTAL_CRANES: int = 2  # Total number of cranes available at the terminal
    # Time taken by a train to pick up and drop off a container in a truck.
    TIME_OF_CRANE_UNLOAD: int = 3
    # Average time taken for a vessel to arrive i.e 5 hours
    TIME_BETWEEN_VESSELS: int = 300
    BERTH_COUNT: int = 2  # Total number of berths in the terminal
    CRANE_COUNT: int = 2  # Total number of cranes in the terminal
    TRUCK_COUNT: int = 3  # Total number of trucks in the terminal
    # Time taken by a truck to transport a container to yard and come back to the terminal.
    TRUCK_TRANSPORTATION_TIME: int = 6
