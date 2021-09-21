"""
Class with all params of BackEnd.MemoryBound.L1Bound class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

class MemoryL1BoundParameters:

    C_MEMORY_L1_BOUND_NAME                    : str        = "BACK-END.MEMORY-BOUND.L1-BOUND"
    C_MEMORY_L1_BOUND_DESCRIPTION             : str        = ("Collect performance losses caused by some aspects of the L1 cache.")
    
    # NSIGHT metrics
    C_MEMORY_L1_BOUND_NSIGHT_METRICS          : str        = ("smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," +
                                                                "smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct")