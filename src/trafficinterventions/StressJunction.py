import os
import sys
import optparse
from unittest.main import main
import traci
import sumolib
from numpy import double
from sumolib import checkBinary 


"""
    @Class: Helper class with methods pertaining to stress calculation
"""

class StressHelper:

    """
        @Method: MinMax scaling of a dict parameter
    """
    @staticmethod
    def normalise(dict):
        xmax = -1 
        xmin = 100000
        for key in dict:
            xmax = max(xmax,dict[key])
            xmin = min(xmin,dict[key])

        if(xmax-xmin > 0):
            for key in dict: 
                dict[key] = (dict[key] - xmin)/(xmax-xmin) 

        return dict

    """
        @Method: Get specific stress parameter
    """
    @staticmethod
    def getStressAt(junction,parameter):
        value = 0 
        incoming_edges = junction.getIncoming()
        for edge in incoming_edges:
            lanes = edge.getLanes()
            for lane in lanes:
                lane_id = lane.getID()

                if(parameter == "haltingNumber"):
                    edgeValue = traci.lane.getLastStepHaltingNumber(lane_id)
                
                if(parameter == "CO2Emissions"):
                    edgeValue = traci.lane.getCO2Emission(lane_id)

                if(parameter == "StepOccupancy"):
                    edgeValue = traci.lane.getLastStepOccupancy(lane_id)
                
                if(parameter == "vehicleLength"):
                    edgeValue = traci.lane.getLastStepLength(lane_id)

                if(parameter == "waitingTime"):
                    edgeValue = traci.lane.getWaitingTime(lane_id)
                value += edgeValue
            
        return value

"""
    @Class: Main class for stress analysis
"""
class StressJunction:
    """
        @Method: Initialising variables and config
    """ 
    def __init__(self,  weightsArray, pathCFG, outPath, pathNET, pathSummaryFile, numLocs, initialPoiLocation = (5064.74,3568.48)):
        
        # Check for Bash Shortcut
        if "SUMO_HOME" in os.environ:
            sys.path.append(os.path.join(
                os.environ["SUMO_HOME"],
                "tools"
            ))
        else:
            sys.exit("Please populate $SUMO_HOME in your .bashrc file.") 

        # Assign all variables
        self.weightsArray = weightsArray
        self.pathCFG = pathCFG
        self.outPath = outPath
        self.numLocs = numLocs
        self.net = sumolib.net.readNet(pathNET)
        self.pathSummaryFile = pathSummaryFile
        self.initialPoiLocation = initialPoiLocation


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

        # Initialise variables used in the simulation
        self.weights = {
            "haltingNumber":1,
            "CO2Emissions":1,
            "StepOccupancy":1,
            "vehicleLength":1,
            "waitingTime":1
        }

        if weightsArray[0] is not None:
            self.weights["haltingNumber"] = self.weightsArray[0]
        if weightsArray[1] is not None:
            self.weights["CO2Emissions"] = self.weightsArray[1]
        if weightsArray[2] is not None:
            self.weights["StepOccupancy"] = self.weightsArray[2]
        if weightsArray[3] is not None:
            self.weights["vehicleLength"] = self.weightsArray[3]
        if weightsArray[4] is not None:
            self.weights["waitingTime"] = self.weightsArray[4]
        
        self.junctions = self.net.getNodes()
        self.junctionsEmissions = []

        for _ in range(len(self.junctions)):
            self.junctionsEmissions.append([])

    """
        @Method: TraCI simulation step and calculation of positions - run in the runSimulation() method
    """
    def loop(self):
        traci.poi.add("index", self.initialPoiLocation[0], self.initialPoiLocation[1], (255,255,255), layer=202.0)
        step = 0

        steps = []
        stressedCounts = {}
        weights = self.weights
        max_list = []

        junctions = self.junctions
        locs = min(5, self.numLocs)
        

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            traci.poi.setType('index', 'TimeStep = '+str(step))
            if step%100 == 0:
                if(step!=0):
                    for i in range(locs):
                        traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
                
                max_list = {}
                max_dict = {}
                parameterDict = {}
                for idx, junction in enumerate(junctions):
                    stress = StressHelper.getStressAt(junction,"haltingNumber")
                    self.junctionsEmissions[idx].append(stress)
                    parameterDict[idx] = stress
                max_dict["haltingNumber"] = parameterDict 

                parameterDict = {}
                for idx, junction in enumerate(junctions):
                    stress = StressHelper.getStressAt(junction,"CO2Emissions")
                    self.junctionsEmissions[idx].append(stress)
                    parameterDict[idx] = stress
                max_dict["CO2Emissions"] = parameterDict 

                parameterDict = {}
                for idx, junction in enumerate(junctions):
                    stress = StressHelper.getStressAt(junction,"StepOccupancy")
                    self.junctionsEmissions[idx].append(stress)
                    parameterDict[idx] = stress
                max_dict["StepOccupancy"] = parameterDict 

                parameterDict = {}
                for idx, junction in enumerate(junctions):
                    stress = StressHelper.getStressAt(junction,"vehicleLength")
                    self.junctionsEmissions[idx].append(stress)
                    parameterDict[idx] = stress
                max_dict["vehicleLength"] = parameterDict 

                parameterDict = {}
                for idx, junction in enumerate(junctions):
                    stress = StressHelper.getStressAt(junction,"waitingTime")
                    self.junctionsEmissions[idx].append(stress)
                    parameterDict[idx] = stress
                max_dict["waitingTime"] = parameterDict 

                #max dict is now having all values 
                #Now normalize 
                max_dict["haltingNumber"] = StressHelper.normalise(max_dict["haltingNumber"])
                max_dict["CO2Emissions"] = StressHelper.normalise(max_dict["CO2Emissions"])
                max_dict["StepOccupancy"] = StressHelper.normalise(max_dict["StepOccupancy"])
                max_dict["vehicleLength"] = StressHelper.normalise(max_dict["vehicleLength"])
                max_dict["waitingTime"] = StressHelper.normalise(max_dict["waitingTime"])

                for edge in max_dict["CO2Emissions"]:
                    max_list[edge] = 0
                
                for param in max_dict: 
                    dict = max_dict[param]
                    for edge in dict: 
                        max_list[edge] +=  weights[param] * dict[edge]
                        
                weighted_values = [] 
                for key in max_list: 
                    weighted_values.append((int(key),double(max_list[key]))) 

                    
                max_list = weighted_values
                max_list = sorted(max_list,key = lambda x:x[1])
                max_list.reverse()

                steps.append(step)

                for i in range(locs):
                    traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
                    if junctions[max_list[i][0]].getID() in stressedCounts.keys():
                        stressedCounts[junctions[max_list[i][0]].getID()]+=1
                    else:
                        stressedCounts[junctions[max_list[i][0]].getID()]=1
                
                filename = self.outPath+'stress/screenshots/00'+str(step)+'.jpg'
                traci.gui.screenshot('View #0', filename)
            
            step += 1

        # Printing the values found
        traci.poi.setType('index', 'Aggregate')
        max_stressed = sorted(stressedCounts.items(), key= lambda x:x[1])
        max_stressed.reverse()
        
        for i in range(locs):
            traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
        
        f = open(self.pathSummaryFile, 'w')
        for i in range(locs):
            traci.gui.toggleSelection(max_stressed[i][0], objType='junction')
            x,y = traci.junction.getPosition(max_stressed[i][0])
            lon, lat = traci.simulation.convertGeo(x, y)
            lon, lat = self.net.convertXY2LonLat(x, y)
            f.write(str(max_stressed[i][0])+" Coordinates:" + str(lat) + " " + str(lon) + '\n')
        f.close()

        filename = self.outPath+'stress/screenshots/aggregate.jpg'
        traci.simulationStep()
        traci.gui.screenshot('View #0', filename)   
        traci.simulationStep()
        traci.close()

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
        traci.start([sumoBinary, "-c", self.pathCFG, "--tripinfo-output", self.outPath + "tripinfo.xml", "--time-to-teleport", "-1"])
        self.loop()
    
