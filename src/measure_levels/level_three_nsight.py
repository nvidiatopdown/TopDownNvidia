"""
Class that represents the level three of the execution based 
on NSIGHT scan tool.

@date:      Jul 2021
@version:   1.0
"""

import re
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1, parentdir) 
from measure_levels.level_two_nsight import LevelTwoNsight
from measure_parts.memory_constant_memory_bound import MemoryConstantMemoryBoundNsight
from measure_levels.level_three import LevelThree
from measure_parts.back_core_bound import BackCoreBoundNsight
from measure_parts.back_memory_bound import BackMemoryBoundNsight
from measure_parts.front_decode import FrontDecodeNsight
from measure_parts.front_fetch import FrontFetchNsight
from measure_parts.front_end import FrontEndNsight
from measure_parts.back_end import BackEndNsight
from measure_parts.divergence import DivergenceNsight
from measure_parts.retire import RetireNsight
from measure_parts.extra_measure import ExtraMeasureNsight
from measure_parts.memory_mio_throttle import MemoryMioThrottleNsight
from measure_parts.memory_l1_bound import MemoryL1BoundNsight
from show_messages.message_format import MessageFormat
from parameters.memory_constant_memory_bound_params import MemoryConstantMemoryBoundParameters
from parameters.memory_mio_throttle_params import MemoryMioThrottleParameters
from parameters.memory_l1_bound_params import MemoryL1BoundParameters
from errors.level_execution_errors import *

class LevelThreeNsight(LevelThree, LevelTwoNsight):
    """
    Class with level three of the execution based on Nsight scan tool.
    
    Atributes:
        __memory_constant_memory_bound      : ConstantMemoryBoundNsight ; constant cache part

        __memory_mio_throttle               : MemoryMioThrottleNsight   ; mio throttle part

        __memory_l1_bound                   : MemoryL1BoundNsight       ; l1 bound part    
    """

    def __init__(self, program : str, input_file : str, output_file : str, output_scan_file : str, collect_metrics : bool,
        front_end : FrontEndNsight, back_end : BackEndNsight, divergence : DivergenceNsight, retire : RetireNsight,
        extra_measure : ExtraMeasureNsight, front_decode : FrontDecodeNsight, front_fetch : FrontFetchNsight,
        back_core_bound : BackCoreBoundNsight, back_memory_bound : BackMemoryBoundNsight):
        
        self.__memory_constant_memory_bound : MemoryConstantMemoryBoundNsight = MemoryConstantMemoryBoundNsight(
            MemoryConstantMemoryBoundParameters.C_MEMORY_CONSTANT_MEMORY_BOUND_NAME, 
            MemoryConstantMemoryBoundParameters.C_MEMORY_CONSTANT_MEMORY_BOUND_DESCRIPTION, 
            MemoryConstantMemoryBoundParameters.C_MEMORY_CONSTANT_MEMORY_BOUND_NSIGHT_METRICS)

        self.__memory_mio_throttle : MemoryMioThrottleNsight =  MemoryMioThrottleNsight (
            MemoryMioThrottleParameters.C_MEMORY_MIO_THROTTLE_NAME, 
            MemoryMioThrottleParameters.C_MEMORY_MIO_THROTTLE_DESCRIPTION, 
            MemoryMioThrottleParameters.C_MEMORY_MIO_THROTTLE_NSIGHT_METRICS)

        self.__memory_l1_bound : MemoryL1BoundNsight =  MemoryL1BoundNsight (
            MemoryL1BoundParameters.C_MEMORY_L1_BOUND_NAME, 
            MemoryL1BoundParameters.C_MEMORY_L1_BOUND_DESCRIPTION, 
            MemoryL1BoundParameters.C_MEMORY_L1_BOUND_NSIGHT_METRICS)

        super().__init__(program, input_file, output_file, output_scan_file, collect_metrics, front_end, back_end, divergence, 
        retire, extra_measure, front_decode, front_fetch, back_core_bound, back_memory_bound)
          

    def memory_constant_memory_bound(self) -> MemoryConstantMemoryBoundNsight:
        """
        Return MemoryConstantMemoryBoundNsight part of the execution.

        Returns:
            reference to MemoryConstantMemoryBoundNsight part of the execution
        """

        return self.__memory_constant_memory_bound
        
    
    def memory_mio_throttle(self) -> MemoryMioThrottleNsight:
        """
        Return MemoryMioThrottleNsight part of the execution.

        Returns:
            reference to MemoryMioThrottleNsight part of the execution
        """

        return self.__memory_mio_throttle
        
  
    def memory_l1_bound(self) -> MemoryL1BoundNsight:
        """
        Return MemoryL1BoundNsight part of the execution.

        Returns:
            reference to MemoryL1BoundNsight part of the execution
        """

        return self.__memory_l1_bound
        


    def _generate_command(self) -> str:
        """ 
        Generate command of execution with NVIDIA scan tool.

        Returns:
            String with command to be executed
        """

        command : str = ("ncu --target-processes all --metrics " + self._front_end.metrics_str() +
            "," + self._back_end.metrics_str() + "," + self._divergence.metrics_str() + "," +
            self._extra_measure.metrics_str() + "," + self._retire.metrics_str() + "," + 
            self._front_decode.metrics_str() + "," + self._front_fetch.metrics_str() + 
            "," + self._back_core_bound.metrics_str() + "," + self._back_memory_bound.metrics_str() +
            "," + self.__memory_constant_memory_bound.metrics_str() + "," + self.__memory_mio_throttle.metrics_str() + "," + 
            self.__memory_l1_bound.metrics_str() + " " + self._program)
        return command
        
    
    def set_results(self,output_command : str):
        """
        Set results of execution ALREADY DONE. Results are in the argument.

        Args:
            output_command : str    ; str with results of execution.
        """

        super()._set_front_back_divergence_retire_results(output_command) # level one results
        super()._set_memory_core_decode_fetch_results(output_command) # level two
        self._set_memory_constant_memory_bound_mio_l1_bound_results(output_command) # level three
        


    def _get_results(self, lst_output : list):
        """ 
        Get results of the different parts.

        Parameters:
            lst_output              : list     ; OUTPUT list with results
        """

        #  Keep Results
        converter : MessageFormat = MessageFormat()

        if not self._collect_metrics:
            return
        if self._collect_metrics and self._front_end.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._front_end.name()))
            super()._add_result_part_to_lst(self._front_end.metrics(), 
                self._front_end.metrics_description(), lst_output)
        if  self._collect_metrics and self._front_decode.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._front_decode.name()))
            super()._add_result_part_to_lst(self._front_decode.metrics(), 
                self._front_decode.metrics_description(), lst_output)      
        if self._collect_metrics and self._front_fetch.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._front_fetch.name()))
            super()._add_result_part_to_lst(self._front_fetch.metrics(), 
                self._front_fetch.metrics_description(), lst_output)
        if self._collect_metrics and self._back_end.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._back_end.name()))
            super()._add_result_part_to_lst(self._back_end.metrics(), 
                self._back_end.metrics_description(), lst_output)
        if self._collect_metrics and self._back_core_bound.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._back_core_bound.name()))
            super()._add_result_part_to_lst(self._back_core_bound.metrics(), 
                self._back_core_bound.metrics_description(), lst_output)
        if self._collect_metrics and self._back_memory_bound.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._back_memory_bound.name()))
            super()._add_result_part_to_lst(self._back_memory_bound.metrics(), 
                self._back_memory_bound.metrics_description(), lst_output)
        if  self._collect_metrics and self.__memory_constant_memory_bound.metrics_str() != "":
            lst_output.append(converter.underlined_str(self.__memory_constant_memory_bound.name()))
            super()._add_result_part_to_lst(self.__memory_constant_memory_bound.metrics(), 
                self.__memory_constant_memory_bound.metrics_description(), lst_output)
        if  self._collect_metrics and self.__memory_mio_throttle.metrics_str() != "":
            lst_output.append(converter.underlined_str(self.__memory_mio_throttle.name()))
            super()._add_result_part_to_lst(self.__memory_mio_throttle.metrics(), 
                self.__memory_mio_throttle.metrics_description(), lst_output)
        if  self._collect_metrics and self.__memory_l1_bound.metrics_str() != "":
            lst_output.append(converter.underlined_str(self.__memory_l1_bound.name()))
            super()._add_result_part_to_lst(self.__memory_l1_bound.metrics(), 
                self.__memory_l1_bound.metrics_description(), lst_output)
        if self._collect_metrics and self._divergence.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._divergence.name()))
            super()._add_result_part_to_lst(self._divergence.metrics(), 
                self._divergence.metrics_description(), lst_output)
        if self._collect_metrics and  self._retire.metrics_str() != "":
                lst_output.append(converter.underlined_str(self._retire.name()))
                super()._add_result_part_to_lst(self._retire.metrics(), 
                self._retire.metrics_description(), lst_output)
        if self._collect_metrics and self._extra_measure.metrics_str() != "":
            lst_output.append(converter.underlined_str(self._extra_measure.name()))
            super()._add_result_part_to_lst(self._extra_measure.metrics(), 
                self._extra_measure.metrics_description(), lst_output)
        lst_output.append("\n")
        
    

    def _metricExists(self, metric_name : str) -> bool:
        """
        Check if metric exists in some part of the execution (MemoryBound, CoreBound...). 

        Args:
            metric_name  : str   ; name of the metric to be checked

        Returns:
            True if metric is defined in some part of the execution (MemoryBound, CoreBound...)
            or false in other case
        """

        is_defined_front_fetch_value : str = super().front_fetch().get_metric_value(metric_name)
        is_defined_front_fetch_unit : str = super().front_fetch().get_metric_unit(metric_name)

        is_defined_front_decode_value : str = super().front_decode().get_metric_value(metric_name)
        is_defined_front_decode_unit : str = super().front_decode().get_metric_unit(metric_name)

        is_defined_back_memory_bound_value : str = super().back_memory_bound().get_metric_value(metric_name)
        is_defined_back_memory_bound_unit : str = super().back_memory_bound().get_metric_unit(metric_name)

        is_defined_back_core_bound_value : str = super().back_core_bound().get_metric_value(metric_name)
        is_defined_back_core_bound_unit : str = super().back_core_bound().get_metric_unit(metric_name)

        if not ((is_defined_front_fetch_value is None and is_defined_front_fetch_unit is None)
            or (is_defined_front_decode_value is None and is_defined_front_decode_unit is None)
            or (is_defined_back_memory_bound_value is None and is_defined_back_memory_bound_unit is None)
            or (is_defined_back_core_bound_value is None or is_defined_back_core_bound_unit is None)):
            return False
        return True

    def _set_memory_constant_memory_bound_mio_l1_bound_results(self, results_launch : str):
        """
        Set results of the level three part (that are not level one or two).
        
        Args:
            results_launch : str   ; results generated by NVIDIA scan tool.

        Raises:
            MetricNotAsignedToPart ; raised if some metric is found don't assigned 
                                      to any measure part
 
             EventNotAsignedToPart ; raised if some event is found don't assigned 
                                      to any measure part
        """
        
        metric_name : str
        metric_unit : str
        metric_value : str
        line : str
        i : int
        list_words : list
        memory_constant_memory_bound_value_has_found: bool
        memory_constant_memory_bound_unit_has_found : bool
        memory_mio_throttle_value_has_found: bool
        memory_mio_throttle_unit_has_found : bool
        memory_l1_bound_value_has_found: bool
        memory_l1_bound_unit_has_found : bool
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
                memory_constant_memory_bound_value_has_found = self.__memory_constant_memory_bound.set_metric_value(metric_name, 
                    metric_value)
                memory_constant_memory_bound_unit_has_found = self.__memory_constant_memory_bound.set_metric_unit(metric_name, 
                    metric_unit) 
                memory_mio_throttle_value_has_found = self.__memory_mio_throttle.set_metric_value(metric_name, 
                    metric_value)
                memory_mio_throttle_unit_has_found = self.__memory_mio_throttle.set_metric_unit(metric_name, 
                    metric_unit)
                memory_l1_bound_value_has_found = self.__memory_l1_bound.set_metric_value(metric_name, 
                    metric_value)
                memory_l1_bound_unit_has_found = self.__memory_l1_bound.set_metric_unit(metric_name, 
                    metric_unit)
                if (not (memory_constant_memory_bound_value_has_found or memory_mio_throttle_value_has_found or memory_l1_bound_value_has_found) 
                    or not (memory_constant_memory_bound_unit_has_found or memory_mio_throttle_unit_has_found or memory_l1_bound_unit_has_found)):
                    if not self._metricExists(metric_name):
                        raise MetricNotAsignedToPart(metric_name)
        

    def memory_mio_throttle_stall(self) -> float:
        """
        Returns percent of stalls due to BackEnd.MemoryBound.MioThrottle part.

        Returns:
            Float with percent of total stalls due to BackEnd.MemoryBound.MioThrottle part
        """

        return self._get_stalls_of_part(self.memory_mio_throttle().metrics())
        

    def memory_mio_throttle_stall_on_back(self) -> float:
        """ 
        Obtain the percentage of stalls due to BackEnd.MemoryBound.MioThrottle
        on the total BackEnd

        Returns:
            Float the percentage of stalls due to BackEnd.MemoryBound.MemoryMioThrottle
            on the total BackEnd
        """

        return (self.memory_mio_throttle_stall()/super().back_end_stall())*100.0

    def memory_mio_throttle_stall_on_memory_bound(self) -> float:
        """ 
        Obtain the percentage of stalls due to BackEnd.MemoryBound.MioThrottle
        on the total BackEnd.MemoryBound

        Returns:
            Float the percentage of stalls due to BackEnd.MemoryBound.MioThrottle
            on the total BackEnd.MemoryBound
        """

        return (self.memory_mio_throttle_stall()/super().back_memory_bound_stall())*100.0
        

    def memory_mio_throttle_percentage_ipc_degradation(self) -> float: 
        """
        Find percentage of IPC degradation due to BackEnd.MemoryBound.MioThrottle part.

        Returns:
            Float with the percent of BackEnd.MemoryBound.MioThrottle's IPC degradation
        """

        return (((self._stall_ipc()*(self.memory_mio_throttle_stall()/100.0))/self.get_device_max_ipc())*100.0)
        
    
    def memory_l1_bound_stall(self) -> float:
        """
        Returns percent of stalls due to BackEnd.MemoryBound.L1Bound part.

        Returns:
            Float with percent of total stalls due to BackEnd.MemoryBound.L1Bound part
        """

        return self._get_stalls_of_part(self.memory_l1_bound().metrics())
        

    def memory_l1_bound_stall_on_back(self) -> float:
        """ 
        Obtain the percentage of stalls due to BackEnd.MemoryBound.L1Bound
        on the total BackEnd

        Returns:
            Float the percentage of stalls due to BackEnd.MemoryBound.L1Bound
            on the total BackEnd
        """

        return (self.memory_l1_bound_stall()/super().back_end_stall())*100.0

    def memory_l1_bound_stall_on_memory_bound(self) -> float:
        """ 
        Obtain the percentage of stalls due to BackEnd.MemoryBound.MemoryL1Bound
        on the total BackEnd.MemoryBound

        Returns:
            Float the percentage of stalls due to BackEnd.MemoryBound.MemoryL1Bound
            on the total BackEnd.MemoryBound
        """

        return (self.memory_l1_bound_stall()/super().back_memory_bound_stall())*100.0
        

    def memory_l1_bound_percentage_ipc_degradation(self) -> float:
        """
        Find percentage of IPC degradation due to BackEnd.MemoryBound.MemoryL1Bound part.

        Returns:
            Float with the percent of BackEnd.MemoryBound.MemoryL1Bound's IPC degradation
        """

        return (((self._stall_ipc()*(self.memory_l1_bound_stall()/100.0))/self.get_device_max_ipc())*100.0)
        

