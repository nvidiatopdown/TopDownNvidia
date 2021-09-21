"""
Measurements made by the TopDown methodology in (memory) L1 bound.

@date:      Jul 2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from measure_parts.back_memory_bound import BackMemoryBound
from measure_parts.back_memory_bound import BackMemoryBound
from measure_parts.metric_measure import MetricMeasureNsight
 
class MemoryL1Bound(BackMemoryBound):
    """Class that defines the L1 Bound (sub-part of MemoryBound) part."""

    pass
 
class MemoryL1BoundNsight(MetricMeasureNsight, MemoryL1Bound):
    """Class that defines the Memory-Bound.L1Bound part with nsight scan tool."""

    def __init__(self, name : str, description : str, metrics : str):
        """ 
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
         
        """

        super().__init__(name, description, metrics)
        
  
