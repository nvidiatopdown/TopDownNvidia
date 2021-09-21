"""
Class with all params of BackEnd.MemoryBound.MioThrottle class
and their subclasses

@date:      Jul 2021
@version:   1.0
"""

class MemoryMioThrottleParameters:

    C_MEMORY_MIO_THROTTLE_NAME                    : str        = "BACK-END.MEMORY-BOUND.MIO-THROTTLE"
    C_MEMORY_MIO_THROTTLE_DESCRIPTION             : str        = ("Collects performance losses caused by MIO (Memory Input/Output) memory system.")
    
    # NSIGHT metrics
    C_MEMORY_MIO_THROTTLE_NSIGHT_METRICS          : str        = ("smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct")
