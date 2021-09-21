"""
Measurements made by the TopDown methodology in replay part.

@date:      Jan-2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from abc import ABC # abstract class
from measure_parts.metric_measure import MetricMeasureNsight, MetricMeasureNvprof
from measure_parts.divergence import Divergence

class DivergenceReplay(Divergence, ABC):
    """Class that defines the Divergence.Replay part."""
    
    pass

class DivergenceReplayNsight(MetricMeasureNsight, DivergenceReplay):
    """Class that defines the Divergence.Replay part with nsight scan tool."""

    def __init__(self, name : str, description : str, metrics : str):
        """ 
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
         
        """

        super().__init__(name, description, metrics)
        

class DivergenceReplayNvprof(MetricMeasureNvprof, DivergenceReplay):
    """Class that defines the Divergence.Replay part with nvprof scan tool."""

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
        


