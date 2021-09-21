"""
Measurements made by the TopDown methodology in Mio throttle.

@date:      Jan-2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from measure_parts.back_memory_bound import BackMemoryBound
from measure_parts.back_memory_bound import BackMemoryBound
from measure_parts.metric_measure import MetricMeasureNsight 
 
class MemoryMioThrottle(BackMemoryBound):
    """Class that defines the ConstantMemoryBound (sub-part of MemoryBound) part."""

    pass
 
class MemoryMioThrottleNsight(MetricMeasureNsight, MemoryMioThrottle):
    """Class that defines the Memory-Bound.MioThrottle part with nsight scan tool."""

    def __init__(self, name : str, description : str, metrics : str):
        """ 
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
         
        """

        super().__init__(name, description, metrics)
        
  
