#!/usr/bin/env python3
"""
Program that implements the Top Down methodology over NVIDIA GPUs.

@date:      Jul 2021
@version:   1.0
"""

import argparse
import sys
from errors.topdown_errors import *
from parameters.topdown_params import TopDownParameters # parameters of program
from measure_levels.level_one_nvprof import LevelOneNvprof
from measure_levels.level_one_nsight import LevelOneNsight
from measure_levels.level_two_nvprof import LevelTwoNvprof
from measure_levels.level_two_nsight import LevelTwoNsight
from measure_levels.level_three_nsight import LevelThreeNsight
from measure_levels.level_three_nvprof import LevelThreeNvprof
from measure_parts.front_end import FrontEndNsight, FrontEndNvprof
from measure_parts.back_end import BackEndNsight, BackEndNvprof
from measure_parts.divergence import DivergenceNsight, DivergenceNvprof
from measure_parts.retire import RetireNsight, RetireNvprof
from measure_parts.extra_measure import ExtraMeasureNsight, ExtraMeasureNvprof
from measure_levels.level_three import LevelThree
from measure_levels.level_one import LevelOne
from measure_levels.level_two import LevelTwo
from measure_parts.front_decode import  FrontDecodeNsight, FrontDecodeNvprof
from measure_parts.front_fetch import FrontFetchNsight, FrontFetchNvprof
from measure_parts.back_core_bound import BackCoreBoundNsight, BackCoreBoundNvprof
from measure_parts.back_memory_bound import BackMemoryBoundNsight, BackMemoryBoundNvprof
from show_messages.message_format import MessageFormat
from args.unique_argument import DontRepeat
from shell.shell import Shell
from parameters.front_end_params import FrontEndParameters
from parameters.back_end_params import BackEndParameters
from parameters.divergence_params import DivergenceParameters
from parameters.retire_params import RetireParameters
from parameters.extra_measure_params import ExtraMeasureParameters
from parameters.front_fetch_params import FrontFetchParameters
from parameters.front_decode_params import FrontDecodeParameters
from parameters.back_memory_bound_params import BackMemoryBoundParameters
from parameters.back_core_bound_params import BackCoreBoundParameters

class TopDown:
    """
    Class that implements TopDown methodology over NVIDIA GPUs.
    
    Attributes:
        __level                         : int                       ;   level of the exection
        
        __input_output_scan_file        : str                       ;   input file with results computed by NVIDIA scan tool

        __output_file                   : str                       ;   path to log to show results or 'None' if option
                                                                        is not specified

        __verbose                       : bool                      ;   True to show long-descriptions of results or
                                                                        False in other case

        __program                       : str                       ;   path to program to be executed
                            
        __delete_output_file_content    : bool                      ;   If '-o/--output' is set delete output's file contents 
                                                                        before write results

        __show_desc                     : bool                      ;   True to show descriptions of results or
                                                                        False in other case

        __show_metrics                  : bool                      ;   True if program has to show metrics computed by NVIDIA 
                                                                        scan tool

        __show_events                   : bool                      ;   True if program has to show events computed by NVIDIA scan 
                                                                        tool

        __show_all_measurements         : bool                      ;   True if program has to show all measures 
                                                                        computed by NVIDIA scan tool

        __show_graph                    : bool                      ;   True if program has to show graphs or False if not

        __output_graph_file             : str                       ;   path to graph file or 'None' if option is not specified

        __output_output_scan_file       : str                       ;   path to scan file or 'None' if option is not specified
    """
    
    def __init__(self):
        """
        Init attributes depending of arguments.
        """

        parser : argparse.ArgumentParse = argparse.ArgumentParser(#prog='[/path/to/PROGRAM]',
            formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position = 100, width=200),
            description = "TopDown methodology on NVIDIA's GPUs",
            epilog = "Check options to run program",
            usage='%(prog)s [OPTIONS] -f [PROGRAM] -l [NUM]') #exit_on_error=False)
        parser._optionals.title = "Optional arguments"
        self.__add_arguments(parser)

        # Save values into attributes
        args : argparse.Namespace = parser.parse_args()
      
        self.__level : int = args.level[0]
        self.__output_file : str = args.file
        self.__verbose : bool = args.verbose
        if args.program is None:
            self.__program : str = None
        else:
            self.__program : str = " ".join(str(string) for string in args.program)
        self.__delete_output_file_content : bool = args.delete_output_file_content
        self.__show_desc : bool = args.show_desc
        self.__show_metrics : bool = args.metrics
        self.__show_events : bool = args.events
        self.__show_all_measurements : bool = args.all_measures
        self.__show_graph : bool = args.show_graph
        self.__output_graph_file : str = args.output_graph_file
        self.__output_scan_file : str = args.output_scan_file
        self.__input_scan_file : str = args.input_scan_file
        
    
    def __add_show_desc_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add show-description argument. 'C_LONG_DESCRIPTION_ARGUMENT_SHORT_OPTION' is the short 
        option of argument and 'C_LONG_DESCRIPTION_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_SHOW_DESCRIPTION_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_SHOW_DESCRIPTION_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_SHOW_DESCRIPTION_ARGUMENT_DESCRIPTION, 
            action = 'store_false',
            dest = 'show_desc')
        

    def __add_metrics_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add metrics argument. 'C_METRICS_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_METRICS_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_METRICS_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_METRICS_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_METRICS_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'metrics')
        
    
    def __add_show_graph_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add graph argument. 'C_GRAPH_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_GRAPH_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_GRAPH_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_GRAPH_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_GRAPH_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'show_graph')
        
    
    def __add_all_measures_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add all measures argument. 'C_ALL_MEASURES_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_ALL_MEASURES_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_ALL_MEASURES_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_ALL_MEASURES_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_ALL_MEASURES_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'all_measures')
        

    def __add_events_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add events argument. 'C_EVENTS_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_EVENTS_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_EVENTS_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_EVENTS_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_EVENTS_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'events')
        
        
    def __add_program_argument(self, group : argparse._ArgumentGroup) :
        """ 
        Add program argument. 'C_FILE_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_FILE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            group : argparse._ArgumentGroup ; group of the argument.
        """

        group.add_argument(
            TopDownParameters.C_FILE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_FILE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_FILE_ARGUMENT_DESCRIPTION,
            default = None,
            nargs = '*',  
            action = DontRepeat,
            type = str, 
            #metavar='/path/to/file',
            dest = 'program')
        

    def __add_level_argument(self, group : argparse._ArgumentGroup):
        """ 
        Add level argument. 'C_LEVEL_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_LEVEL_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            group : argparse._ArgumentGroup ; group of the argument.
        """
        
        group.add_argument (
            TopDownParameters.C_LEVEL_ARGUMENT_SHORT_OPTION, TopDownParameters.C_LEVEL_ARGUMENT_LONG_OPTION,
            required = True,
            help = TopDownParameters.C_LEVEL_ARGUMENT_DESCRIPTION,
            type = int,
            action = DontRepeat,
            nargs = 1,
            choices = range(TopDownParameters.C_MIN_LEVEL_EXECUTION, TopDownParameters.C_MAX_LEVEL_EXECUTION + 1), # range [1,3], produces error, 
            metavar = '[NUM]',
            dest = 'level')
        

    def __add_ouput_file_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add output-file argument. 'C_OUTPUT_FILE_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_OUTPUT_FILE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """
        
        parser.add_argument (
            TopDownParameters.C_OUTPUT_FILE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_OUTPUT_FILE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_OUTPUT_FILE_ARGUMENT_DESCRIPTION,
            default = None,
            action = DontRepeat,
            nargs = '?', 
            type = str, 
            #metavar='/path/to/file',
            dest = 'file')
        

    def __add_verbose_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add verbose argument. 'C_VERBOSE_ARGUMENT_SHORT_OPTION' is the short 
        option of argument and 'C_VERBOSE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_VERBOSE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_VERBOSE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_VERBOSE_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'verbose')
        
    
    def __add_delete_output_file_content(self, parser : argparse.ArgumentParser):
        """ 
        Add output's file delete content argument. 'C_DELETE_CONTENT_ARGUMENT_SHORT_OPTION' is the short 
        option of argument and 'C_DELETE_CONTENT_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """

        parser.add_argument (
            TopDownParameters.C_DELETE_CONTENT_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_DELETE_CONTENT_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_DELETE_CONTENT_ARGUMENT_DESCRIPTION,
            action = 'store_true',
            dest = 'delete_output_file_content')
        

    def __add_ouput_graph_file_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add output graph file argument. 'C_OUTPUT_GRAPH_FILE_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_OUTPUT_GRAPH_FILE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """
        
        parser.add_argument (
            TopDownParameters.C_OUTPUT_GRAPH_FILE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_OUTPUT_GRAPH_FILE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_OUTPUT_GRAPH_FILE_ARGUMENT_DESCRIPTION,
            default = None,
            action = DontRepeat,
            nargs = '?', 
            type = str, 
            #metavar='/path/to/file',
            dest = 'output_graph_file')
        

    def __add_input_scan_file_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add input scan file argument. 'C_INPUT_SCAN_FILE_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_INPUT_SCAN_FILE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """
        
        parser.add_argument (
            TopDownParameters.C_INPUT_SCAN_FILE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_INPUT_SCAN_FILE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_INPUT_SCAN_FILE_ARGUMENT_DESCRIPTION,
            default = None,
            action = DontRepeat,
            nargs = '?', 
            type = str, 
            #metavar='/path/to/file',
            dest = 'input_scan_file')
        

    def __add_output_scan_file_argument(self, parser : argparse.ArgumentParser):
        """ 
        Add output scan file argument. 'C_OUTPUT_SCAN_FILE_ARGUMENT_SHORT_OPTION' is the short option of argument
        and 'C_OUTPUT_SCAN_FILE_ARGUMENT_LONG_OPTION' is the long version of argument.

        Args:
            parser : argparse.ArgumentParser ; group of the argument.
        """
        
        parser.add_argument (
            TopDownParameters.C_OUTPUT_SCAN_FILE_ARGUMENT_SHORT_OPTION, 
            TopDownParameters.C_OUTPUT_SCAN_FILE_ARGUMENT_LONG_OPTION, 
            help = TopDownParameters.C_OUTPUT_SCAN_FILE_ARGUMENT_DESCRIPTION,
            default = None,
            #action = DontRepeat,
            nargs = '?', 
            type = str, 
            #metavar='/path/to/file',
            dest = 'output_scan_file')
        

    def __add_arguments(self, parser : argparse.ArgumentParser):
        """ 
        Add arguments of the pogram.

        Args:
            parser : argparse.ArgumentParser ; group of the arguments.
        """

        # Create group for required arguments
        requiredGroup : argparse._ArgumentGroup = parser.add_argument_group("Required arguments")

        self.__add_program_argument(parser)
        self.__add_level_argument(requiredGroup)
        self.__add_ouput_file_argument(parser)
        self.__add_verbose_argument(parser)
        self.__add_delete_output_file_content(parser)
        self.__add_show_desc_argument(parser)
        self.__add_metrics_argument(parser)
        self.__add_events_argument(parser)
        self.__add_all_measures_argument(parser)
        self.__add_show_graph_argument(parser)
        self.__add_ouput_graph_file_argument(parser)
        self.__add_output_scan_file_argument(parser)
        self.__add_input_scan_file_argument(parser)
        

    def program(self) -> str:
        """
        Returns path to runnable program.

        Returns:
            str with path to program to be executed
        """

        return self.__program
        
    
    def level(self) -> int:
        """ 
        Find the TopDown run level.

        Returns:
            the level of the execution.
        """ 

        return self.__level
        

    def output_file(self) -> str:
        """
        Find path to output file.

        Returns:
            path to file to write, or None if 
            option '-o' or '--output' has not been indicated
        """

        return self.__output_file # descriptor to file or None
        

    def output_graph_file(self) -> str:
        """
        Find path to output graph file.

        Returns:
            path to graph file to write, or None if 
            option '-o' or '--output' has not been indicated
        """

        return self.__output_graph_file # descriptor to file or None
        

    def output_scan_file(self) -> str:
        """
        Find path to output scan file.

        Returns:
            path to scan file to write, or None if 
            option '-o' or '--output' has not been indicated
        """

        return self.__output_scan_file # descriptor to file or None
        
    
    def input_scan_file(self) -> str:
        """
        Find path to input scan file.

        Returns:
            path to scan file to write, or None if 
            option '-is' or '--input-scan' has not been indicated
        """

        return self.__input_scan_file # descriptor to file or None
        
    
    def show_verbose(self) -> bool:
        """
        Check if program has to show verbose.

        Returns:
            True to verbose of False if not
        """

        return self.__verbose
        

    def show_desc(self) -> bool:
        """
        Check if program has to show description of results.

        Returns:
            True to show description of False if not
        """

        return self.__show_desc
        

    def show_metrics(self) -> bool:
        """
        Check if program has to show metrics computed by NVIDIA scan tool.

        Returns:
            True if program has to show metrics computed by NVIDIA scan tool or
            False if not.
        """

        return self.__show_metrics
        

    def show_all_measures(self) -> bool:
        """
        Check if program has to show all measures (events and metrics) computed by NVIDIA scan tool.

        Returns:
            True if program has to show all measures (events and metrics) computed by NVIDIA scan tool or
            False if not.
        """

        return self.__show_all_measurements 
        

    def show_events(self) -> bool:
        """
        Check if program has to show events computed by NVIDIA scan tool.

        Returns:
            True if program has to show events computed by NVIDIA scan tool or
            False if not.
        """

        return self.__show_events
        
    
    def delete_output_file_content(self) -> bool:
        """
        Check if program has to delete output's file contents.

        Returns:
            True to delete output's file content or False if not
        """

        return self.__delete_output_file_content
        

    def input_file(self) -> str:
        """
        Find path to output file.

        Returns:
            path to file with results computed by NVIDIA scan tool, or None if 
            option '-is' or '--input-scan' has not been indicated
        """

        return self.__input_scan_file 
        

    def show_graph(self) -> bool:
        """ 
        Check if program has to show graph with description of results.

        Returns:
            True if program has to show graph or False if not
        """
        
        return self.__show_graph
        

    def __intro_message(self): 
        """ Intro message with information."""

        printer : MessageFormat = MessageFormat()
        message : str = "TopDown Metholodgy over NVIDIA's GPUs"
        #printer.print_center_msg_box(msg = "TopDown Metholodgy over NVIDIA's GPUs", indent = 1, title = "", output_file = self.output_file(), 
        #        width = None, delete_content_file = self.delete_output_file_content())
        printer.print_desplazed_underlined_str(message = message, output_file = self.output_file(), delete_content_file = self.delete_output_file_content())
        print()
        message  = "\n\nWelcome to the " + sys.argv[0] + " program where you can check the bottlenecks of your\n" + \
            "CUDA program running on NVIDIA GPUs. This analysis is carried out considering the architectural\n" + \
            "aspects of your GPU, in its different parts. The objective is to detect the bottlenecks in your\n" + \
            "program, which cause the IPC (Instructions per Cycle) to be drastically reduced."
        printer.print_max_line_length_message(message, TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False)
        print()
        print()
        message = "\n\nIn accordance with what has been entered, the execution will be carried out following the following terms:\n"
        printer.print_max_line_length_message(message, TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False)
        message = ("\n- Execution Level:                  " + str(self.level()) + "\n" +
                   "- Analyzed program:                 " + self.program() + "\n" +
                   "- Output File:                      " + str(self.output_file()) + "\n" +
                   "- Verbose:                          " + str(self.show_verbose()) + "\n" +
                   "- Delete output's file content:     " + str(self.delete_output_file_content()) + "\n" +
                   "- Output Graph File:                " + str(self.output_graph_file()) + "\n" + 
                   "- Show Graph:                       " + str(self.show_graph()) + "\n" +
                   "- Input Scan File:                  " + str(self.input_scan_file()) + "\n" + 
                   "- Output Scan File:                 " + str(self.output_scan_file()))
        execute_with_nvprof : bool = self.__is_nvprof_mode()
        show_events : bool = self.show_events()
        show_events_with_nsight : str = "\n"
        if not execute_with_nvprof:
            if show_events:
                show_events_with_nsight =               (". You have introduce the option\n" + 
                    "                                    to show events (-e, --events), but\n" +
                    "                                    NSIGHT execution doesn't have EVENTS,\n" + 
                    "                                    so this argument will not be taken into\n" + 
                    "                                    account.\n")
        message += ("\n- Show Metrics:                     " + str(self.show_metrics()) + "\n" + \
                    "- Show Events:                      " + str(self.show_events())  + show_events_with_nsight + \
                    "- Show All Measurements:            " + str(self.show_all_measures()) ) 
                    
        printer.print_msg_box(msg = message, indent = 1, title = "EXECUTION FEATURES", output_file = self.output_file(), width = None,
            delete_content_file = False)
        print()
        message = "\n\nSaid that, according to the level entered by you, WE START THE ANALYSIS.\n"
        printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
            output_file = self.output_file(), delete_content_file = False)
        print()
        
      
    def __show_level_one_results(self, level_execution : LevelOne):
        """Show results of level one."""
        
        stalls_front_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.front_end_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_back_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.back_end_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_divergence_message : str = ("{:<20} {:<6}".format("IPC DEGRADATION (%): ", 
            str(round(level_execution.divergence_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))   
        ipc_retire_message : str = ("{:<21} {:<4}".format('PERFORMANCE IPC (%):', 
            str(round(level_execution.retire_ipc_percentage(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')) 
        ipc_degradation_front_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.front_end_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_back_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.back_end_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        messages : list[list[str]] = [["","","",""], [stalls_front_message, stalls_back_message, ipc_degradation_divergence_message, 
        ipc_retire_message], [ipc_degradation_front_message, ipc_degradation_back_message, " ", " "]]
        titles : list[str] = [level_execution.front_end().name(), level_execution.back_end().name(),
            level_execution.divergence().name(),level_execution.retire().name()]
        MessageFormat().print_four_msg_box(messages, titles, 1, self.output_file(), False)
        

    def __show_level_two_results(self, level_execution : LevelTwo):
        """Show results of level two."""

        stalls_front_decode_on_total_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.front_decode_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_front_fetch_on_total_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.front_fetch_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_back_core_bound_on_total_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.back_core_bound_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_back_memory_bound_on_total_message : str = ("{:<20} {:<6}".format('STALLS, on the total (%): ', 
            str(round(level_execution.back_memory_bound_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_front_decode_on_front_message : str = ("{:<22} {:<6}".format('STALLS, on FrontEnd  (%): ', 
            str(round(level_execution.front_decode_stall_on_front(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_front_fetch_on_front_message : str = ("{:<20} {:<6}".format('STALLS, on FrontEnd  (%): ', 
            str(round(level_execution.front_fetch_stall_on_front(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_back_core_bound_on_back_message : str = ("{:<20} {:<6}".format('STALLS, on BackEnd   (%): ', 
            str(round(level_execution.back_core_bound_stall_on_back(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        stalls_back_memory_bound_on_back_message : str = ("{:<20} {:<6}".format('STALLS, on BackEnd   (%): ', 
            str(round(level_execution.back_memory_bound_stall_on_back(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_front_decode_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.front_decode_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_front_fetch_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.front_fetch_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_back_core_bound_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.back_core_bound_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        ipc_degradation_back_memory_bound_message : str = ("{:<26} {:<5}".format('IPC DEGRADATION      (%): ', 
            str(round(level_execution.back_memory_bound_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))
        messages : list[list[str]] = [["","","",""] , [stalls_front_decode_on_total_message, 
            stalls_front_fetch_on_total_message,  stalls_back_core_bound_on_total_message, 
            stalls_back_memory_bound_on_total_message], [stalls_front_decode_on_front_message, 
            stalls_front_fetch_on_front_message, stalls_back_core_bound_on_back_message, 
            stalls_back_memory_bound_on_back_message], ["", "", "", ""], 
            [ipc_degradation_front_decode_message, ipc_degradation_front_fetch_message,
            ipc_degradation_back_core_bound_message, ipc_degradation_back_memory_bound_message]]
        titles : list[str] = [level_execution.front_decode().name(), level_execution.front_fetch().name(),
            level_execution.back_core_bound().name(),level_execution.back_memory_bound().name()]
    
        printer : MessageFormat = MessageFormat()
        printer.print_four_msg_box(messages, titles, 1, self.output_file(), False)
        printer.print_max_line_length_message(message = "\n", max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
        ipc_degradation_branch_divergence_message : str = ("{:<20} {:<6}".format("IPC DEGRADATION (%): ", 
            str(round(level_execution.branch_divergence_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))   
        ipc_degradation_replay_divergence_message : str = ("{:<20} {:<6}".format("IPC DEGRADATION (%): ", 
            str(round(level_execution.replay_divergence_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%'))   
        titles = [level_execution.divergence_branch().name(), level_execution.divergence_replay().name()]
        messages = [[ipc_degradation_branch_divergence_message, ipc_degradation_replay_divergence_message]]
        printer.print_two_msg_box(messages, titles, 1, self.output_file(), False)
        

    def __show_level_three_results(self, level_execution : LevelThree):
        """Show results of level three."""

        stalls_memory_constant_memory_bound_on_total_message : str = ("STALLS, on the total             (%): " +
            str(round(level_execution.memory_constant_memory_bound_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
        stalls_memory_constant_memory_bound_on_memory_bound_message : str = ("STALLS, on " + level_execution.back_memory_bound().name() + " (%): " +  
            str(round(level_execution.memory_constant_memory_bound_stall_on_memory_bound(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
        stalls_memory_constant_memory_bound_on_back_message : str = ("STALLS, on " + level_execution.back_end().name() + "              (%): " +
            str(round(level_execution.memory_constant_memory_bound_stall_on_back(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
        ipc_degradation_memory_constant_memory_bound_message : str = ("IPC DEGRADATION                  (%): " +  
            str(round(level_execution.memory_constant_memory_bound_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
        if type(level_execution) is LevelThreeNsight:
            stalls_memory_mio_throttle_on_total_message : str = ("STALLS, on the total             (%): " +  
                str(round(level_execution.memory_mio_throttle_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            stalls_memory_l1_bound_on_total_message : str = ("STALLS, on the total             (%): " +
                str(round(level_execution.memory_l1_bound_stall(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            stalls_memory_mio_throttle_on_memory_bound_message : str = ("STALLS, on " + level_execution.back_memory_bound().name() + " (%): " +  
                str(round(level_execution.memory_mio_throttle_stall_on_memory_bound(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            stalls_memory_l1_bound_on_memory_bound_message : str = ("STALLS, on " + level_execution.back_memory_bound().name() + " (%): " +  
                str(round(level_execution.memory_l1_bound_stall_on_memory_bound(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            stalls_memory_mio_throttle_on_back_message : str = ("STALLS, on " + level_execution.back_end().name() + "              (%): " +
                str(round(level_execution.memory_mio_throttle_stall_on_back(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            stalls_memory_l1_bound_on_back_message : str = ("STALLS, on " + level_execution.back_end().name() + "              (%): " +
                str(round(level_execution.memory_l1_bound_stall_on_back(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            ipc_degradation_memory_mio_throttle_message : str = ("IPC DEGRADATION                  (%): " +  
                str(round(level_execution.memory_mio_throttle_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            ipc_degradation_memory_l1_bound_message : str = ("IPC DEGRADATION                  (%): " +  
                str(round(level_execution.memory_l1_bound_percentage_ipc_degradation(), TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + '%')
            titles : list[str] = [level_execution.memory_constant_memory_bound().name(), level_execution.memory_mio_throttle().name(), 
                level_execution.memory_l1_bound().name()]
            messages : list[list[str]] = [[stalls_memory_constant_memory_bound_on_total_message, stalls_memory_mio_throttle_on_total_message, 
            stalls_memory_l1_bound_on_total_message], [stalls_memory_constant_memory_bound_on_memory_bound_message, 
            stalls_memory_mio_throttle_on_memory_bound_message, stalls_memory_l1_bound_on_memory_bound_message], [stalls_memory_constant_memory_bound_on_back_message, 
            stalls_memory_mio_throttle_on_back_message, stalls_memory_l1_bound_on_back_message], ["","","",""], 
            [ipc_degradation_memory_constant_memory_bound_message, ipc_degradation_memory_mio_throttle_message, ipc_degradation_memory_l1_bound_message]]
            MessageFormat().print_three_msg_box(messages, titles, 1, self.output_file(), False)
        else:
            messages : str = ("\n" + stalls_memory_constant_memory_bound_on_total_message + "\n" + 
            stalls_memory_constant_memory_bound_on_memory_bound_message + "\n" + stalls_memory_constant_memory_bound_on_back_message 
            + "\n\n" + ipc_degradation_memory_constant_memory_bound_message)
            MessageFormat().print_msg_box(messages, 1, None, level_execution.memory_constant_memory_bound().name(), self.output_file(),
            False)
        
    
    def __show_results(self, level_execution):
        """ Show Results of execution indicated by argument.

        Args:
            level_execution   : LevelOne/LevelTwo/LevelThree(Nsight/Nvprof)  ; reference to level one/two/three analysis ALREADY DONE in the
        """

        delete_content : bool # check if it has to delete content 
        if self.show_verbose():
            delete_content = False
        else:
            delete_content = self.delete_output_file_content()

        printer : MessageFormat = MessageFormat()
        message : str = "The results have been obtained correctly. General results of IPC are the following:\n\n"
        printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
            output_file = self.output_file(), delete_content_file = delete_content)
        print()
        message = ("IPC OBTAINED: " + str(round(level_execution.retire_ipc(),TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + " | MAXIMUM POSSIBLE IPC: " +  
            str(level_execution.get_device_max_ipc()))
        printer.print_desplazed_msg_box(msg = message, indent = 1, title = "", output_file = self.output_file(), width = None, delete_content_file = False)
        if self.show_desc():
            message = ("\n\n'IPC OBTAINED' is the retire IPC of the analyzed program and 'MAXIMUM POSSIBLE IPC'\n" +
                "is the the maximum IPC your GPU can achieve. This is computed taking into account architectural concepts, such as the\n" +
                "number of warp planners per SM, as well as the number of Dispatch units of each SM.")
            printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), 
            delete_content_file = False)
            message = ("\n    As you can see, the IPC obtanied it " + "is " + str(round((level_execution.get_device_max_ipc()/level_execution.ipc())*100, 
                TopDownParameters.C_MAX_NUM_RESULTS_DECIMALS)) + "% smaller than you could get. This lower IPC is due to STALLS in the different \nparts "              
                + "of the architecture and DIVERGENCE problems. We analyze them based on the level of the TopDown:\n")
            printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
            print()
            
        printer.print_max_line_length_message("\n", TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False)
        message = "DESCRIPTION OF MEASURE PARTS"
        printer.print_desplazed_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
        print()
        if (type(level_execution) is LevelTwoNsight or type(level_execution) is LevelTwoNvprof or type(level_execution) is LevelThreeNvprof or 
            type(level_execution) is LevelThreeNsight):
            message = "\nLEVEL ONE RESULTS"
            printer.print_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
            printer.print_max_line_length_message("\n", TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False) 
            if self.show_desc():
                message = "\n" + level_execution.front_end().name() + ": " + level_execution.front_end().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                    output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.back_end().name() + ": " + level_execution.back_end().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                    output_file = self.output_file(), 
                delete_content_file = False)
                print()
                message = "\n" + level_execution.divergence().name() + ": " + level_execution.divergence().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()

                message = "\n" + level_execution.retire().name() + ": " + level_execution.retire().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
            self.__show_level_one_results(level_execution)
            print()
            message = "\n\nLEVEL TWO RESULTS"
            printer.print_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
            printer.print_max_line_length_message("\n", TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False)
            if self.show_desc():
                message = "\n" + level_execution.front_fetch().name() + ": " + level_execution.front_fetch().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.front_decode().name() + ": " + level_execution.front_decode().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.back_core_bound().name() + ": " + level_execution.back_core_bound().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.back_memory_bound().name() + ": " + level_execution.back_memory_bound().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.divergence_branch().name() + ": " + level_execution.divergence_branch().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.divergence_replay().name() + ": " + level_execution.divergence_replay().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()
            self.__show_level_two_results(level_execution)
            print()
            if type(level_execution) is LevelThreeNsight or type(level_execution) is LevelThreeNvprof:
                message = "\n\nLEVEL THREE RESULTS"
                printer.print_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
                print()
                if self.show_desc():
                    message = "\n" + level_execution.memory_constant_memory_bound().name() + ": " + level_execution.memory_constant_memory_bound().description() + "\n\n"
                    printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                    output_file = self.output_file(), delete_content_file = False)
                    print()
                    if type(level_execution) is LevelThreeNsight:
                        message = "\n" + level_execution.memory_l1_bound().name() + ": " + level_execution.memory_l1_bound().description() + "\n\n"
                        printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                        output_file = self.output_file(), delete_content_file = False)
                        print()
                        message = "\n" + level_execution.memory_mio_throttle().name() + ": " + level_execution.memory_mio_throttle().description() + "\n\n"
                        printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                        output_file = self.output_file(), delete_content_file = False)
                        print()
                self.__show_level_three_results(level_execution)
                print()
        else: # levelr one
            message = "RESULTS"
            printer.print_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
            print()
            if self.show_desc():
                message = "\n" + level_execution.front_end().name() + ": " + level_execution.front_end().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                    output_file = self.output_file(), delete_content_file = False)
                print()
                message = "\n" + level_execution.back_end().name() + ": " + level_execution.back_end().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                    output_file = self.output_file(), 
                delete_content_file = False)
                print()
                message = "\n" + level_execution.divergence().name() + ": " + level_execution.divergence().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()

                message = "\n" + level_execution.retire().name() + ": " + level_execution.retire().description() + "\n\n"
                printer.print_max_line_length_message(message = message, max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, 
                output_file = self.output_file(), delete_content_file = False)
                print()

            self.__show_level_one_results(level_execution)
            print()
        

    def __is_nvprof_mode(self) -> bool:
        """
        Check if the execution must be done with NVPROF scan tool.

        Returns:
            True if the execution must be done with NVPROF scan tool, or false
            if not (NSIGHT).
        """
        
        shell : Shell = Shell()
        compute_capability : str = shell.launch_command_show_all("nvcc $DIR_UNTIL_TOPDOWN/TopDownNvidia/src/measure_parts/compute_capability.cu --run", None)
        shell.launch_command("rm -f $DIR_UNTIL_TOPDOWN/TopDownNvidia/src/measure_parts/a.out", None) # delete file
        if not compute_capability:
            raise ModeExecutionError
        compute_capability_float : float = float(compute_capability)
        if compute_capability_float < 0.0:
            raise ComputeCapabilityNumberError
        if compute_capability_float > TopDownParameters.C_COMPUTE_CAPABILITY_NVPROF_MAX_VALUE:
            return False
        return True
        

    def launch(self):
        """ Launch execution."""

        if self.show_verbose():
            # introduction
            self.__intro_message()
        show_metrics : bool = self.show_metrics()
        show_events : bool = self.show_events()
        if self.show_all_measures():
            show_metrics = True
            show_events = True
        program : str = self.program()

        # check if it's python file
        if (program is not None and len(program) > 3 and program[len(program) - 3] == '.' and program[len(program) - 2] == 'p' 
            and program[len(program) - 1] == 'y'):
            program = "python3 " + program
        if self.__is_nvprof_mode():
            front_end : FrontEndNvprof
            back_end : BackEndNvprof
            divergence : DivergenceNvprof
            retire : RetireNvprof
            extra_measure : ExtraMeasureNvprof
            if self.level() == 1:
                front_end = FrontEndNvprof(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NVPROF_L1_METRICS, FrontEndParameters.C_FRONT_END_NVPROF_L1_EVENTS)
                back_end = BackEndNvprof(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION, 
                    BackEndParameters.C_BACK_END_NVPROF_L1_METRICS, BackEndParameters.C_BACK_END_NVPROF_L1_EVENTS)
                divergence = DivergenceNvprof(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NVPROF_L1_METRICS, DivergenceParameters.C_DIVERGENCE_NVPROF_L1_EVENTS)
                retire = RetireNvprof(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NVPROF_L1_METRICS, RetireParameters.C_RETIRE_NVPROF_L1_EVENTS)
                extra_measure = ExtraMeasureNvprof(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L1_METRICS, ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L1_EVENTS)
                level : LevelOneNvprof = LevelOneNvprof(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, show_events, 
                front_end, back_end, divergence, retire, extra_measure)
            elif self.level() == 2:
                front_end = FrontEndNvprof(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NVPROF_L2_METRICS, FrontEndParameters.C_FRONT_END_NVPROF_L2_EVENTS)
                back_end = BackEndNvprof(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION, 
                    BackEndParameters.C_BACK_END_NVPROF_L2_METRICS, BackEndParameters.C_BACK_END_NVPROF_L2_EVENTS)
                divergence = DivergenceNvprof(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NVPROF_L2_METRICS, DivergenceParameters.C_DIVERGENCE_NVPROF_L2_EVENTS)
                retire = RetireNvprof(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NVPROF_L2_METRICS, RetireParameters.C_RETIRE_NVPROF_L2_EVENTS)
                extra_measure = ExtraMeasureNvprof(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L2_METRICS, ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L2_EVENTS)
                front_decode : FrontDecodeNvprof = FrontDecodeNvprof(FrontDecodeParameters.C_FRONT_DECODE_NAME, 
                    FrontDecodeParameters.C_FRONT_DECODE_DESCRIPTION, FrontDecodeParameters.C_FRONT_DECODE_NVPROF_L2_METRICS, 
                    FrontDecodeParameters.C_FRONT_DECODE_NVPROF_L2_EVENTS)
                front_fetch : FrontFetchNvprof = FrontFetchNvprof(FrontFetchParameters.C_FRONT_FETCH_NAME, 
                    FrontFetchParameters.C_FRONT_FETCH_DESCRIPTION, FrontFetchParameters.C_FRONT_FETCH_NVPROF_L2_METRICS, 
                    FrontFetchParameters.C_FRONT_FETCH_NVPROF_L2_EVENTS)
                back_memory_bound : BackMemoryBoundNvprof = BackMemoryBoundNvprof(BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NAME, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_DESCRIPTION, BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NVPROF_L2_METRICS, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NVPROF_L2_EVENTS)
                back_core_bound : BackCoreBoundNvprof = BackCoreBoundNvprof(BackCoreBoundParameters.C_BACK_CORE_BOUND_NAME, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_DESCRIPTION, BackCoreBoundParameters.C_BACK_CORE_BOUND_NVPROF_L2_METRICS, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_NVPROF_L2_EVENTS)
                level : LevelTwoNvprof = LevelTwoNvprof(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, show_events, 
                front_end, back_end, divergence, retire, extra_measure, front_fetch, front_decode, back_core_bound, back_memory_bound) 
            elif self.level() == 3:
                front_end = FrontEndNvprof(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NVPROF_L3_METRICS, FrontEndParameters.C_FRONT_END_NVPROF_L3_EVENTS)
                back_end = BackEndNvprof(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION, 
                    BackEndParameters.C_BACK_END_NVPROF_L3_METRICS, BackEndParameters.C_BACK_END_NVPROF_L3_EVENTS)
                divergence = DivergenceNvprof(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NVPROF_L3_METRICS, DivergenceParameters.C_DIVERGENCE_NVPROF_L3_EVENTS)
                retire = RetireNvprof(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NVPROF_L3_METRICS, RetireParameters.C_RETIRE_NVPROF_L3_EVENTS)
                extra_measure = ExtraMeasureNvprof(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L3_METRICS, ExtraMeasureParameters.C_EXTRA_MEASURE_NVPROF_L3_EVENTS)
                front_decode : FrontDecodeNvprof = FrontDecodeNvprof(FrontDecodeParameters.C_FRONT_DECODE_NAME, 
                    FrontDecodeParameters.C_FRONT_DECODE_DESCRIPTION, FrontDecodeParameters.C_FRONT_DECODE_NVPROF_L3_METRICS, 
                    FrontDecodeParameters.C_FRONT_DECODE_NVPROF_L3_EVENTS)
                front_fetch : FrontFetchNvprof = FrontFetchNvprof(FrontFetchParameters.C_FRONT_FETCH_NAME, 
                    FrontFetchParameters.C_FRONT_FETCH_DESCRIPTION, FrontFetchParameters.C_FRONT_FETCH_NVPROF_L3_METRICS, 
                    FrontFetchParameters.C_FRONT_FETCH_NVPROF_L3_EVENTS)
                back_memory_bound : BackMemoryBoundNvprof = BackMemoryBoundNvprof(BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NAME, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_DESCRIPTION, BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NVPROF_L3_METRICS, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NVPROF_L3_EVENTS)
                back_core_bound : BackCoreBoundNvprof = BackCoreBoundNvprof(BackCoreBoundParameters.C_BACK_CORE_BOUND_NAME, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_DESCRIPTION, BackCoreBoundParameters.C_BACK_CORE_BOUND_NVPROF_L3_METRICS, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_NVPROF_L3_EVENTS)
                level : LevelThreeNvprof = LevelThreeNvprof(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, show_events, 
                front_end, back_end, divergence, retire, extra_measure, front_fetch, front_decode, back_core_bound, back_memory_bound)        
        else:
            front_end : FrontEndNsight
            back_end : BackEndNsight
            divergence : DivergenceNsight
            retire : RetireNsight
            extra_measure : ExtraMeasureNsight
            if self.level() == 1:
                front_end = FrontEndNsight(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NSIGHT_L1_METRICS)
                back_end = BackEndNsight(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION,
                    BackEndParameters.C_BACK_END_NSIGHT_L1_METRICS)
                divergence = DivergenceNsight(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NSIGHT_L1_METRICS)
                retire = RetireNsight(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NSIGHT_L1_METRICS)
                extra_measure = ExtraMeasureNsight(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NSIGHT_L1_METRICS)
                level : LevelOneNsight = LevelOneNsight(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, front_end, 
                back_end, divergence, retire, extra_measure)
            elif self.level() == 2:
                front_end = FrontEndNsight(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NSIGHT_L2_METRICS)
                back_end = BackEndNsight(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION,
                    BackEndParameters.C_BACK_END_NSIGHT_L2_METRICS)
                divergence = DivergenceNsight(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NSIGHT_L2_METRICS)
                retire = RetireNsight(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NSIGHT_L2_METRICS)
                extra_measure = ExtraMeasureNsight(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NSIGHT_L2_METRICS)
                front_decode : FrontDecodeNsight =  FrontDecodeNsight(FrontDecodeParameters.C_FRONT_DECODE_NAME, 
                    FrontDecodeParameters.C_FRONT_DECODE_DESCRIPTION, FrontDecodeParameters.C_FRONT_DECODE_NSIGHT_L2_METRICS)
                front_fetch : FrontFetchNsight =  FrontFetchNsight(FrontFetchParameters.C_FRONT_FETCH_NAME, 
                    FrontFetchParameters.C_FRONT_FETCH_DESCRIPTION, FrontFetchParameters.C_FRONT_FETCH_NSIGHT_L2_METRICS)
                back_memory_bound : BackMemoryBoundNsight =  BackMemoryBoundNsight(BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NAME, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_DESCRIPTION, BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NSIGHT_L2_METRICS)
                back_core_bound : BackCoreBoundNsight = BackCoreBoundNsight (BackCoreBoundParameters.C_BACK_CORE_BOUND_NAME, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_DESCRIPTION, BackCoreBoundParameters.C_BACK_CORE_BOUND_NSIGHT_L2_METRICS) 
                level : LevelTwoNsight = LevelTwoNsight(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, front_end, 
                back_end, divergence, retire, extra_measure, front_decode, front_fetch, back_core_bound, back_memory_bound) 
            elif self.level() == 3:
                front_end = FrontEndNsight(FrontEndParameters.C_FRONT_END_NAME, FrontEndParameters.C_FRONT_END_DESCRIPTION,
                    FrontEndParameters.C_FRONT_END_NSIGHT_L3_METRICS)
                back_end = BackEndNsight(BackEndParameters.C_BACK_END_NAME, BackEndParameters.C_BACK_END_DESCRIPTION,
                    BackEndParameters.C_BACK_END_NSIGHT_L3_METRICS)
                divergence = DivergenceNsight(DivergenceParameters.C_DIVERGENCE_NAME, DivergenceParameters.C_DIVERGENCE_DESCRIPTION,
                    DivergenceParameters.C_DIVERGENCE_NSIGHT_L3_METRICS)
                retire = RetireNsight(RetireParameters.C_RETIRE_NAME, RetireParameters.C_RETIRE_DESCRIPTION,
                    RetireParameters.C_RETIRE_NSIGHT_L3_METRICS)
                extra_measure = ExtraMeasureNsight(ExtraMeasureParameters.C_EXTRA_MEASURE_NAME, ExtraMeasureParameters.C_EXTRA_MEASURE_DESCRIPTION,
                    ExtraMeasureParameters.C_EXTRA_MEASURE_NSIGHT_L3_METRICS)
                front_decode : FrontDecodeNsight = FrontDecodeNsight(FrontDecodeParameters.C_FRONT_DECODE_NAME, 
                    FrontDecodeParameters.C_FRONT_DECODE_DESCRIPTION, FrontDecodeParameters.C_FRONT_DECODE_NSIGHT_L3_METRICS)
                front_fetch : FrontFetchNsight =  FrontFetchNsight(FrontFetchParameters.C_FRONT_FETCH_NAME, 
                    FrontFetchParameters.C_FRONT_FETCH_DESCRIPTION, FrontFetchParameters.C_FRONT_FETCH_NSIGHT_L3_METRICS)
                back_memory_bound : BackMemoryBoundNsight = BackMemoryBoundNsight(BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NAME, 
                    BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_DESCRIPTION, BackMemoryBoundParameters.C_BACK_MEMORY_BOUND_NSIGHT_L3_METRICS)
                back_core_bound : BackCoreBoundNsight = BackCoreBoundNsight(BackCoreBoundParameters.C_BACK_CORE_BOUND_NAME, 
                    BackCoreBoundParameters.C_BACK_CORE_BOUND_DESCRIPTION, BackCoreBoundParameters.C_BACK_CORE_BOUND_NSIGHT_L3_METRICS) 
                level : LevelThreeNsight = LevelThreeNsight(program, self.input_file(), self.output_file(), self.output_scan_file(), show_metrics, front_end, 
                back_end, divergence, retire, extra_measure, front_decode, front_fetch, back_core_bound, back_memory_bound) 
        lst_output : list[str] = list() # for extra information
        level.run(lst_output)
        self.__show_results(level)
        if self.show_all_measures() or self.show_metrics() or self.show_events():
            # Write results in output-file if has been specified
            printer : MessageFormat = MessageFormat()
            printer.print_max_line_length_message("\n\n", TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, self.output_file(), False)
            message : str = "List of measurements computed by NVIDIA scan tool"
            printer.print_desplazed_underlined_str(message = message, output_file = self.output_file(), delete_content_file = False)
            if not self.output_file() is None:
                    printer.write_in_file_at_end(self.output_file(), lst_output)
            element : str
            for element in lst_output:
                print(element)
        if self.show_graph():
            level.showGraph()
        if not self.output_graph_file() is None:
            level.saveGraph(self.output_graph_file())
     

if __name__ == '__main__':
    td = TopDown()
    td.launch()
    MessageFormat().print_max_line_length_message(message = "\nAnalysis performed correctly!\n", 
    max_length = TopDownParameters.C_NUM_MAX_CHARACTERS_PER_LINE, output_file = td.output_file(), delete_content_file = False)
