import trafficinterventions

"""
Note: If you wish to not rewrite the XML file, please add another parameter to the functions.
"""

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