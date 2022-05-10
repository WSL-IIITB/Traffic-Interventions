import trafficinterventions

"""
Note: If you wish to not rewrite the XML file, please add another parameter to the functions.
"""

"""
Change Trips Functionality
"""

# Instantiating an object of the XML Parser for Trip Modification
fileName = "sample3.xml" # Change the path of your file accordingly.
ct = trafficinterventions.ChangeTrips.ChangeTrips(fileName=fileName)

# Get Root Tag
print(ct.getRootElementTag())

# Get Unique Parent Tags
print(ct.getUniqueParentTags())

# Get all Trip IDs
print(ct.getLaneTypes())

# Get all Trip Information
print(ct.getTripInformation())

# Changing the start time of trip 3 to 1.00
ct.changeTripStartTime(
    [3],
    1.00
)