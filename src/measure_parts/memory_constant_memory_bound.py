"""
Measurements made by the TopDown methodology in (memory) constant memory part.

@date:      Jul 2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from measure_parts.back_memory_bound import BackMemoryBound
from measure_parts.metric_measure import MetricMeasureNsight, MetricMeasureNvprof
 
class MemoryConstantMemoryBound(BackMemoryBound):
    """Class that defines the ConstantMemoryBound (sub-part of MemoryBound) part."""

    pass
 
class MemoryConstantMemoryBoundNsight(MetricMeasureNsight, MemoryConstantMemoryBound):
    """Class that defines the Core-Bound.ConstantMemoryBound part with nsight scan tool."""

    def __init__(self, name : str, description : str, metrics : str):
        """ 
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
         
        """

        super().__init__(name, description, metrics)
        

class MemoryConstantMemoryBoundNvprof(MetricMeasureNvprof, MemoryConstantMemoryBound):
    """Class that defines the Core-Bound.ConstantMemoryBound part with nvprof scan tool."""

    def __init__(self, name : str, description : str, metrics : str, events : str):
        """ 
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
        
            events              : str   ;   string with events
        """

        super().__init__(name, description, metrics, events)
        

  
