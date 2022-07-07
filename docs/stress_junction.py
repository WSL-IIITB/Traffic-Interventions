import trafficinterventions

# Initialiasing the object
sj = trafficinterventions.StressJunction.StressJunction(
        weightsArray=[1,1,1,1,1], # Weights for the parameters - in the order of [haltingNumber, CO2Emissions, StepOccupancy, vehicleLength, waitingTime]
        pathCFG="map.sumocfg", # .sumocfg file path
        outPath="Outputs/", # Output path for screenshots
        pathNET="osm.net.xml", # .net.xml file path
        pathSummaryFile="stressed_junctions.txt", # File path for summary of the simulation
        numLocs = 5, # Number of stressed junctions to be printed
        initialPoiLocation = (5064.74,3568.48) # Center of the simulation
    )

# Run the simulation and get outputs   
sj.runSimulation()