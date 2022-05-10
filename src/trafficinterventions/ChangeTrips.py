import xml.etree.ElementTree as ET

"""
    @Class : To perform trip interventions
"""
class ChangeTrips():
    def __init__(self, fileName):
        self._fileName = fileName
        self._tree = ET.parse(self._fileName)
        self._root = self._tree.getroot()

    """
        Get Head of XML Tree
    """
    def getRootElementTag(self):
        return self._root.tag

    """
        Get different attribute types
    """
    def getUniqueParentTags(self):
        d = {}
        for child in self._root:
            if (child.tag) not in d:
                d[child.tag] = 1
            else:
                d[child.tag] += 1

        return d.keys()

    """
        Get all Trip IDs
    """
    def getLaneTypes(self):
        l = []
        for child in self._root:
            if child.tag == "trip":
                l.append(child.attrib["id"])

        return l

    """
        Change the start time of a trip
    """
    def changeTripStartTime(self, tripIDList, newStartTime, newFileName = None):
        for child in self._root:
            if child.tag == "trip" and newStartTime >= 0:
                attributesDict = child.attrib
                if int(attributesDict["id"]) in tripIDList:
                    child.set("depart", str(newStartTime))

        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))

    """
        Get Trip information
    """
    def getTripInformation(self):
        l = []
        for child in self._root:
            if child.tag == "trip":
                l.append(
                    (child.attrib["id"],
                    child.attrib)
                )
        return l