"""
Class with all params of ExtraMeasure class
and their subclasses

@date:      Jan 2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from parameters.level_execution_params import LevelExecutionParameters

class ExtraMeasureParameters:

    C_EXTRA_MEASURE_NAME                    : str      = "EXTRA-MEASURE"
    C_EXTRA_MEASURE_DESCRIPTION             : str      = ("Part with support measures. In this part, we include events/metrics that are not part of any analyzed part.")
    
    # NVPROF metrics/arguments
    C_EXTRA_MEASURE_NVPROF_L1_METRICS          : str      = ("")
    C_EXTRA_MEASURE_NVPROF_L1_EVENTS           : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_EVENT_NAME_NVPROF)
    
    C_EXTRA_MEASURE_NVPROF_L2_METRICS          : str      = ("")
    C_EXTRA_MEASURE_NVPROF_L2_EVENTS           : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_EVENT_NAME_NVPROF)

    C_EXTRA_MEASURE_NVPROF_L3_METRICS          : str      = ("")
    C_EXTRA_MEASURE_NVPROF_L3_EVENTS           : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_EVENT_NAME_NVPROF)
    
    # NSIGHT metrics
    C_EXTRA_MEASURE_NSIGHT_L1_METRICS          : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_METRIC_NAME_NSIGHT)
    C_EXTRA_MEASURE_NSIGHT_L2_METRICS          : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_METRIC_NAME_NSIGHT)
    C_EXTRA_MEASURE_NSIGHT_L3_METRICS          : str      = (LevelExecutionParameters.C_CYCLES_ELAPSED_METRIC_NAME_NSIGHT + ",sm__cycles_active.avg,sm__inst_executed.avg, sm__sass_average_branch_targets_threads_uniform.pct")

