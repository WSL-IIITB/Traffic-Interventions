import trafficinterventions
 
# Initialiasing the object
ej = trafficinterventions.EmissionJunction.EmissionJunction(
    pathCFG="map.sumocfg", # .sumocfg file path
    outPath="Outputs/", # Output path for screenshots
    pathNET="osm.net.xml", # .net.xml file path
    pathSummaryFile="polluted_junctions.txt", # File path for summary of the simulation
    numLocs = 5, # Number of stressed junctions to be printed
    initialPoiLocation = (5064.74,3568.48) # Center of the simulation
)

# Run the simulation and get outputs   
ej.runSimulation()