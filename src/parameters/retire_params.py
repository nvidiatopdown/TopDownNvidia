"""
Class with all params of Retire class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from parameters.level_execution_params import LevelExecutionParameters

class RetireParameters:

    C_RETIRE_NAME                    : str       = "RETIRE"
    C_RETIRE_DESCRIPTION             : str       = ("This part collects the performance of the application, considering the efficiency of the WARP.")
    
    # NVPROF metrics/arguments
    C_RETIRE_NVPROF_L1_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NVPROF)
    C_RETIRE_NVPROF_L1_EVENTS           : str       = ("")
    
    C_RETIRE_NVPROF_L2_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NVPROF)
    C_RETIRE_NVPROF_L2_EVENTS           : str       = ("")
    
    C_RETIRE_NVPROF_L3_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NVPROF)
    C_RETIRE_NVPROF_L3_EVENTS           : str       = ("")

    # NSIGHT metrics
    C_RETIRE_NSIGHT_L1_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NSIGHT)
    C_RETIRE_NSIGHT_L2_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NSIGHT)
    C_RETIRE_NSIGHT_L3_METRICS          : str       = (LevelExecutionParameters.C_IPC_METRIC_NAME_NSIGHT)

