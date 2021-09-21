"""
Class with all params of BackEnd class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

class BackEndParameters:

    C_BACK_END_NAME                    : str        = "BACK-END"
    C_BACK_END_DESCRIPTION             : str        = ("It analyzes the parts of the GPU architecture where the BackEnd produces bottleneck,\n"
                                                    + "which leads to IPC losses. In this part, We analyze aspects related to the 'execution' part of\n"
                                                    + "the instructions, in which aspects such as limitations by functional units, memory limits, etc.\n")
    # NVPROF metrics/arguments
    C_BACK_END_NVPROF_L1_METRICS          : str        = ("stall_memory_dependency,stall_constant_memory_dependency,stall_pipe_busy," +
                                                        "stall_memory_throttle,stall_exec_dependency")
    C_BACK_END_NVPROF_L1_EVENTS           : str        = ("")
    
    C_BACK_END_NVPROF_L2_METRICS          : str        = ("stall_memory_dependency,stall_constant_memory_dependency,stall_pipe_busy," +
                                                        "stall_memory_throttle,stall_exec_dependency")
    C_BACK_END_NVPROF_L2_EVENTS           : str        = ("")

    C_BACK_END_NVPROF_L3_METRICS          : str        = ("stall_memory_dependency,stall_constant_memory_dependency,stall_pipe_busy," +
                                                        "stall_memory_throttle,stall_exec_dependency")
    C_BACK_END_NVPROF_L3_EVENTS           : str        = ("")
    
    # NSIGHT metrics
    C_BACK_END_NSIGHT_L1_METRICS          : str        = ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_drain_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," + 
                                                            "smsp__warp_issue_stalled_wait_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct")
    C_BACK_END_NSIGHT_L2_METRICS          : str        = ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_drain_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," + 
                                                            "smsp__warp_issue_stalled_wait_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct")

    C_BACK_END_NSIGHT_L3_METRICS          : str        =    ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_drain_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," + 
                                                            "smsp__warp_issue_stalled_wait_per_warp_active.pct," +
                                                            "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct")
