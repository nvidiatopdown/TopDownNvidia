"""
Class that represents the execution level of nvprof.

@date:      Jul 2021
@version:   1.0
"""

from abc import ABC, abstractmethod # abstract class
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from parameters.level_execution_params import LevelExecutionParameters # parameters of program
from errors.level_execution_errors import *
from measure_levels.level_execution import LevelExecution 
from measure_parts.extra_measure import ExtraMeasureNvprof

class LevelExecutionNvprof(LevelExecution, ABC):
    """ 
    Class that represents the levels of the execution with nvprof scan tool
     
    Attributes:
         _extra_measure      : ExtraMeasureNvprof   ; support measures

        _collect_events    : bool                   ; True if the execution must recolted the events used by NVIDIA scan tool
                                                    or False in other case
    """

    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool, 
    collect_events : bool, extra_measure : ExtraMeasureNvprof):
        self._extra_measure : ExtraMeasureNvprof = extra_measure
        self._collect_events = collect_events
        super().__init__(program, input_file, output_file, output_scan_file, collect_metrics)
        

    def collect_events(self) -> bool:
        """
        Check if execution must collect NVIDIA's scan tool events.

        Returns:
            Boolean with True if it has to collect events or False if not
        """

        return self._collect_events
        

    def extra_measure(self) -> ExtraMeasureNvprof:
        """
        Return ExtraMeasureNvprof part of the execution.

        Returns:
            reference to ExtraMeasureNvprof part of the execution
        """
        
        return self._extra_measure
        

    @abstractmethod
    def run(self, lst_output : list):
        """
        Makes execution.
        
        Parameters:
            lst_output  : list ; list with results
        """
        
        pass
  
    @abstractmethod
    def _generate_command(self) -> str:
        """ 
        Generate command of execution with NVIDIA scan tool.

        Returns:
            String with command to be executed
        """

        pass

    @abstractmethod
    def _get_results(self, lst_output : list):
        """ 
        Get results of the different parts.

        Parameters:
            lst_output              : list     ; OUTPUT list with results
        """

        pass 

    def _add_result_part_to_lst(self, dict_values : dict, dict_desc : dict,
        lst_to_add , isMetric : bool):
        """
        Add results of execution part (FrontEnd, BackEnd...) to list indicated by argument.

        Args:
            dict_values     : dict      ; diccionary with name_metric/event-value elements of the part to
                                          add to 'lst_to_add'

            dict_desc       : dict      ; diccionary with name_metric/event-description elements of the
                                          part to add to 'lst_to_add'

            lst_output      : list ; list where to add all elements
            
            isMetric        : bool      ; True if they are metrics or False if they are events

        Raises:
            MetricNoDefined             ; raised in case you have added an metric that is
                                          not supported or does not exist in the NVIDIA analysis tool
            EventNoDefined              ; raised in case you have added an event that is
                                          not supported or does not exist in the NVIDIA analysis tool
        """

        measure_name : str = "Event"
        measure_desc_title : str = measure_name + " Description"
        measure_desc_title_max_length : int = len(measure_desc_title)
        if isMetric:
            measure_name = "Metric"
            measure_desc_title = measure_name + " Description"
            measure_desc_title_max_length = len(measure_desc_title)
            for key_desc in dict_desc:
                if len(dict_desc.get(key_desc)) > measure_desc_title_max_length:
                    measure_desc_title_max_length = len(dict_desc.get(key_desc))
        measure_name_title : str = measure_name + " Name"
        measure_name_title_max_length : int = len(measure_name_title)
        measure_value_title : str = measure_name + " Value"
        measure_value_title_max_length : int = len(measure_value_title) 
        for key_value in dict_values:
            if len(key_value) > measure_name_title_max_length:
                measure_name_title_max_length = len(key_value)
        measure_name_title_max_length += 10
        measure_desc_title_max_length += 10
        description = "\t\t\t%-*s" % (measure_name_title_max_length , measure_name_title)
        description += "%-*s" % (measure_desc_title_max_length, measure_desc_title)
        description += "%-*s" % (measure_value_title_max_length, measure_value_title)
        line_length : int = len(description) 
        metrics_events_not_average  = LevelExecutionParameters.C_METRICS_AND_EVENTS_NOT_AVERAGE_COMPUTED.split(",")
        total_value : float = 0.0
        value_str : str
        total_value_str : str = ""
        value_measure_str : str
        i : int = 0
        if isMetric:
            metric_name : str
            metric_desc : str
            is_percentage : bool = False
            is_computed_as_average : bool
            total_value_str : str
            for key_value in dict_values:
                if dict_values[key_value][0][len(dict_values[key_value][0]) - 1] == "%":
                    is_percentage = True
                    # In NVIDIA scan tool, the percentages in each kernel are calculated on the total of
                    # each kernel and not on the total of the application
                    if key_value in metrics_events_not_average:
                        raise ComputedAsAverageError(key_value)
                is_computed_as_average = not (key_value in metrics_events_not_average)
                total_value = round(self._get_total_value_of_list(dict_values[key_value], is_computed_as_average),
                    LevelExecutionParameters.C_MAX_NUM_RESULTS_DECIMALS)
                if total_value.is_integer():
                    total_value = int(total_value)
                value_measure_str = str(total_value)
                if is_percentage:
                    value_measure_str += "%"
                    is_percentage = False
                metric_name = key_value
                metric_desc = dict_desc.get(key_value)
                value_str = "\t\t\t%-*s" % (measure_name_title_max_length , metric_name)
                value_str += "%-*s" % (measure_desc_title_max_length , metric_desc)
                value_str += "%-*s" % (len(value_measure_str), value_measure_str)
                if len(value_str) > line_length:
                    line_length = len(value_str)
                if i != len(dict_values) - 1:
                    value_str += "\n"
                total_value_str += value_str
                i += 1
        else:
            event_name : str
            for key_value in dict_values:
                total_value = round(self._get_total_value_of_list(dict_values[key_value], False),
                    LevelExecutionParameters.C_MAX_NUM_RESULTS_DECIMALS)
                if total_value.is_integer():
                    total_value = int(total_value)
                value_measure_str = str(total_value)
                event_name = key_value
                value_str = "\t\t\t%-*s" % (measure_name_title_max_length , event_name)
                value_str += "%-*s" % (measure_desc_title_max_length , "-")
                value_str += "%-*s" % (len(value_measure_str), value_measure_str)
                if len(value_str) > line_length:
                    line_length = len(value_str)
                if i != len(dict_values) - 1:
                    value_str += "\n"
                total_value_str += value_str
                i += 1     
        spaces_length : int = len("\t\t\t")
        line_str : str = "\t\t\t" + f'{"-" * (line_length - spaces_length)}'
        lst_to_add.append("\n" + line_str)
        lst_to_add.append(description)
        lst_to_add.append(line_str)
        lst_to_add.append(total_value_str)
        lst_to_add.append(line_str + "\n")
            

    def _percentage_time_kernel(self, kernel_number : int) -> float:
        """ 
        Get time percentage in each Kernel.
        Each kernel measured is an index of dictionaries used by this program.

        Args:
            kernel_number   : int   ; number of kernel
        """
        
        value_lst : list = self._extra_measure.get_event_value(LevelExecutionParameters.C_CYCLES_ELAPSED_EVENT_NAME_NVPROF)
        if value_lst is None:
            raise ElapsedCyclesError
        value_str : str
        total_value : float = 0.0
        for value_str in value_lst:
            total_value += float(value_str)
        return (float(value_lst[kernel_number])/total_value)*100.0
        

