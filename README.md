# Traffic-Interventions

## Installation
- `python -m pip install --upgrade pip`
- `pip install trafficinterventions xml`

--- 
## Documentation
All relevant files can be found [here](https://github.com/WSL-IIITB/Traffic-Interventions/tree/main/docs)

--- 

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
