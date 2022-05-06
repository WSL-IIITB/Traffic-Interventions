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