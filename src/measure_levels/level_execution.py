"""
Class that represents the levels of the execution.

@date:      Jan-2021
@version:   1.0
"""

import locale
from abc import ABC, abstractmethod # abstract class
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  
from shell.shell import Shell # launch shell arguments
from parameters.level_execution_params import LevelExecutionParameters # parameters of program
from errors.level_execution_errors import *
from parameters.topdown_params import TopDownParameters 
from graph.pie_chart import PieChart

class LevelExecution(ABC):
    """ 
    Class that represents the levels of the execution.
     
    Attributes:
        _input_file             : str           ; path to input file with results. 'None' if we must do the analysis

        _output_file            : str           ; path to output file with results. 'None' to don't use
                                                  output file

        _output_scan_file       : str           ; path to output scan file with results computed by Nvidia Scan tool. 
                                                 'None' to don't use output scan file   

        _program                : str           ; program of the execution

        _collect_metrics        : bool          ; True if the execution must recolted the metrics used by NVIDIA scan tool
                                                  or False in other case

        _compute_capability     : float         ; Compute Capbility of the execution

    """
    
    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool):
        self._program : str = program
        self._output_file : str = output_file
        self._collect_metrics : bool = collect_metrics
        self._input_file : str = input_file
        self._output_scan_file : str = output_scan_file
        shell : Shell = Shell()
        compute_capability_str : str = shell.launch_command_show_all("nvcc $DIR_UNTIL_TOPDOWN/TopDownNvidia/src/measure_parts/compute_capability.cu --run", None)
        shell.launch_command("rm -f $DIR_UNTIL_TOPDOWN/TopDownNvidia/src/measure_parts/a.out", None) # delete 'a.out' generated
        if not compute_capability_str:
            raise ComputeCapabilityError
        self._compute_capability : float = float(compute_capability_str)

    @abstractmethod
    def _generate_command(self) -> str:
        """ 
        Generate command of execution with NVIDIA scan tool.

        Returns:
            String with command to be executed
        """

        pass
        

    @abstractmethod
    def set_results(output_command : str): 
        """
        Set results of execution ALREADY DONE. Results are in the argument.
        
        Args:
            output_command : str    ; str with results of execution.
        """

        pass
        

    @abstractmethod
    def run(self, lst_output):
        """
        Makes execution.
        
        Parameters:
            lst_output  : list ; list with results
        """
        
        pass
        

    def _launch(self, command : str) -> str:
        """ 
        Launch NVIDIA scan tool.
        
        Args:
            command : str ; String with command

        Returns:
            String with results.

        Raises:
            ProfilingError  ; raised in case of error reading results from NVIDIA scan tool
        """

        shell : Shell = Shell()
        output_command : str = shell.launch_command_redirect(command, LevelExecutionParameters.C_INFO_MESSAGE_EXECUTION, self.output_scan_file(), True)
        if output_command is None:
            raise ProfilingError
        return output_command  
        
    
    @abstractmethod
    def _get_results(self, lst_output):
        """ 
        Get results of the different parts.

        Parameters:
            lst_output  : list     ; OUTPUT list with results
        """

        pass
        

    def get_device_max_ipc(self) -> float:
        """
        Get Max IPC of device.

        Returns:
            Float with the max IPC supported by GPU
        """

        dict_warps_schedulers_per_cc : dict = dict({3.0: 4, 3.2: 4, 3.5: 4, 3.7: 4, 5.0: 4, 5.2: 4, 5.3: 4, 
            6.0: 2, 6.1: 4, 6.2: 4, 7.0: 4, 7.2: 4, 7.5: 4, 8.0: 1}) 
        dict_ins_per_cycle : dict = dict({3.0: 2, 3.2: 2, 3.5: 2, 3.7: 2, 5.0: 2, 5.2: 2, 5.3: 2, 
            6.0: 2, 6.1: 2, 6.2: 2, 7.0: 1, 7.2: 1, 7.5: 1, 8.0: 1})
        return dict_warps_schedulers_per_cc.get(self._compute_capability)*dict_ins_per_cycle.get(self._compute_capability)
        
    
    def _get_total_value_of_list(self, list_values, computed_as_average : bool) -> float:
        """
        Get total value of list of metric/event.
    
        Args:
            list_values         : list ; list to be computed

            computed_as_average : bool      ; True if you want to obtain total value as average
                                              as the average of the elements as a function of the 
                                              time executed or False if it is the total value per 
                                              increment
        Returns:
            Float with total value of the list
        """
        
        i : int = 0
        total_value : float = 0.0
        value_str : str = ""
        value : float = 0.0
        for value_str in list_values:
            if value_str[len(value_str) - 1] == "%":
                value = float(value_str[0:len(value_str) - 1])
                if computed_as_average:
                    value *= (self._percentage_time_kernel(i)/100.0)
                total_value += value
            else:
                if self._compute_capability > TopDownParameters.C_COMPUTE_CAPABILITY_NVPROF_MAX_VALUE:
                    value = locale.atof(value_str)
                else:
                    value = float(value_str)
                if computed_as_average:
                    value *= (self._percentage_time_kernel(i)/100.0)
                total_value += value
            i += 1
        return total_value
        

    def _get_stalls_of_part(self, dict : dict) -> float:
        """
        Get percent of stalls of the dictionary indicated by argument.

        Args:
            dic :   dict    ; dictionary with stalls of the corresponding part

        Returns:
            A float with percent of stalls of the dictionary indicated by argument.
        """

        total_value : float = 0.0
        for key in dict.keys():
            total_value += self._get_total_value_of_list(dict.get(key), True)
        return total_value
        
    
    def _get_stalls_of_part_per_kernel(self, dict : dict) -> float:
        """
        Get percent of stalls of the dictionary indicated by argument in each kernel.

        Args:
            dic :   dict    ; dictionary with stalls of the corresponding part

        Returns:
            A float with percent of stalls of the dictionary indicated by argument.
        """

        total_value : float = 0.0
        for key in dict.keys():
            total_value += self._get_total_value_of_list(dict.get(key), True)
        return total_value
        

    def collect_metrics(self) -> bool:
        """
        Check if execution must collect NVIDIA's scan tool metrics.

        Returns:
            Boolean with True if it has to collect metrics or False if not
        """

        return self._collect_metrics
        

    def input_file(self) -> str:
        """ 
        Returns path to input file.
        
        Returns: 
            Path to input file or 'None' if it hasn't been specified.
        """
        
        return self._input_file
                

    def output_file(self) -> str:
        """ 
        Returns path to output file.
        
        Returns: 
            Path to output file or 'None' if it hasn't been specified.
        """
        
        return self._output_file
        

    def output_scan_file(self) -> str:
        """ 
        Returns path to output scan file.
        
        Returns: 
            Path to output scan file or 'None' if it hasn't been specified.
        """
        
        return self._output_scan_file
        
 
    @abstractmethod
    def _percentage_time_kernel(self, kernel_number : int) -> float:
        """ 
        Get time percentage in each Kernel based on cycles elapsed metric/event name
        Each kernel measured is an index of dictionaries used by this program.

        Args:
                kernel_number                   : int   ; number of kernel
                
                cycles_elapsed_counter_name     : str   ; name of event/metric to obatin cycles elapsed in kernel
        Raises:
                ElapsedCyclesError      ; cycles elapsed in 'kernel_number' cannot be obtained
        """
        
        
   
    @abstractmethod
    def _create_graph(self) -> PieChart:
        """ 
        Create a graph where figures are going to be saved.

        Returns:
            Referente to PieChart with graph
        """

        pass
        
   
    @abstractmethod
    def _add_graph_data(self, graph : PieChart):
        """ 
        Add data to graph.

        Args:
            graph   : PieChart  ; reference to PieChart where save figures        
        """
        
        pass
        
        
    def showGraph(self):
        """Show graph to show results."""
        
        graph : PieChart = self._create_graph()
        self._add_graph_data(graph)
        graph.show()
        

    def saveGraph(self, file_str : str):
        """ 
        Save graph in file indicated as argument.

        Args:
            file_str    : str   ; path to output file where save fig
        """
        
        graph : PieChart = self._create_graph()
        self._add_graph_data(graph)
        graph.save(file_str)

