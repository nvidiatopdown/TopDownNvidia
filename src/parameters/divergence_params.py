"""
Class with all params of Divergence class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from parameters.level_execution_params import LevelExecutionParameters

class DivergenceParameters:

    C_DIVERGENCE_NAME                    : str      = "DIVERGENCE"
    C_DIVERGENCE_DESCRIPTION             : str      = ("Includes performance losses caused by conditional branches (in which warp is not " +
                                                        "generally not fully exploited) and repetition of instructions.")
    # NVPROF metrics/arguments
    C_DIVERGENCE_NVPROF_L1_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NVPROF + "," + 
                                                        LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NVPROF)
    C_DIVERGENCE_NVPROF_L1_EVENTS           : str      = ("")
    
    C_DIVERGENCE_NVPROF_L2_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NVPROF + "," + 
                                                        LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NVPROF)
    C_DIVERGENCE_NVPROF_L2_EVENTS           : str      = ("")

    C_DIVERGENCE_NVPROF_L3_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NVPROF + "," + 
                                                        LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NVPROF)
    C_DIVERGENCE_NVPROF_L3_EVENTS           : str      = ("")

    # NSIGHT metrics
    C_DIVERGENCE_NSIGHT_L1_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT + 
                                                      "," + LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NSIGHT)
    C_DIVERGENCE_NSIGHT_L2_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT + 
                                                      "," + LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NSIGHT)
    C_DIVERGENCE_NSIGHT_L3_METRICS          : str      = (LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT + 
                                                      "," + LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NSIGHT)

