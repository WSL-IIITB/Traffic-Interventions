# Traffic-Interventions

## Installation
- `python -m pip install --upgrade pip`
- `pip install --upgrade trafficinterventions`

--- 
## Documentation
All relevant files can be found [here](https://github.com/WSL-IIITB/Traffic-Interventions/tree/main/docs)

--- 

## Interventions

### Sample Usage : Edge Manipulation
```py
import trafficinterventions

ce = trafficinterventions.ChangeEdges.ChangeEdges(fileName="sample.xml")

# Sample Intervention
ce.disallowAppendTypes(["bus"], ["-100"], "new_file.xml")
```
---

### Sample Usage : Lane Manipulation
```py
import trafficinterventions

cl = trafficinterventions.ChangeLanes.ChangeLanes(fileName="sample.xml")

# Sample Intervention
ce.changePriorityLanes(["highway.cycleway"], 100, "new_file.xml")
```
---

### Sample Usage : Trip Manipulation
```py
import trafficinterventions

ct = trafficinterventions.ChangeTrips.ChangeTrips(fileName="sample.xml")

# Sample Intervention
ct.changeTripStartTime([3], 1.00, "new_file.xml")
```
---


## Simulations

### Sample Usage: Speed Camera Placement
```py
import trafficinterventions


sc = trafficinterventions.SpeedCamera.SpeedCamera(
    maxTimeSteps= 1000,
    nearestNeighbourDisallow= 250.0,
    gridArray=[-10000,10000,10000,-10000],
    pathCFG="map.sumocfg",
    outPath="Outputs/",
    summaryFilePath="summary.txt",
    numLocs=5
)

# Run the simulation and get outputs
sc.runSimulation() 
```
---

### Sample Usage: Stressed Junctions Detection
```py
import trafficinterventions


sj = trafficinterventions.StressJunction.StressJunction(
        maxTimeSteps=1000, 
        weightsArray=[1,1,1,1,1], 
        pathCFG="map.sumocfg", 
        outPath="Outputs/", 
        pathNET="osm.net.xml", 
        pathSummaryFile="stressed_junctions.txt", 
        numLocs = 5,
        initialPoiLocation = (5064.74,3568.48) 
)

# Run the simulation and get outputs   
sj.runSimulation()
```
---
### Sample Usage: Polluted Junctions Detection
```py
import trafficinterventions


ej = trafficinterventions.EmissionJunction.EmissionJunction(
    maxTimeSteps=1000, 
    pathCFG="map.sumocfg", 
    outPath="Outputs/", 
    pathNET="osm.net.xml", 
    pathSummaryFile="polluted_junctions.txt", 
    numLocs = 5, 
    initialPoiLocation = (5064.74,3568.48) 
)

# Run the simulation and get outputs   
ej.runSimulation()
```