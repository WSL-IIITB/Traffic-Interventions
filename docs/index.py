import trafficinterventions

"""
Note: If you wish to not rewrite the XML file, please add another parameter to the functions.
"""

"""
Change Edges Functionality
"""

# Instantiating an object of the XML Parser for Lane Modification
fileName = "sample.xml" # Change the path of your file accordingly.
ce = trafficinterventions.ChangeEdges.ChangeEdges(fileName=fileName)

# Get Root Tag
print(ce.getRootElementTag())

# Get Unique Parent Tags
print(ce.getUniqueParentTags())

# Get the first 10 Lane Type IDs
print(ce.getUniqueEdgeIDs()[:10])

# Get Edge Inforation
ce.getEdgeInformation(["-734354815#0"])

# # Selectively disallow vehicle types from edge
ce.disallowAppendTypes(["truck", "bus"], ["-734354815#0"], None)

# Selectively allow vehicle types from edge
ce.allowAppendTypes(["e-scooter"], ["-777797681"], None)

"""
Change Lanes Functionality
"""
# Instantiating an object of the XML Parser for Lane Modification
fileName = "sample2.xml" # Change the path of your file accordingly.
cl = trafficinterventions.ChangeLanes.ChangeLanes(fileName=fileName)

# Get Root Tag
print(cl.getRootElementTag())

# Get Unique Parent Tags
print(cl.getUniqueParentTags())

# Get all Lane Type IDs
print(cl.getLaneTypes())

# Get all Lane Information
    
print(cl.getLaneInformation())

# Changing priorities of highway.cycleway lanes to 2
cl.changePriorityLanes(
    ["highway.cycleway"],
    2
)

# Changing the number of lanes reserved to highway.trunk to 3
cl.changeNumLanes(
    ["highway.cycleway"],
    3
)

# Toggling one-way status of railway.rail
cl.toggleOneWay(
    ["railway.rail"]
)

# Changing the number of lanes on the highway to double their original count 
l = cl.getLaneInformation()
for i in range(len(l)):
    cl.changeNumLanes(
        [l[i][0]],
        2 * int(l[i][1]["numLanes"])
    )

