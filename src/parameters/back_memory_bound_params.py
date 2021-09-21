"""
Class with all params of BackMEMORY_BOUND-MemoryBound class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

class BackMemoryBoundParameters:

    C_BACK_MEMORY_BOUND_NAME                    : str        = "BACK-END.MEMORY-BOUND"
    C_BACK_MEMORY_BOUND_DESCRIPTION             : str        = ("It analyzes the parts of the GPU architecture where we have a loss of performance (IPC) due to\n"
                                                                + "memory bounds. This part takes into account aspects such as data dependencies, failures or access\n"
                                                                + "limits in caches.")
    # NVPROF metrics/arguments 
    C_BACK_MEMORY_BOUND_NVPROF_L2_METRICS          : str        =  ("stall_memory_dependency,stall_constant_memory_dependency,stall_memory_throttle")
    C_BACK_MEMORY_BOUND_NVPROF_L2_EVENTS           : str        = ("")

    C_BACK_MEMORY_BOUND_NVPROF_L3_METRICS          : str        =  ("stall_memory_dependency,stall_constant_memory_dependency,stall_memory_throttle")
    C_BACK_MEMORY_BOUND_NVPROF_L3_EVENTS           : str        = ("")

    # NSIGHT metrics
    C_BACK_MEMORY_BOUND_NSIGHT_L2_METRICS          : str        =  ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," + 
                                                                    "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_drain_per_warp_active.pct")
    C_BACK_MEMORY_BOUND_NSIGHT_L3_METRICS          : str        = ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," + 
                                                                    "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," +
                                                                    "smsp__warp_issue_stalled_drain_per_warp_active.pct")
