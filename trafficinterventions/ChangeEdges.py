import xml.etree.ElementTree as ET

"""
    @Class : To perform edge change interventions
"""

class ChangeEdges():
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
        Get all Edge IDs
    """
    def getUniqueEdgeIDs(self):
        l = []
        for child in self._root:
            if child.tag == "edge":
                l.append(child.attrib["id"])
        
        return list(set(l))

    """
        Get Edge Information
    """
    def getEdgeInformation(self, edgeIdList):
        for child in self._root:
            if child.tag == "edge":
                if child.attrib["id"] in edgeIdList:
                    for lanes in child:
                        print(lanes.attrib)

    """
        Disallow certain vehicle types at edges
        @Link: https://sumo.dlr.de/docs/Vehicle_Type_Parameter_Defaults.html
    """
    def disallowAppendTypes(self, vehicleTypes, edgeIdList, newFileName = None):
        for child in self._root:
            if child.tag == "edge":
                if child.attrib["id"] in edgeIdList:
                    for lanes in child:
                        attributesDict = lanes.attrib
                        if "disallow" in attributesDict:
                            s = attributesDict["disallow"]
                            for v in vehicleTypes:
                                if v not in s:
                                    s += " "
                                    s += str(v)
                            lanes.set("disallow", s)

        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))

    """
        Allow certain vehicle types at edges
        @Link: https://sumo.dlr.de/docs/Vehicle_Type_Parameter_Defaults.html
    """
    def allowAppendTypes(self, vehicleTypes, edgeIdList, newFileName = None):
        for child in self._root:
            if child.tag == "edge":
                if child.attrib["id"] in edgeIdList:
                    for lanes in child:
                        attributesDict = lanes.attrib
                        if "allow" in attributesDict:
                            s = attributesDict["allow"]
                            for v in vehicleTypes:
                                if v not in s:
                                    s += " "
                                    s += str(v)
                            lanes.set("allow", s)

        if newFileName is None:
            self._tree.write(self._fileName)
        else:
            self._tree.write(str(newFileName))