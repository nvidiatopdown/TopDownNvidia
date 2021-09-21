"""
Class that represents the execution level of nsight

@date:      Jul 2021
@version:   1.0
"""

import locale
from abc import ABC, abstractmethod # abstract class
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from parameters.level_execution_params import LevelExecutionParameters # parameters of program
from errors.level_execution_errors import *
from measure_levels.level_execution import LevelExecution
from measure_parts.extra_measure import ExtraMeasureNsight

class LevelExecutionNsight(LevelExecution, ABC):
    """ 
    Class that represents the levels of the execution with nsight scan tool.
     
    Attributes:
        _extra_measure      : ExtraMeasureNsight  ; support measures

        _collect_events    : bool          ; True if the execution must recolted the events used by NVIDIA scan tool
                                              or False in other case
    """

    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool, 
        extra_measure : ExtraMeasureNsight):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        self._extra_measure : ExtraMeasureNsight = extra_measure
        super().__init__(program, input_file, output_file, output_scan_file, collect_metrics)
        

    def extra_measure(self) -> ExtraMeasureNsight:
        """
        Return ExtraMeasureNsight part of the execution.

        Returns:
            reference to ExtraMeasureNsight part of the execution
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

    def extra_measure(self) -> ExtraMeasureNsight:
        """
        Return ExtraMeasureNsight part of the execution.

        Returns:
            reference to ExtraMeasureNsight part of the execution
        """

        return self._extra_measure
        

    def _add_result_part_to_lst(self, dict_values : dict, dict_desc : dict,
        lst_to_add):
        """
        Add results of execution part (FrontEnd, BackEnd...) to list indicated by argument.

        Args:
            dict_values     : dict      ; diccionary with name_metric/event-value elements of the part to
                                          add to 'lst_to_add'

            dict_desc       : dict      ; diccionary with name_metric/event-description elements of the
                                          part to add to 'lst_to_add'
                                          
            lst_output      : list ; list where to add all elements

        Raises:
            MetricNoDefined             ; raised in case you have added an metric that is
                                          not supported or does not exist in the NVIDIA analysis tool
        """

        # metrics_events_not_average : list = LevelExecutionParameters.C_METRICS_AND_EVENTS_NOT_AVERAGE_COMPUTED.split(",")
        name_max_length : int = len("Metric Name")
        metric_unit_title : str = "Metric Unit"
        unit_max_length : int = len(metric_unit_title)
        metric_value_title : str = "Metric Value"
        for key_value,key_unit in zip(dict_values, dict_desc):
            if len(key_value) > name_max_length:
                name_max_length = len(key_value)
            if len(key_value[0]) > unit_max_length:
                unit_max_length = key_value[0]
        metric_name_length : int = name_max_length + 10
        metric_unit_length : int = unit_max_length + 10
        metric_value_length : int = len(metric_value_title) 
        description : str  = ("\t\t\t%-*s" % (metric_name_length , "Metric Name"))
        description += ("%-*s" % (metric_unit_length , metric_unit_title))
        description += ("%-*s" % (metric_value_length, metric_value_title))
        line_length : int = len(description) 
        
        metrics_events_not_average : list  = LevelExecutionParameters.C_METRICS_AND_EVENTS_NOT_AVERAGE_COMPUTED.split(",")
        total_value : float = 0.0
        value_str : str
        total_value_str : str = ""
        metric_name : str
        metric_unit : str
        i : int = 0 
        for key_value, key_unit in zip(dict_values, dict_desc):
            total_value = round(self._get_total_value_of_list(dict_values[key_value], False),
             LevelExecutionParameters.C_MAX_NUM_RESULTS_DECIMALS)
            if total_value.is_integer():
                total_value = int(total_value)
            value_metric_str = str(total_value)
            metric_name = key_value
            metric_unit = dict_desc.get(key_unit)
            if not metric_unit:
                metric_unit = "-"
            elif metric_unit == "%":
                # In NVIDIA scan tool, the percentages in each kernel are calculated on the total of
                # each kernel and not on the total of the application
                if key_value in metrics_events_not_average:
                    raise ComputedAsAverageError(key_unit)
            value_str = "\t\t\t%-*s" % (metric_name_length, metric_name)
            value_str += "%-*s" % (metric_unit_length, metric_unit)
            value_str += "%-*s" % (len(metric_value_title), value_metric_str) 
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

        value_lst : list = self._extra_measure.get_metric_value(LevelExecutionParameters.C_CYCLES_ELAPSED_METRIC_NAME_NSIGHT)
        if value_lst is None:
            raise ElapsedCyclesError
        value_str : str
        total_value : float = 0.0
        for value_str in value_lst:
            total_value += locale.atof(value_str)
        return (locale.atof(value_lst[kernel_number])/total_value)*100.0
        
