"""
Mistakes launched by LevelExecution class
and its subclasses in the hierarchy.

@date:      Jan 2021
@version:   1.0
"""

class ProfilingError(Exception):
    """Exception raised when NVIDIA scan tool has failed (results not produced)"""
    
    C_ERROR_MESSAGE     : str = "Error with the NVIDIA scan tool (results not generated)"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class MetricNotAsignedToPart(Exception):
    """Exception raised when a metric has not been assigned to any analysis part"""
    
    C_ERROR_MESSAGE     : str = "Following Metric has not been assigned to any analysis part: "

    def __init__(self, metric_name : str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + metric_name)
        

class EventNotAsignedToPart(Exception):
    """Exception raised when an event has not been assigned to any analysis part
    
    Attributes:
        event_name    : str   ; name of the event that produced the error
    """
    
    C_ERROR_MESSAGE     : str = "Following event has not been assigned to any analysis part: "

    def __init__(self, event_name : str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + event_name)
        

class MetricNoDefined(Exception):
    """Exception raised when a metric has introduced but does not exist in NVIDIA scan tool.
    
    Attributes:
        metric_name    : str   ; name of the metric that produced the error
    """
    
    C_ERROR_MESSAGE     : str = "Following Metric does not exist in NVIDIA scan tool: "

    def __init__(self, metric_name: str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + metric_name)
        

class EventNoDefined(Exception):
    """Exception raised when a event has introduced but does not exist in NVIDIA scan tool.
    
    Attributes:
        event_name    : str   ; name of the event that produced the error
    """
    
    C_ERROR_MESSAGE     : str = "Error. Following event does not exist in NVIDIA scan tool: "

    def __init__(self, event_name: str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + event_name)
        

class IpcMetricNotDefined(Exception):
    """Exception raised if IPC cannot be obtanied because it was not 
            computed by the NVIDIA scan tool
    """
    
    C_ERROR_MESSAGE     : str = "IPC cannot be obtanied from NVIDIA scan tool (it hasn't computed)"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class RetireIpcMetricNotDefined(Exception):
    """Exception raised if "retire" IPC cannot be obtanied because it was not 
            computed by the NVIDIA scan tool
    """
    
    C_ERROR_MESSAGE     : str = ("Retire IPC cannot be obtanied from NVIDIA scan tool" 
                                + " (it hasn't computed)")

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class MetricDivergenceIpcDegradationNotDefined(Exception):
    """Exception raised when a metric required to calculate the percentage of IPC lost in 
    divergence is not defined.
    
    Attributes:
        metric_name    : str   ; name of the event that produced the error"""
    
    C_ERROR_MESSAGE     : str = ("Following Metric is necessary to calculate the percentage of " +
    "IPC lost in divergence: ")

    def __init__(self, metric_name : str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + metric_name)
        

class ElapsedCyclesError(Exception):
    """Exception raised if cannot obtain the elapsed time in each kernel measured."""
    
    C_ERROR_MESSAGE     : str = "Cannot obtain the elapsed time in kernels measured."

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class ComputedAsAverageError(Exception):
    """Exception raised when a metric or event that is a percentage has been configured
       to be computed as add of elements of each kernel. Must be defined as average
    
    Attributes:
        metric_name    : str   ; name of the event that produced the error"""
    
    C_ERROR_MESSAGE     : str = ("Following metric/event cannot be computed as average in each kernel"
     + " because it's a percentage and must be computed as AVERAGE. Delete it from LevelExecutionParameters: ")

    def __init__(self, metric_name : str):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE + metric_name)
        

class TitleSizeError(Exception):
    """Exception raised if size of graph's title list is less than minimum"""

    C_ERROR_MESSAGE     : str = "Size of graph's title list is too low. Minimum Number: "

    def __init__(self, minimum_graph_num : int):
        """
        Show error message.
        
        Args:
            minimum_graph_num : int ; minimum number of graphs
        """

        super().__init__(self.C_ERROR_MESSAGE + str(minimum_graph_num))
        

class ComputeCapabilityError(Exception):
    """Exception raised if cannot obtain the compute capability"""
    
    C_ERROR_MESSAGE     : str = "Cannot obtain the compute capability"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class MaximumIPCError(Exception):
    """Exception raised if cannot obtain the MAX ipc of GPU"""
    
    C_ERROR_MESSAGE     : str = "Cannot obtain  the MAX ipc of GPU"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class GraphsTitleSizeError(Exception):
    """Exception raised if size of length of titles is incorrect"""
    
    C_ERROR_MESSAGE     : str = "INCORRECT size of titles length"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

