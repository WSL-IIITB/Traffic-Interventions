import trafficinterventions

# Initialiasing the object
sc = trafficinterventions.SpeedCamera.SpeedCamera(
    maxTimeSteps= 1000, # Number of simulation steps
    nearestNeighbourDisallow= 250.0, # Specifies how far detection points should be away from each other
    gridArray=[-10000,10000,10000,-10000], # Grid of interest : [left, right, up, down]
    pathCFG="map.sumocfg", # Input file path
    outPath="Outputs/", # Output file path (for screenshots)
    summaryFilePath="summary.txt", # File which contains the appropriate positions - populated after the simulation
    numLocs=5, # Number of locations you wish to retrieve
    colour=(255,0,0) # Colour of the speed camera points
)

# Run the simulation and get outputs
sc.runSimulation() 