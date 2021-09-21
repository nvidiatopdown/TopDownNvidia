"""
Class with all params of BackEnd-CoreBound class
and their subclasses

@date:      Jan 2021
@version:   1.0
"""

class BackCoreBoundParameters:

    C_BACK_CORE_BOUND_NAME                    : str        = "BACK-END.CORE-BOUND"
    C_BACK_CORE_BOUND_DESCRIPTION             : str        = ("In this part, the aspects related to CUDA cores that cause bottlenecks and thus performance losses are analyzed.\n"
                                                            + "Some aspects such as the use and availability of the functional units are analyzed.")
    # NVPROF metrics/arguments
    C_BACK_CORE_BOUND_NVPROF_L2_METRICS          : str        = ("stall_pipe_busy")
    C_BACK_CORE_BOUND_NVPROF_L2_EVENTS           : str        = ("")

    C_BACK_CORE_BOUND_NVPROF_L3_METRICS          : str        = ("stall_pipe_busy")
    C_BACK_CORE_BOUND_NVPROF_L3_EVENTS           : str        = ("")

    # NSIGHT metrics
    C_BACK_CORE_BOUND_NSIGHT_L2_METRICS          : str        = ("smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_wait_per_warp_active.pct")
    C_BACK_CORE_BOUND_NSIGHT_L3_METRICS          : str        = ("smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_wait_per_warp_active.pct")