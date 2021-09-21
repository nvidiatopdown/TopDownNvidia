"""
Class with all params of FrontEnd-Fetch class
and their subclasses.

@date:      Jul 2021
@version:   1.0
"""

class FrontFetchParameters:

    C_FRONT_FETCH_NAME                    : str       = "FRONT-END.FETCH"
    C_FRONT_FETCH_DESCRIPTION             : str       = ("Includes the loss of performance caused by crashes due to not being" + 
                                                            "able to do the FETCH of the operations.")

    # NVPROF metrics/arguments
    C_FRONT_FETCH_NVPROF_L2_METRICS          : str       = ("stall_inst_fetch,stall_sync")
    C_FRONT_FETCH_NVPROF_L2_EVENTS           : str       = ("")
    
    C_FRONT_FETCH_NVPROF_L3_METRICS          : str       = ("stall_inst_fetch,stall_sync")
    C_FRONT_FETCH_NVPROF_L3_EVENTS           : str       = ("")
    
    # NSIGHT metrics
    C_FRONT_FETCH_NSIGHT_L2_METRICS          : str       = ("smsp__warp_issue_stalled_no_instruction_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_barrier_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_membar_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_branch_resolving_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_sleeping_per_warp_active.pct")
    C_FRONT_FETCH_NSIGHT_L3_METRICS          : str       = ("smsp__warp_issue_stalled_no_instruction_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_barrier_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_membar_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_branch_resolving_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_sleeping_per_warp_active.pct")
