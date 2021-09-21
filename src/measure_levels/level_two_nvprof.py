"""
Class that represents the level two of the execution with nvprof scan tool.

@date:      Jul 2021
@version:   1.0
"""

import re
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1, parentdir) 
from measure_levels.level_one_nvprof import LevelOneNvprof
from measure_parts.back_core_bound import BackCoreBoundNvprof
from measure_parts.back_memory_bound import BackMemoryBoundNvprof
from measure_parts.front_decode import FrontDecodeNvprof
from measure_parts.front_fetch import FrontFetchNvprof
from measure_parts.divergence_replay import DivergenceReplayNvprof
from measure_parts.divergence_branch import DivergenceBranchNvprof
from measure_parts.front_end import FrontEndNvprof
from measure_parts.back_end import BackEndNvprof
from measure_parts.divergence import DivergenceNvprof
from measure_parts.retire import RetireNvprof
from measure_parts.extra_measure import ExtraMeasureNvprof
from measure_levels.level_two import LevelTwo
from show_messages.message_format import MessageFormat
from errors.level_execution_errors import *
from parameters.divergence_replay_params import DivergenceReplayParameters
from parameters.divergence_branch_params import DivergenceBranchParameters
from parameters.level_execution_params import LevelExecutionParameters

class LevelTwoNvprof(LevelTwo, LevelOneNvprof):
    """
    Class with level two of the execution based on NVPROF scan tool
    
    Atributes:
        _back_memory_bound      : BackMemoryBoundNvprof     ; backs' memory bound part

        _back_core_bound        : BackCoreBoundNvprof       ; backs' core bound part

        _front_decode           : FrontDecodeNvprof         ; front's decode part

        _front_fetch            : FrontFetchNvprof          ; front's fetch part

        _branch_divergence      : DivergenceBranchNvprof    ; divergence's branch part

        _replay_divergence      : DivergenceReplayNvprof    ; divergence's replay part
    """

    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool, collect_events : bool,
        front_end : FrontEndNvprof, back_end : BackEndNvprof, divergence : DivergenceNvprof, retire : RetireNvprof, 
        extra_measure : ExtraMeasureNvprof, front_decode : FrontDecodeNvprof, front_fetch : FrontFetchNvprof, 
        back_core_bound : BackCoreBoundNvprof, back_memory_bound : BackMemoryBoundNvprof):
        
        self._back_core_bound : BackCoreBoundNvprof = back_core_bound
        self._back_memory_bound : BackMemoryBoundNvprof = back_memory_bound
        self._front_decode : FrontDecodeNvprof = front_decode
        self._front_fetch : FrontFetchNvprof = front_fetch
        self._branch_divergence : DivergenceBranchNvprof = DivergenceBranchNvprof(DivergenceBranchParameters.C_DIVERGENCE_BRANCH_NAME, DivergenceBranchParameters.C_DIVERGENCE_BRANCH_DESCRIPTION, "", "")
        self._replay_divergence : DivergenceReplayNvprof = DivergenceReplayNvprof(DivergenceReplayParameters.C_DIVERGENCE_REPLAY_NAME, DivergenceReplayParameters.C_DIVERGENCE_REPLAY_DESCRIPTION, "", "")
        super().__init__(program, input_file, output_file, output_scan_file, collect_metrics, collect_events, front_end, back_end, divergence, retire, extra_measure)
        

    def divergence_replay(self) -> DivergenceReplayNvprof:
        """
        Return Replay part of the execution.
 
        Returns:
            reference to CoreBound part of the execution
        """
 
        return self._replay_divergence
        
 
 
    def divergence_branch(self) -> DivergenceBranchNvprof:
        """
        Return Replay part of the execution.
 
        Returns:
            reference to CoreBound part of the execution
        """
        
        return self._branch_divergence        
        

    def back_core_bound(self) -> BackCoreBoundNvprof:
        """
        Return CoreBound part of the execution.

        Returns:
            reference to CoreBound part of the execution
        """
        
        return self._back_core_bound
        

    def back_memory_bound(self) -> BackMemoryBoundNvprof:
        """
        Return MemoryBound part of the execution.

        Returns:
            reference to MemoryBoundNvprof part of the execution
        """
        
        return self._back_memory_bound
        

    def front_decode(self) -> FrontDecodeNvprof:
        """
        Return FrontDecode part of the execution.

        Returns:
            reference to FrontDecodeNvprof part of the execution
        """
        
        return self._front_decode
        

    def front_fetch(self) -> FrontFetchNvprof:
        """
        Return FrontFetch part of the execution.

        Returns:
            reference to FrontFetchNvprof part of the execution
        """
        
        return self._front_fetch
        

    def _generate_command(self) -> str:
        """ 
        Generate command of execution with NVIDIA scan tool.

        Returns:
            String with command to be executed
        """
        command : str = ("nvprof --metrics " + self._front_end.metrics_str() + "," + self._back_end.metrics_str() + 
            "," + self._divergence.metrics_str() + "," + self._extra_measure.metrics_str() + "," + self._retire.metrics_str() + 
            "," + self._front_decode.metrics_str() + "," + self._front_fetch.metrics_str() + "," + 
            self._back_core_bound.metrics_str() + "," + self._back_memory_bound.metrics_str() + "  --events " + 
            self._front_end.events_str() + "," + self._back_end.events_str() + "," + self._divergence.events_str() +  "," + 
            self._extra_measure.events_str() + "," + self._retire.events_str() + "," +  self._front_decode.events_str() + 
            "," + self._front_fetch.events_str() + "," + self._back_core_bound.events_str() + "," + self._back_memory_bound.events_str() + 
            " --unified-memory-profiling off " + self._program)
        return command
        

    def _get_results(self, lst_output : list):
        """ 
        Get results of the different parts.

        Parameters:
            lst_output              : list     ; OUTPUT list with results
        """

        #  Keep Results
        converter : MessageFormat = MessageFormat()

        if not self._collect_metrics and not self._collect_events:
            return
        if (self._collect_metrics and self._front_end.metrics_str() != "" or 
            self._collect_events and self._front_end.events_str() != ""):
            lst_output.append(converter.underlined_str(self._front_end.name()))
        if self._collect_metrics and self._front_end.metrics_str() != "":
            super()._add_result_part_to_lst(self._front_end.metrics(), 
                self._front_end.metrics_description(), lst_output, True)
        if self._collect_events and self._front_end.events_str() != "":
                super()._add_result_part_to_lst(self._front_end.events(), 
                self._front_end.events_description(), "", lst_output, False)
        if (self._collect_metrics and self._front_decode.metrics_str() != "" or 
            self._collect_events and self._front_decode.events_str() != ""):
            lst_output.append(converter.underlined_str(self._front_decode.name()))
        if  self._collect_metrics and self._front_decode.metrics_str() != "":
            super()._add_result_part_to_lst(self._front_decode.metrics(), 
                self._front_decode.metrics_description(), lst_output, True)
        if self._collect_events and self._front_decode.events_str() != "":
                super()._add_result_part_to_lst(self._front_decode.events(), 
                self._front_decode.events_description(), lst_output, False)
        if (self._collect_metrics and self._front_fetch.metrics_str() != "" or 
            self._collect_events and self._front_fetch.events_str() != ""):
            lst_output.append(converter.underlined_str(self._front_fetch.name()))
        if self._collect_metrics and self._front_fetch.metrics_str() != "":
            super()._add_result_part_to_lst(self._front_fetch.metrics(), 
                self._front_fetch.metrics_description(), lst_output, True)
        if self._collect_events and self._front_fetch.events_str() != "":
                super()._add_result_part_to_lst(self._front_fetch.events(), 
                self._front_fetch.events_description(), lst_output, False)
        if (self._collect_metrics and self._back_end.metrics_str() != "" or 
            self._collect_events and self._back_end.events_str() != ""):
            lst_output.append(converter.underlined_str(self._back_end.name()))
        if self._collect_metrics and self._back_end.metrics_str() != "":
            super()._add_result_part_to_lst(self._back_end.metrics(), 
                self._back_end.metrics_description(), lst_output, True)        
        if self._collect_events and self._back_end.events_str() != "":
                super()._add_result_part_to_lst(self._back_end.events(), 
                self._back_end.events_description(), lst_output, False)
        if (self._collect_metrics and self._back_core_bound.metrics_str() != "" or 
            self._collect_events and self._back_core_bound.events_str() != ""):
            lst_output.append(converter.underlined_str(self._back_core_bound.name()))
        if self._collect_metrics and self._back_core_bound.metrics_str() != "":
            super()._add_result_part_to_lst(self._back_core_bound.metrics(), 
                self._back_core_bound.metrics_description(), lst_output, True)
        if self._collect_events and self._back_core_bound.events_str() != "":
                super()._add_result_part_to_lst(self._back_core_bound.events(), 
                self._back_core_bound.events_description(), lst_output, False) 
        if (self._collect_metrics and self._back_memory_bound.metrics_str() != "" or 
            self._collect_events and self._back_memory_bound.events_str() != ""):
            lst_output.append(converter.underlined_str(self._back_memory_bound.name()))
        if self._collect_metrics and self._back_memory_bound.metrics_str() != "":
            super()._add_result_part_to_lst(self._back_memory_bound.metrics(), 
                self._back_memory_bound.metrics_description(), lst_output, True)
        if self._collect_events and self._back_memory_bound.events_str() != "":
                super()._add_result_part_to_lst(self._back_memory_bound.events(), 
                self._back_memory_bound.events_description(), lst_output, False)
        if (self._collect_metrics and self._divergence.metrics_str() != "" or 
            self._collect_events and self._divergence.events_str() != ""):
            lst_output.append(converter.underlined_str(self._divergence.name()))
        if self._collect_metrics and self._divergence.metrics_str() != "":
            super()._add_result_part_to_lst(self._divergence.metrics(), 
                self._divergence.metrics_description(), lst_output, True)
        if self._collect_events and self._divergence.events_str() != "":
                super()._add_result_part_to_lst(self._divergence.events(), 
                self._divergence.events_description(),lst_output, False)
        if (self._collect_metrics and self._retire.metrics_str() != "" or 
            self._collect_events and self._retire.events_str() != ""):
            lst_output.append(converter.underlined_str(self._retire.name()))  
        if self._collect_metrics and  self._retire.metrics_str() != "":
                super()._add_result_part_to_lst(self._retire.metrics(), 
                self._retire.metrics_description(), lst_output, True)
        if self._collect_events and self._retire.events_str() != "":
                super()._add_result_part_to_lst(self._retire.events(), 
                self._retire.events_description(), lst_output, False)
        if (self._collect_metrics and self._extra_measure.metrics_str() != "" or 
            self._collect_events and self._extra_measure.events_str() != ""):
            lst_output.append(converter.underlined_str(self._extra_measure.name()))
        if self._collect_metrics and self._extra_measure.metrics_str() != "":
            super()._add_result_part_to_lst(self._extra_measure.metrics(), 
                self._extra_measure.metrics_description(), lst_output, True)
        if self._collect_events and self._extra_measure.events_str() != "":
                super()._add_result_part_to_lst(self._extra_measure.events(), 
                self._extra_measure.events_description(), lst_output, False)
        lst_output.append("\n")
        
    
    def _set_memory_core_decode_fetch_results(self, results_launch : str):
        """
        Set results of the level two part (that are not level one).
        
        Args:
            results_launch : str   ; results generated by NVIDIA scan tool.
        
        Raises:
             MetricNotAsignedToPart ; raised if some metric is found don't assigned 
                                      to any measure part
 
             EventNotAsignedToPart ; raised if some event is found don't assigned 
                                      to any measure part
        """

        event_name : str
        event_total_value : str
        metric_name : str
        metric_description : str
        metric_avg_value : str
        has_read_all_events : bool = False
        back_core_bound_value_has_found : bool 
        back_core_bound_description_has_found : bool
        back_memory_bound_value_has_found : bool 
        back_memory_bound_description_has_found : bool
        front_decode_value_has_found : bool 
        front_decode_description_has_found : bool
        front_fetch_value_has_found : bool 
        front_fetch_description_has_found : bool
        for line in results_launch.splitlines():
            line = re.sub(' +', ' ', line) # delete more than one spaces and put only one
            list_words = line.split(" ")
            if not has_read_all_events:
                # Check if it's line of interest:
                # ['', 'X', 'event_name','Min', 'Max', 'Avg', 'Total']
                if len(list_words) > 1: 
                    if list_words[1] == "Metric": # check end events
                        has_read_all_events = True
                    elif list_words[0] == '' and list_words[len(list_words) - 1][0].isnumeric():
                        event_name = list_words[2]
                        event_total_value = list_words[len(list_words) - 1]     
                        back_core_bound_value_has_found = self._back_core_bound.set_event_value(event_name, event_total_value)
                        #back_core_bound_description_has_found = self._back_core_bound.set_event_description(event_name, metric_description)
                        back_memory_bound_value_has_found = self._back_memory_bound.set_event_value(event_name, event_total_value)
                        #back_memory_bound_description_has_found = self._back_memory_bound.set_event_description(event_name, metric_description)
                        front_decode_value_has_found = self._front_decode.set_event_value(event_name, event_total_value)
                        #front_decode_description_has_found = self._front_decode.set_event_description(event_name, metric_description)
                        front_fetch_value_has_found = self._front_fetch.set_event_value(event_name, event_total_value)
                        #front_fetch_description_has_found = self._front_fetch.set_event_description(event_name, metric_description)
                        if not (back_core_bound_value_has_found or back_memory_bound_value_has_found or front_decode_value_has_found
                            or front_fetch_value_has_found): #or 
                            #not(back_core_bound_description_has_found or back_memory_bound_description_has_found or front_decode_description_has_found
                            # or front_fetch_description_has_found)): 
                            if not self.__eventExists(event_name):
                                raise EventNotAsignedToPart(event_name)
            else: # metrics
                # Check if it's line of interest:
                # ['', 'X', 'NAME_COUNTER', ... , 'Min', 'Max', 'Avg' (Y%)] where X (int number), Y (int/float number)
                if len(list_words) > 1 and list_words[0] == '' and list_words[len(list_words) - 1][0].isnumeric():
                    metric_name = list_words[2]
                    metric_description = ""
                    for i in range(3, len(list_words) - 3):
                        metric_description += list_words[i] + " "     
                    metric_avg_value = list_words[len(list_words) - 1]
                    #metric_max_value = list_words[len(list_words) - 2]
                    #metric_min_value = list_words[len(list_words) - 3]
                    #if metric_avg_value != metric_max_value or metric_avg_value != metric_min_value:
                        # Do Something. NOT USED
                    back_core_bound_value_has_found = self._back_core_bound.set_metric_value(metric_name, metric_avg_value)
                    back_core_bound_description_has_found = self._back_core_bound.set_metric_description(metric_name, metric_description)
                    back_memory_bound_value_has_found = self._back_memory_bound.set_metric_value(metric_name, metric_avg_value)
                    back_memory_bound_description_has_found = self._back_memory_bound.set_metric_description(metric_name, metric_description)
                    front_decode_value_has_found = self._front_decode.set_metric_value(metric_name, metric_avg_value)
                    front_decode_description_has_found = self._front_decode.set_metric_description(metric_name, metric_description)  
                    front_fetch_value_has_found = self._front_fetch.set_metric_value(metric_name, metric_avg_value)
                    front_fetch_description_has_found = self._front_fetch.set_metric_description(metric_name, metric_description)         
                    if (not (back_core_bound_value_has_found or back_memory_bound_value_has_found or front_decode_value_has_found
                        or front_fetch_value_has_found) or not(back_core_bound_description_has_found or back_memory_bound_description_has_found 
                        or front_decode_description_has_found or front_fetch_description_has_found)): 
                        if not self._metricExists(metric_name):
                            raise MetricNotAsignedToPart(metric_name)
        

    def _branch_divergence_ipc_degradation(self) -> float:
        """
        Find IPC degradation due to Divergence.Branch part

        Returns:
            Float with theDivergence's IPC degradation

        """
        
        return super()._branch_diver_ipc_degradation(LevelExecutionParameters.C_WARP_EXECUTION_EFFICIENCY_METRIC_NAME_NVPROF)
        


    def _replay_divergence_ipc_degradation(self) -> float:
        """
        Find IPC degradation due to Divergence.Replay part

        Returns:
            Float with theDivergence's IPC degradation

        """
        
        return super()._replay_diver_ipc_degradation(LevelExecutionParameters.C_ISSUE_IPC_METRIC_NAME_NVPROF)
        

    def _metricExists(self, metric_name : str) -> bool:
        """
        Check if metric exists in some part of the execution (MemoryBound, CoreBound...). 

        Args:
            metric_name  : str   ; name of the metric to be checked

        Returns:
            True if metric is defined in some part of the execution (MemoryBound, CoreBound...)
            or false in other case
        """

        is_defined_front_end_value : str = super().front_end().get_metric_value(metric_name)
        is_defined_front_end_description : str = super().front_end().get_metric_description(metric_name)

        is_defined_back_end_value : str = super().back_end().get_metric_value(metric_name)
        is_defined_back_end_description : str = super().back_end().get_metric_description(metric_name)

        is_defined_divergence_value : str = super().divergence().get_metric_value(metric_name)
        is_defined_divergence_description : str = super().divergence().get_metric_description(metric_name)

        is_defined_retire_value : str = super().retire().get_metric_value(metric_name)
        is_defined_retire_description : str = super().retire().get_metric_description(metric_name)

        is_defined_extra_measure_value : str = super().extra_measure().get_metric_value(metric_name)
        is_defined_extra_measure_description : str = super().extra_measure().get_metric_description(metric_name)

    
        if not ((is_defined_front_end_value is None and is_defined_front_end_description is None)
            or (is_defined_back_end_value is None and is_defined_back_end_description is None)
            or (is_defined_divergence_value is None and is_defined_divergence_description is None)
            or (is_defined_retire_value is None or is_defined_retire_description is None)
            or (is_defined_extra_measure_value is None and is_defined_extra_measure_description is None)):
            return False
        return True
        

    def __eventExists(self, event_name : str) -> bool:
        """
        Check if event exists in some part of the execution (MemoryBound, CoreBound...). 

        Args:
            event_name  : str   ; name of the event to be checked

        Returns:
            True if event is defined in some part of the execution (MemoryBound, CoreBound...)
            or false in other case
        """

        is_defined_front_end_value : str = super().front_end().get_metric_value(event_name)
        is_defined_front_end_description : str = super().front_end().get_metric_description(event_name)

        is_defined_back_end_value : str = super().back_end().get_metric_value(event_name)
        is_defined_back_end_description : str = super().back_end().get_metric_description(event_name)

        is_defined_divergence_value : str = super().divergence().get_metric_value(event_name)
        is_defined_divergence_description : str = super().divergence().get_metric_description(event_name)

        is_defined_retire_value : str = super().retire().get_metric_value(event_name)
        is_defined_retire_description : str = super().retire().get_metric_description(event_name)

        is_defined_extra_measure_value : str = super().extra_measure().get_metric_value(event_name)
        is_defined_extra_measure_description : str = super().extra_measure().get_metric_description(event_name)

        if not ((is_defined_front_end_value is None and is_defined_front_end_description is None)
            or (is_defined_back_end_value is None and is_defined_back_end_description is None)
            or (is_defined_divergence_value is None and is_defined_divergence_description is None)
            or (is_defined_retire_value is None or is_defined_retire_description is None)
            or (is_defined_extra_measure_value is None and is_defined_extra_measure_description is None)):
            return False
        return True
        

