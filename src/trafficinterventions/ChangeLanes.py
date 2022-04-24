import xml.etree.ElementTree as ET

"""
    @Class : To perform lane change interventions
"""
class ChangeLanes():
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
        Get all Lane IDs
    """
    def getLaneTypes(self):
        l = []
        for child in self._root:
            if child.tag == "type":
                l.append(child.attrib["id"])

        return l

    """
        Change priority attributes of certain lanes
    """
    def changePriorityLanes(self, laneTypeList, newPriorityValue, newFileName = None):
        for child in self._root:
            if child.tag == "type":
                attributesDict = child.attrib
                if attributesDict["id"] in laneTypeList:
                    child.set("priority", str(newPriorityValue))
        
        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))

    """
        Change the number of lanes with given IDs
    """
    def changeNumLanes(self, laneTypeList, newNumberLanes, newFileName = None):
        for child in self._root:
            if child.tag == "type":
                attributesDict = child.attrib
                if attributesDict["id"] in laneTypeList:
                    child.set("numLanes", str(newNumberLanes))

        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))

    """
        Make certain lanes one-way, or reverse their states
    """
    def toggleOneWay(self, laneTypeList, newFileName = None):
        for child in self._root:
            if child.tag == "type":
                attributesDict = child.attrib
                if attributesDict["id"] in laneTypeList:
                    if str(attributesDict["oneway"]) == "0":
                        child.set("oneway", "1")
                    elif str(attributesDict["oneway"]) == "1":
                        child.set("oneway", "0")
        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))

    """
        Get Lane information
    """
    def getLaneInformation(self):
        l = []
        for child in self._root:
            if child.tag == "type":
                l.append(
                    (child.attrib["id"],
                    child.attrib)
                )
        return l