import math
import os
import sys
import optparse
import traci
from sumolib import checkBinary 
from collections import Counter

"""
   @Class: Helper class to store vehicle attributes
"""
class Vehicle:
    _laneId = None 
    _speedLastTimeStep = None 

    def __init__(self, laneId, speedLastTimeStep) -> None:
        self._laneId = laneId
        self._speedLastTimeStep = speedLastTimeStep

    def getLaneId(self) -> int:
        return self._laneId

    def getSpeedLastTimeStep(self) -> float:
        return self._speedLastTimeStep

    @staticmethod
    def checkPositionInBox(left, right, up, down, x, y):
        if x < left or x > right:
            return False 
        if y < down or y > up:
            return False 
        return True

"""
    @Class: Helper class to store vehicle position and speed values
"""
class VehiclePosition:
        _x = None 
        _y = None 
        _speedLastTimeStep = None 

        def __init__(self, x, y, speedLastTimeStep) -> None:
            self._x = x 
            self._y = y 
            self._speedLastTimeStep = speedLastTimeStep

        def getPosition(self):
            return self._x, self._y
        
        def getSpeedLastTimeStep(self) -> float:
            return self._speedLastTimeStep

"""
    @Class: Data Structure to store speed and position tuples
"""
class SpeedPositionHelper:
    _positionList = None
    _speed = None 

    def __init__(self, positionList, speed) -> None:
        self._positionList = positionList
        self._speed = speed
    
    def getPosition(self) -> list:
        return self._positionList

    def getSpeed(self) -> float:
        return self._speed
    
    def getX(self) -> float:
        return self._positionList[0]

    def getY(self) -> float:
        return self._positionList[1]

"""
    @Class: Distance calculation and nearest neighbour removal functions
"""
class DistanceCalculationHelper:
    _nearest = None 
    _pointList = None

    def __init__(self, nearest, sortedPointList):
        self._nearest = nearest
        self._pointList = sortedPointList
    
    @staticmethod
    def getDistanceBetweenPoints(x1, x2, y1, y2):
        return math.sqrt(
            (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
        )
    
    def removeNearestList(self):
        l = []
        i = 0 
        while i < len(self._pointList):
            l.append(self._pointList[i])
            j = (i+1)
            while j < len(self._pointList):
                x1 = self._pointList[i][0]
                y1 = self._pointList[i][1]
                x2 = self._pointList[j][0]
                y2 = self._pointList[j][1]

                d = DistanceCalculationHelper.getDistanceBetweenPoints(x1,x2,y1,y2)
                if d <= self._nearest:
                    j += 1 
                else:
                    break
            i = j    
        return l 
        
"""
    @Class: Main class to find speed camera locations
"""
class SpeedCamera:
    """
        @Method: Initialing variables and config
    """
    def __init__(self, maxTimeSteps, nearestNeighbourDisallow, gridArray, pathCFG, outPath, summaryFilePath, numLocs, colour):
        
        # Check for Bash Shortcut
        if "SUMO_HOME" in os.environ:
            sys.path.append(os.path.join(
                os.environ["SUMO_HOME"],
                "tools"
            ))
        else:
            sys.exit("Please populate $SUMO_HOME in your .bashrc file.") 

        # Assign all variables
        self.maxTimeSteps = maxTimeSteps
        self.nearestNeighbourDisallow = nearestNeighbourDisallow
        self.left = gridArray[0]
        self.right = gridArray[1]
        self.up = gridArray[2]
        self.down = gridArray[3]
        self.pathCFG = pathCFG
        self.outPath = outPath
        self.summaryFilePath = summaryFilePath
        self.numLocs = numLocs
        self.colour = colour 

        # Option Parser
        optParser = optparse.OptionParser()
        optParser.add_option(
            "--nogui", 
            action = "store_true",
            default = False,
            help = "Please run sumo --help."
        )
        options, args = optParser.parse_args()
        self.options = options

        # Variables used in the simulation
        self.vehiclesDict = {}
        self.freqDict = {}
        self.iters = 0 
        self.previousPOI = []
        self.deleteOldPOI = False 


    """
        @Method: Helper function for sorting based on speed values
    """
    def speedCompareKey(self, item):
        return -item.getSpeed()
    
    """
        @Method: TraCI simulation step and calculation of positions - run in the runSimulation() method
    """
    def loop(self):
        timeStep = 0 

        while traci.simulation.getMinExpectedNumber() > 0 and timeStep <= self.maxTimeSteps:
            traci.simulationStep()

            positionsList = []
            for v in traci.vehicle.getIDList():
                x,y = traci.vehicle.getPosition(v) 
                cs = traci.vehicle.getSpeedWithoutTraCI(v)
                
                if Vehicle.checkPositionInBox(self.left,self.right,self.up,self.down,x,y):
                    if v not in self.vehiclesDict or cs > self.vehiclesDict[v].getSpeedLastTimeStep():
                        vo = VehiclePosition(x = x, y = y, speedLastTimeStep = cs)
                        self.vehiclesDict[v] = vo 
                            
                        xys = SpeedPositionHelper(positionList = [x,y], speed = cs)
                        positionsList.append(xys)
                            
                        if (x,y) not in self.freqDict: 
                            self.freqDict[(x,y)] = 1 
                        else:
                            self.freqDict[(x,y)] += 1

            positionsList.sort(key = self.speedCompareKey)

            # Closest Distance Logic
            distList = []
            for p in range(len(positionsList)):
                l = []
                l.append(positionsList[p].getX())
                l.append(positionsList[p].getY())
                distList.append(l)

            dcHelper = DistanceCalculationHelper(self.nearestNeighbourDisallow, distList)
            positionsList = dcHelper.removeNearestList()
            
            for i in range(min(5, len(positionsList))):
                nid = "demo" + str(self.iters)
                self.iters += 1

                if self.iters % 200 == 0:
                    if self.deleteOldPOI == True:
                        for oldID in self.previousPOI:
                            try:
                                traci.poi.remove(oldID)
                            except Exception as e:
                                print(e)
                    self.previousPOI = []
                    traci.poi.add(poiID=nid, x = positionsList[i][0], y = positionsList[i][1], layer = 202.0, color = self.colour)
                    traci.gui.toggleSelection(nid, objType='poi')
                    self.previousPOI.append(nid)

            timeStep += 1 

    """
        @Method: Printing Location Info
    """
    def printLocations(self):
        traci.close()
        sys.stdout.flush()
        print("-"*100)
        numLocs = self.numLocs
        numLocs = min(numLocs, len(self.freqDict.keys()))
        c = Counter(self.freqDict)
        for xyloc in c.most_common()[:numLocs]:
            print(f"Position, Violation count: {xyloc}")

        with open(self.summaryFilePath,'w') as f:
            for xyloc in c.most_common()[:numLocs]:
                f.write(f"Position, Violation count: {xyloc}" + "\n")
    

    """
        @Method: Main Method for Speed Camera simulation
    """
    def runSimulation(self):

        # Setting Sumo Binary
        if self.options.nogui:
            sumoBinary = checkBinary("sumo")
        else:
            sumoBinary = checkBinary("sumo-gui")   

        # Running the loop
        traci.start([sumoBinary, "-c", self.pathCFG, "--tripinfo-output", "tripinfo.xml", "--time-to-teleport", "-1"])
        self.loop()

        # Printing the locations and saving screenshots
        filename = self.outPath + 'speedcams.jpg'
        traci.simulationStep()
        traci.gui.screenshot('View #0', filename)    
        traci.simulationStep()
        self.printLocations()
