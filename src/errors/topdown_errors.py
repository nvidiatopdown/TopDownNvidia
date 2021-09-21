"""
Mistakes launched by TopDown class

@date:      Jan 2021
@version:   1.0
"""

class ComputeCapabilityNumberError(Exception):
    """Exception raised when the Compute Capability of Decive is out of range.
    
    Attributes:
        event_name    : str   ; name of the event that produced the error
    """
    
    C_ERROR_MESSAGE     : str = "Error with the Compute Capability value obtained"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

class ModeExecutionError(Exception):
    """Exception raised when compute capability of (current) device cannot be obtained
    
    Attributes:
        event_name    : str   ; name of the event that produced the error
    """
    
    C_ERROR_MESSAGE     : str = "Error obtaining Compute Capability of current device"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        

