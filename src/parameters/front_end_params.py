"""
Class with all params of FrontEnd class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

class FrontEndParameters:

    C_FRONT_END_NAME                    : str       = "FRONT-END"
    C_FRONT_END_DESCRIPTION             : str       = ("It analyzes the parts of the GPU architecture where the FrontEnd produces bottlenecks,\n" 
                                                    + "which leads to IPC losses. In this part, aspects related to the fetch of instructions\n"
                                                    + "are analyzed, such as errors in the instruction cache or IPC losses due to thread synchronization.\n")
    # NVPROF metrics/arguments
    C_FRONT_END_NVPROF_L1_METRICS          : str       = ("stall_inst_fetch,stall_sync,stall_other")
    C_FRONT_END_NVPROF_L1_EVENTS           : str       = ("")

    C_FRONT_END_NVPROF_L2_METRICS          : str       = ("stall_inst_fetch,stall_sync,stall_other")
    C_FRONT_END_NVPROF_L2_EVENTS           : str       = ("")

    C_FRONT_END_NVPROF_L3_METRICS          : str       = ("stall_inst_fetch,stall_sync,stall_other")
    C_FRONT_END_NVPROF_L3_EVENTS           : str       = ("")


    # NSIGHT metrics
    C_FRONT_END_NSIGHT_L1_METRICS          : str       = ("smsp__warp_issue_stalled_no_instruction_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_barrier_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_membar_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_dispatch_stall_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_misc_per_warp_active.pct," + 
                                                       "smsp__warp_issue_stalled_branch_resolving_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_sleeping_per_warp_active.pct")

    C_FRONT_END_NSIGHT_L2_METRICS          : str       =("smsp__warp_issue_stalled_no_instruction_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_barrier_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_membar_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_dispatch_stall_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_misc_per_warp_active.pct," + 
                                                       "smsp__warp_issue_stalled_branch_resolving_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_sleeping_per_warp_active.pct")

    C_FRONT_END_NSIGHT_L3_METRICS          : str       = ("smsp__warp_issue_stalled_no_instruction_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_barrier_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_membar_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_dispatch_stall_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_misc_per_warp_active.pct," + 
                                                       "smsp__warp_issue_stalled_branch_resolving_per_warp_active.pct," +
                                                       "smsp__warp_issue_stalled_sleeping_per_warp_active.pct")
