"""
Class that represents the level one of the execution with nsight scan tool.

@date:      Jul 2021
@version:   1.0
"""


import re
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from measure_levels.level_one import LevelOne 
from measure_levels.level_execution_nsight import LevelExecutionNsight
from measure_parts.front_end import FrontEndNsight
from measure_parts.back_end import BackEndNsight
from measure_parts.divergence import DivergenceNsight
from measure_parts.retire import RetireNsight
from measure_parts.extra_measure import ExtraMeasureNsight
from show_messages.message_format import MessageFormat
from errors.level_execution_errors import *
from parameters.level_execution_params import LevelExecutionParameters

class LevelOneNsight(LevelOne, LevelExecutionNsight):
    """ 
    Class thath represents the level one of the execution with nsight scan tool.

    Attributes:
        _front_end      : FrontEnd      ; FrontEnd part of the execution

        _back_end       : BackEnd       ; BackEnd part of the execution

        _divergence     : Divergence    ; Divergence part of the execution

        _retire         : Retire        ; Retire part of the execution
    """

    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool, front_end : FrontEndNsight, 
        back_end : BackEndNsight, divergence : DivergenceNsight, retire : RetireNsight, extra_measure : ExtraMeasureNsight):

        self._front_end : FrontEndNsight = front_end
        self._back_end  : BackEndNsight = back_end
        self._divergence : DivergenceNsight = divergence
        self._retire : RetireNsight = retire
        super().__init__(program, input_file, output_file, output_scan_file, collect_metrics, extra_measure)
        

    def _generate_command(self) -> str:
        """ 
        Generate command of execution with NVIDIA scan tool.

        Returns:
            String with command to be executed
        """
        
        command : str = ("ncu --target-processes all --metrics " + self._front_end.metrics_str() + 
            "," + self._back_end.metrics_str() + "," + self._divergence.metrics_str() + "," + self._extra_measure.metrics_str() +
            "," + self._retire.metrics_str() + " "+  str(self._program))
        return command
        

    def front_end(self) -> FrontEndNsight:
        """
        Return FrontEndNsight part of the execution.

        Returns:
            reference to FrontEndNsight part of the execution
        """

        return self._front_end
        
    
    def back_end(self) -> BackEndNsight:
        """
        Return BackEndNsight part of the execution.

        Returns:
            reference to BackEndNsight part of the execution
        """

        return self._back_end
        

    def divergence(self) -> DivergenceNsight:
        """
        Return DivergenceNsight part of the execution.

        Returns:
            reference to DivergenceNsight part of the execution
        """

        return self._divergence
        

    def retire(self) -> RetireNsight:
        """
        Return RetireNsight part of the execution.

        Returns:
            reference to RetireNsight part of the execution
        """

        return self._retire
        

    def _divergence_ipc_degradation(self) -> float:
        """
        Find IPC degradation due to Divergence part

        Returns:
            Float with theDivergence's IPC degradation

        """
        return super()._diver_ipc_degradation(LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT, 
        LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NSIGHT)
        

    def _get_results(self, lst_output : list):
        """
        Get results of the different parts.

        Parameters:
            lst_output              : list     ; OUTPUT list with results
        """

        converter : MessageFormat = MessageFormat()
        #  Keep Results
        if not self._collect_metrics:
            return
        if self._collect_metrics and self._front_end.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._front_end.name()))
            super()._add_result_part_to_lst(self._front_end.metrics(), 
                self._front_end.metrics_description(), lst_output)           
        if self._collect_metrics and self._back_end.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._back_end.name()))
            super()._add_result_part_to_lst(self._back_end.metrics(), 
                self._back_end.metrics_description(), lst_output)  
        if self._collect_metrics and self._divergence.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._back_end.name()))
            super()._add_result_part_to_lst(self._divergence.metrics(), 
                self._divergence.metrics_description(), lst_output)
        if self._collect_metrics and self._retire.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._retire.name()))
            super()._add_result_part_to_lst(self._retire.metrics(), 
                self._retire.metrics_description(), lst_output)
        if self._collect_metrics and self._extra_measure.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._extra_measure.name()))
            super()._add_result_part_to_lst(self._extra_measure.metrics(), 
                self._extra_measure.metrics_description(), lst_output)
        lst_output.append("\n")
        

    def ipc(self) -> float:
        """
        Get IPC of execution.

        Returns:
            float with the IPC
        """

        return super()._get_ipc(LevelExecutionParameters.C_IPC_METRIC_NAME_NSIGHT)
        

    
    def _set_front_back_divergence_retire_results(self, results_launch : str):
        """ Get Results from FrontEnd, BanckEnd, Divergence and Retire parts.
        
        Args:
            results_launch  : str   ; results generated by NVIDIA scan tool
            
        Raises:
            MetricNotAsignedToPart      ; raised when a metric has not been assigned to any analysis part
        """
        
        metric_name : str
        metric_unit : str 
        metric_value : str 
        line : str
        i : int
        list_words : list
        front_end_value_has_found : bool
        frond_end_unit_has_found : bool
        back_end_value_has_found : bool
        back_end_unit_has_found : bool
        divergence_value_has_found : bool
        divergence_unit_has_found : bool
        extra_measure_value_has_found : bool
        extra_measure_unit_has_found : bool
        retire_value_has_found : bool 
        retire_unit_has_found : bool
        can_read_results : bool = False
        for line in str(results_launch).splitlines():
            line = re.sub(' +', ' ', line) # delete more than one spaces and put only one
            list_words = line.split(" ")
            # Check if it's line of interest:
            # ['', 'metric_name','metric_unit', 'metric_value']
            if not can_read_results:
                if list_words[0] == "==PROF==" and list_words[1] == "Disconnected":
                        can_read_results = True
                continue
            if (len(list_words) == 4 or len(list_words) == 3) and list_words[1][0] != "-":
                if len(list_words) == 3: 
                    metric_name = list_words[1]
                    metric_unit = ""
                    metric_value = list_words[2]   
                else:
                    metric_name = list_words[1]
                    metric_unit = list_words[2]
                    metric_value = list_words[3]
   
                front_end_value_has_found = self._front_end.set_metric_value(metric_name, metric_value)
                frond_end_unit_has_found = self._front_end.set_metric_unit(metric_name, metric_unit)
                back_end_value_has_found = self._back_end.set_metric_value(metric_name, metric_value)
                back_end_unit_has_found = self._back_end.set_metric_unit(metric_name, metric_unit)
                divergence_value_has_found = self._divergence.set_metric_value(metric_name, metric_value)
                divergence_unit_has_found = self._divergence.set_metric_unit(metric_name, metric_unit)
                extra_measure_value_has_found = self._extra_measure.set_metric_value(metric_name, metric_value)
                extra_measure_unit_has_found = self._extra_measure.set_metric_unit(metric_name, metric_unit)
                retire_value_has_found = self._retire.set_metric_value(metric_name, metric_value)
                retire_unit_has_found = self._retire.set_metric_unit(metric_name, metric_unit)
                if (not (front_end_value_has_found or back_end_value_has_found or divergence_value_has_found or 
                    extra_measure_value_has_found or retire_value_has_found) or 
                    not(frond_end_unit_has_found or back_end_unit_has_found 
                    or divergence_unit_has_found or extra_measure_unit_has_found or retire_unit_has_found)):
                    raise MetricNotAsignedToPart(metric_name)
        

    def retire_ipc(self) -> float:
        """
        Get "RETIRE" IPC of execution.

        Raises:
            RetireIpcMetricNotDefined ; raised if retire IPC cannot be obtanied because it was not 
            computed by the NVIDIA scan tool.
        """

        return super()._ret_ipc(LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NSIGHT)
        
