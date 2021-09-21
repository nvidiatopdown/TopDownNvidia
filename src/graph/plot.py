import sys
import pathlib
import os.path
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import collections  as mc

#!/usr/bin/env python
# Example
class Grafica:
    def _addFeatures(self):
        # Add title and axis names
        plt.title(sys.argv[1])
        plt.xlabel(sys.argv[2])
        plt.ylabel(sys.argv[3])
        pass

    def _addData(self):
        # colours for graphs
        colourScatter = ['blue', 'red', 'orange', 'grey']
        colourPlot = ['blue', 'red', 'orange', 'grey']
        
        # introduce fileNames in array
        fileNames = sys.argv[4]    
        fileNames = fileNames.replace('[','')
        fileNames = fileNames.replace(']','')
        files = fileNames.split(',')
        
        # legends
        legendsArgument = sys.argv[5]    
        legendsArgument = legendsArgument.replace('[','')
        legendsArgument = legendsArgument.replace(']','')
        legends = legendsArgument.split(',')
        

        x_axis = []
        y_axis = []
        count = 0
        indexLegends = 0
        colourNumber = 0
        for fileName in files:
            # read file
            f = open(fileName, 'r') 
            Lines = f.readlines() 
            
            # add data
            for line in Lines: 
                lineList = line.split()
                
                for word in lineList:
                    if count == 0:
                        x_axis.append(float(word))
                        count = count + 1
                    else:
                        y_axis.append(float(word))
                        count = 0
            plt.plot(x_axis,y_axis,linestyle='solid',color=colourPlot[colourNumber], label = legends[indexLegends])
            plt.legend(legends[indexLegends])
            #plt.scatter(x_axis,y_axis,color=colourScatter[colourNumber],zorder=1)
            colourNumber = colourNumber + 1
            indexLegends = indexLegends + 1
            x_axis = []
            y_axis = []
        #plt.legend(loc=2,fancybox=True, shadow=True, ncol=1)
        plt.legend(title= 'Legend',loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tick_params(axis='both',direction='inout', length=0, width=10000, colors='black'
               ,labelsize=10)
        plt.margins(0)

        pass

    def _check_arguments(self):
        
        # Arguments Features
        MIN_NUMBER_ARGUMENTS = 6
        MAX_NUMBER_ARGUMENTS = 8
        HELP_OPTION = "help"
 
        if len(sys.argv) < MIN_NUMBER_ARGUMENTS or len(sys.argv) > MAX_NUMBER_ARGUMENTS:
            if len(sys.argv) == 1:
                print("Error with number arguments")
            elif sys.argv[1] == HELP_OPTION:
                print("python3 " + sys.argv[0] + " <title> <titleX> <titleY> [<file[0]>,<file[n]>]" +
                    ", [<legend<[0]>,<legend<[n]>] <nameFig> [<xLimStart>,<xLimEnd>,<xStep>], [<yLimStart>,<yLimEnd>,<ystep>]")
                print("python3 " + sys.argv[0] + " <title> <titleX> <titleY> [<file[0]>,<file[n]>]" +
                    ", [<legend<[0]>,<legend<[n]>] <nameFig> <x/y>[<<x/y>LimStart>,<<x/y>LimEnd>,<<x/y>Step>]")
            sys.exit()
        pass

    def _check_limits(self):
        NUMBER_ARGUMENT_WITH_SOME_LIMITS = 8
        NUMBER_ARGUMENT_WITH_ALL_LIMITS = 9
        if len(sys.argv) == NUMBER_ARGUMENT_WITH_SOME_LIMITS:
            argument = sys.argv[7]
            type_axis = argument[0]
            
            argument = argument.replace(argument[0],'')
            argument = argument.replace('[','')
            argument = argument.replace(']','')
            argument = argument.split(',')
            
            if (type_axis == 'y') or (type_axis == 'Y'):
                plt.ylim(float(argument[0]),float(argument[1]))
                plt.yticks( np.arange(float(argument[0]), float(argument[1]), step=float(argument[2])))
            elif type_axis == 'X' or type_axis == 'x':
                plt.xlim(float(argument[0]), float(argument[1]))
                plt.xticks(np.arange(float(argument[0]), float(argument[1]), step=float(argument[2])))
            else:
                print("ERROR")

        elif len(sys.argv) == NUMBER_ARGUMENT_WITH_ALL_LIMITS:
            ## X limits
            argument = sys.argv[6]
            type_axis = argument[0]
            
            argument = argument.replace(argument[0],'')
            argument = argument.replace('[','')
            argument = argument.replace(']','')
            argument = argument.split(',')

            plt.xlim(int(argument[0]), int(argument[1]))
            plt.xticks(np.arange(int(argument[0]), int(argument[1]), step=int(argument[2])))
            
            ## Y limits
            argument = sys.argv[7]
            type_axis = argument[0]
            
            argument = argument.replace(argument[0],'')
            argument = argument.replace('[','')
            argument = argument.replace(']','')
            argument = argument.split(',')

            plt.ylim(int(argument[0]), int(argument[1]))
            plt.yticks(np.arange(int(argument[0]), int(argument[1]), step=int(argument[2])))
        pass


    def main(self):
        self._check_arguments()
        self._addFeatures()
        self._addData()
        
        self._check_limits()

        # show
        plt.grid()
        plt.show()

        # set size 
        figure = plt.gcf()
        figure.set_size_inches(16, 8)
        plt.savefig(sys.argv[6], dpi=400)
    pass


# execute 
Grafica().main()
