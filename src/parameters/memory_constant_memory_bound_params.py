"""
Class with all params of BackEnd.MemoryBound.Constant-Memory-Bound class
and their subclasses

@date:      Jan 2021
@version:   1.0
"""

class MemoryConstantMemoryBoundParameters:

    C_MEMORY_CONSTANT_MEMORY_BOUND_NAME                    : str        = "BACK-END.MEMORY-BOUND.CONSTANT-MEMORY-BOUND"
    C_MEMORY_CONSTANT_MEMORY_BOUND_DESCRIPTION             : str        = ("It denotes the performance losses occurring because of immediate constant cache miss.")
    
    # NVPROF metrics/arguments
    C_MEMORY_CONSTANT_MEMORY_BOUND_NVPROF_METRICS          : str        = ("stall_constant_memory_dependency")
    C_MEMORY_CONSTANT_MEMORY_BOUND_NVPROF_EVENTS           : str        = ("")

    # NSIGHT metrics
    C_MEMORY_CONSTANT_MEMORY_BOUND_NSIGHT_METRICS          : str        = ("smsp__warp_issue_stalled_imc_miss_per_warp_active.pct")
