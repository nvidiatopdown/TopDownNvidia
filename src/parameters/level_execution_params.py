"""
Class with parameters used by LevelExecution file
and their subclasses of the hierachy.

@date:      Jul 2021
@version:   1.0
"""

class LevelExecutionParameters:

    C_IPC_METRIC_NAME_NVPROF                            : str       = "ipc"
    C_IPC_METRIC_NAME_NSIGHT                            : str       = "sm__inst_executed.avg.per_cycle_active"

    C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NVPROF      : str       = "warp_execution_efficiency"
    C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT      : str       = "smsp__thread_inst_executed_per_inst_executed.pct"
    
    C_ISSUE_IPC_METRIC_NAME_NVPROF                      : str       = "issued_ipc"
    C_ISSUE_IPC_METRIC_NAME_NSIGHT                      : str       = "sm__inst_issued.avg.per_cycle_active"

    
    C_CYCLES_ELAPSED_EVENT_NAME_NVPROF                  : str       = "elapsed_cycles_sm"
    C_CYCLES_ELAPSED_METRIC_NAME_NSIGHT                 : str       = "sm__cycles_elapsed.sum"

    C_MAX_NUM_RESULTS_DECIMALS                          : int       = 3 # recommended be same with same value definided in TopDownParameters

    C_INFO_MESSAGE_EXECUTION                            : str       = "Making analysis... Wait to results."

    # add here the events and metrics 
    # that will be computed by adding in 
    # each kernel, and not as a function 
    # of the time executed
    C_METRICS_AND_EVENTS_NOT_AVERAGE_COMPUTED           : str       = "inst_issued"
    
    # level_one.py graph's description
    C_LEVEL_ONE_GRAPHS_TITLES                           : list      = ["IPC Degradation", "STALLS on TOTAL"]                   
    
    # level_two.py graph's description
    #C_LEVEL_TWO_GRAPHS_TITLES                           : list
    
    @staticmethod
    def level_two_graphs_titles(front_end_name : str, back_end_name : str) -> str:
        """
        Returns name's of level's two graphs title.
        
        Params:
            front_end_name  : str   ; front-end's name
            back_end_name   : str   ; back-end's name
        """
        return (["IPC Degradation (LEVEL ONE)", "STALLS on TOTAL (LEVEL ONE)", "IPC Degradation on TOTAL (LEVEL TWO)", "STALLS on TOTAL (LEVEL TWO)",
                                                                    "STALLS on " + front_end_name + " (LEVEL TWO)", "STALLS on " + back_end_name  + " (LEVEL TWO)"])
        

