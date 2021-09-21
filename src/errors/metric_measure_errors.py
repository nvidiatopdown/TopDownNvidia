"""
Mistakes launched by MetricMeasure class 
and its subclasses in the hierarchy.

@date:      Jan 2021
@version:   1.0
"""

class DataStructuresOfEventError(Exception):
    """Exception raised when an event is defined in a data structure, 
    but not in another that should be."""
    
    C_ERROR_MESSAGE     : str = ("Following event is defined in a data" +
        "structure, but not in another that should be: ")

    def __init__(self, event_name : str):
        """Show error message.
        
        Attributes:
            event_name    : str   ; name of the event that produced the error
        """
        
        super().__init__(self.C_ERROR_MESSAGE + event_name)
    pass

class DataStructuresOfMetricError(Exception):
    """Exception raised when a metric is defined in a data structure, 
    but not in another that should be."""
    
    C_ERROR_MESSAGE     : str = ("Following metric is defined in a data" +
        " structure, but not in another that should be: ")

    def __init__(self, metric_name : str):
        """Show error message.
        
        Attributes:
            metric_name    : str   ; name of the metric that produced the error
        """
        
        super().__init__(self.C_ERROR_MESSAGE + metric_name)
    pass