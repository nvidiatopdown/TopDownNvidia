"""
Class with all params of FrontEnd-Decode class
and their subclasses

@date:      Jan 2021
@version:   1.0
"""

class FrontDecodeParameters:

    C_FRONT_DECODE_NAME                    : str       = "FRONT-END.DECODE"
    C_FRONT_DECODE_DESCRIPTION             : str       = ("Includes the loss of performance caused by crashes due to not being" + 
                                                            "able to do the DECODE of the operations.")
    
    # NVPROF metrics/arguments
    C_FRONT_DECODE_NVPROF_L2_METRICS          : str       = ("stall_other")
    C_FRONT_DECODE_NVPROF_L2_EVENTS           : str       = ("")

    C_FRONT_DECODE_NVPROF_L3_METRICS          : str       = ("")
    C_FRONT_DECODE_NVPROF_L3_EVENTS           : str       = ("")
    
    # NSIGHT metrics
    C_FRONT_DECODE_NSIGHT_L2_METRICS          : str       = ("smsp__warp_issue_stalled_dispatch_stall_per_warp_active.pct," +
                                                                 "smsp__warp_issue_stalled_misc_per_warp_active.pct")
    C_FRONT_DECODE_NSIGHT_L3_METRICS          : str       = ("smsp__warp_issue_stalled_dispatch_stall_per_warp_active.pct," +  
                                                                 "smsp__warp_issue_stalled_misc_per_warp_active.pct")

