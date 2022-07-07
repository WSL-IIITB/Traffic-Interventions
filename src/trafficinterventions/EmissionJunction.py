import os
import sys
import optparse
import traci
import sumolib
from sumolib import checkBinary 

"""
    @Class: Main class for emission analysis
"""
class EmissionJunction:

    """
        @Method: Initialising variables and config
    """
    def __init__(self, pathCFG, outPath, pathNET, pathSummaryFile, numLocs, initialPoiLocation = (5064.74,3568.48)):
        
        # Check for Bash Shortcut
        if "SUMO_HOME" in os.environ:
            sys.path.append(os.path.join(
                os.environ["SUMO_HOME"],
                "tools"
            ))
        else:
            sys.exit("Please populate $SUMO_HOME in your .bashrc file.") 

        # Assign all variables
        self.pathCFG = pathCFG 
        self.outPath = outPath 
        self.pathNET = pathNET
        self.pathSummaryFile = pathSummaryFile
        self.numLocs = numLocs
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
        self.net = sumolib.net.readNet(pathNET)
        self.junctions = self.net.getNodes()
        self.junctionsEmissions = []

        for _ in range(len(self.junctions)):
            self.junctionsEmissions.append([])


    """
        @Method: Calculates the sum of CO2 emissions for each lane that pertains to the junction
    """
    def get_emission_at(self, junction):
        tc2e = 0
        incoming_edges = junction.getIncoming()
        outgoing_edges = junction.getOutgoing()
        edges = incoming_edges+outgoing_edges
        for edge in edges:
            lanes = edge.getLanes()
            for lane in lanes:
                lane_id = lane.getID()
                co2 = traci.lane.getCO2Emission(lane_id)
                tc2e+=co2
            
        return tc2e


    """
        @Method: TraCI simulation step and calculation of positions - run in the runSimulation() method
    """
    def loop(self):
        traci.poi.add("index", self.initialPoiLocation[0], self.initialPoiLocation[1], (255,255,255), layer=202.0)
        step = 0

        junctions = self.junctions 
        locs = min(5, self.numLocs)

        junctions_emissions = []
        for i in range(len(junctions)):
            junctions_emissions.append([])

        steps = []
        max_list = []
        max_dict = {}

        while traci.simulation.getMinExpectedNumber() > 0:

            traci.simulationStep()
            traci.poi.setType('index', 'TimeStep = '+str(step))
            
            if step%100 == 0:
                if(step!=0):
                    for i in range(locs):
                        traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
                max_list = []
                max_dict = {}
                
                for idx, junction in enumerate(junctions):
                    emission = self.get_emission_at(junction)
                    junctions_emissions[idx].append(emission)
                    max_dict[idx] = emission

                max_list = sorted(max_dict.items(), key=lambda x:x[1])
                max_list.reverse()

                steps.append(step)
                for i in range(locs):
                    traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
                
                filename = self.outPath+'screenshots/00'+str(step)+'.jpg'
                traci.gui.screenshot('View #0', filename)
            step += 1
        
        # Printing the values found
        traci.poi.setType('index', 'Aggregate')

        total_emissions_dict = {}
        for idx, emission in enumerate(junctions_emissions):
            total_emissions_dict[idx] = sum(emission)
        total_emissions_list = sorted(total_emissions_dict.items(), key= lambda x:x[1])
        total_emissions_list.reverse()

        for i in range(locs):
            traci.gui.toggleSelection(junctions[max_list[i][0]].getID(), objType='junction')
        
        f = open(self.pathSummaryFile, 'w')
        for i in range(locs):
            traci.gui.toggleSelection(junctions[total_emissions_list[i][0]].getID(), objType='junction')
            
            x,y = traci.junction.getPosition(junctions[total_emissions_list[i][0]].getID())
            lon, lat = traci.simulation.convertGeo(x, y)
            lon, lat = self.net.convertXY2LonLat(x, y)
            
            f.write(str(junctions[total_emissions_list[i][0]].getID())+ +" Coordinates:" + str(lat) + " " + str(lon) +  '\n')
        f.close()

        filename = self.outPath+'screenshots/aggregate.jpg'
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
