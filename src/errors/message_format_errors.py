"""
Mistakes launched by MessageFormat class 

@date:      Jan 2021
@version:   1.0
"""

class WriteInOutPutFileError(Exception):
    """Exception raised in case of error writing in output file"""
    
    C_ERROR_MESSAGE     : str = "Error writing in output file"

    def __init__(self):
        """Show error message."""
        
        super().__init__(self.C_ERROR_MESSAGE)
        