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