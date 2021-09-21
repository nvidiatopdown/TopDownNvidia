"""
Program that shows messages in different format.

@date:      Jan-2021
@version:   1.0
"""

import textwrap # text message
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from errors.message_format_errors import *

class MessageFormat:
    """Class with different methods to show messages."""
    
    def __write_str_in_file(self, str_to_write : str, output_file : str, delete_content_file : bool):
        """ Write string ((if it's correct) in file.

        Params:
            str_to_write            : str   ; string to write
            output_file             : str   ; path to file
            delete_content_file     : bool  ; True if you want to delete content of file before write or
                                                false if you want to add 'str_to_write' at the end of file
        """
        
        if not output_file is None:
            try:
                option : str = "w" # by default
                if not delete_content_file:
                    option = "a"
                f : _io.TextIOWrapper = open(output_file, option)
                try:
                    #f.write("\n".join(str(item) for item in message))
                    f.write(str_to_write)

                finally:
                    f.close()
            except:  
                raise WriteInOutPutFileError
        

    def print_msg_box(self, msg, indent, width, title, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        lines = msg.split('\n')
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
        if title:
            box += f'║{space}{title:<{width}}{space}║\n'  # title
            box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
        box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
        box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_center_msg_box(self, msg, indent, width, title, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        lines = msg.split('\n')
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'\t\t\t\t\t\t\t╔{"═" * (width + indent * 2)}╗\n'  # upper_border
        if title:
            box += f'\t\t\t\t\t\t\t║{space}{title:<{width}}{space}║\n'  # title
            box += f'\t\t\t\t\t\t\t║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
        box += ''.join([f'\t\t\t\t\t\t\t║{space}{line:<{width}}{space}║\n' for line in lines])
        box += f'\t\t\t\t\t\t\t╚{"═" * (width + indent * 2)}╝'  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_four_msg_box(self, msgs, titles, indent, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        width1 = len(msgs[0][0])
        width2 = len(msgs[0][1])
        width3 = len(msgs[0][2])
        width4 = len(msgs[0][3])
        for i in range(1, len(msgs)):
            if width1 < len(msgs[i][0]):
                width1 = len(msgs[i][0])
            if width2 < len(msgs[i][1]):
                width2 = len(msgs[i][1])
            if width3 < len(msgs[i][2]):
                width3 = len(msgs[i][2])
            if width4 < len(msgs[i][3]):
                width4 = len(msgs[i][3])
    
        space = " " * indent
        box = f'╔{"═" * (width1 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width2 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width3 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width4 + indent * 2)}╗\n'
        if titles:
            box += f'║{space}{titles[0]:<{width1}}{space}║  '  # title
            box += f'║{space}{titles[1]:<{width2}}{space}║  '  # title
            box += f'║{space}{titles[2]:<{width3}}{space}║  '  # title
            box += f'║{space}{titles[3]:<{width4}}{space}║\n'  # title
            box += f'║{space}{"-" * len(titles[0]):<{width1}}{space}║  '  # underscore
            box += f'║{space}{"-" * len(titles[1]):<{width2}}{space}║  '  # underscore
            box += f'║{space}{"-" * len(titles[2]):<{width3}}{space}║  '  # underscore  
            box += f'║{space}{"-" * len(titles[3]):<{width4}}{space}║\n'  # underscore
        
        for i in range(0, len(msgs)):
            box += ''.join(f'║{space}{msgs[i][0]:<{width1}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][1]:<{width2}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][2]:<{width3}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][3]:<{width4}}{space}║  ')
            box += "\n"
        box += f'╚{"═" * (width1 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width2 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width3 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width4 + indent * 2)}╝  '  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        
 
    def print_three_msg_box(self, msgs, titles, indent, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        width1 = len(msgs[0][0])
        width2 = len(msgs[0][1])
        width3 = len(msgs[0][2])
        for i in range(1, len(msgs)):
            if width1 < len(msgs[i][0]):
                width1 = len(msgs[i][0])
            if width2 < len(msgs[i][1]):
                width2 = len(msgs[i][1])
            if width3 < len(msgs[i][2]):
                width3 = len(msgs[i][2])
    
        space = " " * indent
        box = f'╔{"═" * (width1 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width2 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width3 + indent * 2)}╗\n'  # upper_border
        if titles:
            box += f'║{space}{titles[0]:<{width1}}{space}║  '  # title
            box += f'║{space}{titles[1]:<{width2}}{space}║  '  # title
            box += f'║{space}{titles[2]:<{width3}}{space}║\n'  # title
            box += f'║{space}{"-" * len(titles[0]):<{width1}}{space}║  '  # underscore
            box += f'║{space}{"-" * len(titles[1]):<{width2}}{space}║  '  # underscore
            box += f'║{space}{"-" * len(titles[2]):<{width3}}{space}║\n'  # underscore  
        
        for i in range(0, len(msgs)):
            box += ''.join(f'║{space}{msgs[i][0]:<{width1}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][1]:<{width2}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][2]:<{width3}}{space}║  ')
            box += "\n"
        box += f'╚{"═" * (width1 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width2 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width3 + indent * 2)}╝  '  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_two_msg_box(self, msgs, titles, indent, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        width1 = len(msgs[0][0])
        width2 = len(msgs[0][1])
        for i in range(1, len(msgs)):
            if width1 < len(msgs[i][0]):
                width1 = len(msgs[i][0])
            if width2 < len(msgs[i][1]):
                width2 = len(msgs[i][1])
    
        space = " " * indent
        box = f'╔{"═" * (width1 + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width2 + indent * 2)}╗\n'  # upper_border
        if titles:
            box += f'║{space}{titles[0]:<{width1}}{space}║  '  # title
            box += f'║{space}{titles[1]:<{width2}}{space}║\n'  # title
            box += f'║{space}{"-" * len(titles[0]):<{width1}}{space}║  '  # underscore
            box += f'║{space}{"-" * len(titles[1]):<{width2}}{space}║\n'  # underscore
        
        for i in range(0, len(msgs)):
            box += ''.join(f'║{space}{msgs[i][0]:<{width1}}{space}║  ')
            box += ''.join(f'║{space}{msgs[i][1]:<{width2}}{space}║  ')
            box += "\n"
        box += f'╚{"═" * (width1 + indent * 2)}╝  '  # lower_border
        box += f'╚{"═" * (width2 + indent * 2)}╝  '  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_desplazed_msg_box(self, msg, indent, width, title, output_file : str, delete_content_file : bool):
        """Print message-box with optional title."""

        lines = msg.split('\n')
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'\t\t\t\t\t╔{"═" * (width + indent * 2)}╗\n'  # upper_border
        if title:
            box += f'\t\t\t\t\t║{space}{title:<{width}}{space}║\n'  # title
            box += f'\t\t\t\t\t║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
        box += ''.join([f'\t\t\t\t\t║{space}{line:<{width}}{space}║\n' for line in lines])
        box += f'\t\t\t\t\t╚{"═" * (width + indent * 2)}╝\n'  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_n_per_line_msg_box(self, matrix : list, titles, indent, width, output_file : str, delete_content_file : bool):
        """Print message-box with optional title.""" # NOT USED. DONT USE

        lines = matrix[0][0].split('\n') # by default
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = ""
        for i in range(len(titles) - 1):
            box += f'╔{"═" * (width + indent * 2)}╗  '  # upper_border
        box += f'╔{"═" * (width + indent * 2)}╗\n'
        if len(titles) > 1:
            for i in range(len(titles)):
                if i == len(titles) - 1:
                    box += f'║{space}{titles[i]:<{width}}{space}║\n'  # title
                else:
                    box += f'║{space}{titles[i]:<{width}}{space}║  '  # title
            for i in range(len(titles)):
                if i == len(titles) - 1:
                    box += f'║{space}{"-" * len(titles[i]):<{width}}{space}║\n'  # underscore
                else:
                    box += f'║{space}{"-" * len(titles[i]):<{width}}{space}║  '  # underscore
        num_ite : int = 0
        for i in range(len(matrix)):
            if i == len(matrix) - 1:
                box += "\n"
            for j in range(len(matrix[i])):
                if num_ite ==  len(matrix)*len(matrix[0])- 1 :
                    box += f'║{space}{matrix[i][j]:<{width}}{space}║\n'
                else:
                    box += f'║{space}{matrix[i][j]:<{width}}{space}║  '
            num_ite = num_ite + 1
        box += "\n"
        for i in range(len(matrix[0])):
            box += f'╚{"═" * (width + indent * 2)}╝  '  # lower_border
        print(box)
        self.__write_str_in_file(box, output_file, delete_content_file)
        

    def print_max_line_length_message(self, message : str, max_length : int, output_file : str, delete_content_file : bool):
        """Print Message with max length per line."""

        print('\n'.join(textwrap.wrap(message, max_length, break_long_words = False)))
        if not output_file is None:
            self.__write_str_in_file(message, output_file, delete_content_file)
        

    def write_in_file_at_end(self, file : str, message : list):
        """
        Write 'message' at the end of file with path 'file'

        Params:
            file    : str           ; path to file to write.
            
            message : list     ; list of string with the information to be written (in order) to file.
                                      Each element of the list corresponds to a line.

        Raises:
            WriteInOutPutFileError  ; error when opening or write in file. Operation not performed
        """

        try:
            f : _io.TextIOWrapper = open(file, "a")
            try:
                f.write("\n".join(str(item) for item in message))

            finally:
                f.close()
        except:  
            raise WriteInOutPutFileError
        

    def print_underlined_str(self, message : str, output_file : str, delete_content_file : bool):
        """ Print a string underlined. """
        message_underlined : str = self.underlined_str(message)
        print(message_underlined)
        if not output_file is None:
            self.__write_str_in_file(message_underlined, output_file, delete_content_file)
        

    def print_desplazed_underlined_str(self, message : str, output_file : str, delete_content_file : bool):
        """ Print a desplazed string underlined. """

        #message : str = '{:s}'.format('\u0332'.join(message))
        #message : str = '{:s}'.format('\u0332'.join(" " + message))
        #message = "\t\t\t\t\t" + message
        #print(message)
        
        leng : int = len(message)
        message = "\t\t\t\t\t" + message
        message  += "\n\t\t\t\t\t" + f'{"-" * (leng)}\n'
        print(message)

        if not output_file is None:
            self.__write_str_in_file(message, output_file, delete_content_file)
        

    def underlined_str(self, message : str) -> str:
        """ Returns a string underlined. """
        #return '{:s}'.format('\u0332'.join(" " + message))
        leng : int = len(message)
        message  += "\n" + f'{"-" * (leng)}\n'
        return message 
        
