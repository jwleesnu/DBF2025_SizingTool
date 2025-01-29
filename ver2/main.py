import cProfile
import pstats
import pandas as pd
from pstats import SortKey
from vsp_grid import runVSPGridAnalysis
from mission_grid import runMissionGridSearch, ResultAnalysis
from vsp_analysis import  loadAnalysisResults, visualize_results, resetAnalysisResults, removeAnalysisResults
from mission_analysis import MissionAnalyzer, visualize_mission
from internal_dataclass import *
from setup_dataclass import *

def main():

    removeAnalysisResults(csvPath = "data/test.csv")
    removeAnalysisResults(csvPath = "data/total_results.csv")
    removeAnalysisResults(csvPath = "data/organized_results.csv")

    presetValues = PresetValues(
        m_x1 = 0.25,                        # kg
        x1_flight_time = 30,                # sec
        
        throttle_takeoff = 0.9,             # 0~1
        max_climb_angle=40,                 #deg
        max_load = 30,                      # kg
        h_flap_transition = 5,              # m
        
        number_of_motor = 2,                 
        max_battery_capacity = 2250,        # mAh (per one battery)
        min_battery_voltage = 21.8,         # V 
        propulsion_efficiency = 0.1326,     # Efficiency of the propulsion system
        score_weight_ratio = 0.5            # mission2/3 score weight ratio
        )
    
    propulsionSpecs = PropulsionSpecs(
        M2_propeller_data_path = "data/propDataCSV/PER3_8x6E.csv",
        M3_propeller_data_path = "data/propDataCSV/PER3_8x6E.csv",
        battery_data_path = "data/batteryDataCSV/Maxamps_2250mAh_6S.csv",
        Kv = 109.91,
        R = 0.062,
        number_of_battery = 2,
        n_cell = 6,
        battery_Wh = 49.95,
        max_current = 60,
        max_power = 1332    
    )
    
    aircraftParamConstraints = AircraftParamConstraints (
        #Constraints for constructing the aircraft

        m_total_min = 8500.0,                # g
        m_total_max = 8500.0,
        m_total_interval = 500.0,
        
        # wing parameter ranges
        span_min = 1800.0,                   # mm
        span_max = 1800.0,                   
        span_interval = 100.0,
    
        AR_min = 5.45,                  
        AR_max = 5.45,
        AR_interval = 0.5,
        
        taper_min = 0.45,
        taper_max = 0.55,                      
        taper_interval = 0.1,
        
        twist_min = 0.0,                     # degree
        twist_max = 0.0,                     
        twist_interval = 1.0,

        # wing loading limit
        wing_loading_min = 5,
        wing_loading_max = 15
        )
    
    baseAircraft = Aircraft(
        m_total = 8500, 
        m_fuselage = 3000,

        wing_density = 0.0000852, spar_density = 1.0,

        mainwing_span = 1800,        
        mainwing_AR = 5.45,           
        mainwing_taper = 0.65,        
        mainwing_twist = 0.0,        
        mainwing_sweepback = 0,   
        mainwing_dihedral = 5.0,     
        mainwing_incidence = 2.0,    

        flap_start = [0.05, 0.4],            
        flap_end = [0.25, 0.6],              
        flap_angle = [20.0, 15.0],           
        flap_c_ratio = [0.35, 0.35],         

        horizontal_volume_ratio = 0.7,
        horizontal_area_ratio = 0.25, 
        horizontal_AR = 4.0,         
        horizontal_taper = 1,      
        horizontal_ThickChord = 8,

        vertical_volume_ratio = 0.053,
        vertical_taper = 0.6,        
        vertical_ThickChord = 9  
        )

    runVSPGridAnalysis(aircraftParamConstraints,presetValues,baseAircraft)

    results = pd.read_csv("data/test.csv", sep='|', encoding='utf-8')
    print(results.head()) 

    for hashVal in results["hash"]:
        print(f"\nAnalyzing for hash{hashVal}")

        missionParamConstraints = MissionParamConstraints (
            
            M2_max_speed_min = 35,
            M2_max_speed_max = 35,
            M3_max_speed_min = 20,
            M3_max_speed_max = 20,
            max_speed_analysis_interval = 5,
            
            #Constraints for calculating mission2
            M2_throttle_climb_min = 0.9,
            M2_throttle_climb_max = 0.9,
            M2_throttle_turn_min = 0.5,
            M2_throttle_turn_max = 0.5,
            M2_throttle_level_min = 0.5,
            M2_throttle_level_max = 0.5,
            M2_throttle_analysis_interval = 0.05,

            #Constraints for calculating mission3  
            M3_throttle_climb_min = 0.9,
            M3_throttle_climb_max = 0.9,
            M3_throttle_turn_min = 0.6,
            M3_throttle_turn_max = 0.6,
            M3_throttle_level_min = 0.6,
            M3_throttle_level_max = 0.6,
            M3_throttle_analysis_interval = 0.05
            )
        
        runMissionGridSearch(hashVal,presetValues,missionParamConstraints,propulsionSpecs)
          
    
    ResultAnalysis(presetValues)

    return


if __name__== "__main__":
    main()
