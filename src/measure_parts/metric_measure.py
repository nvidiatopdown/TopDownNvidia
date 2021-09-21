"""
Measurements made by the TopDown methodology.

@date:      Jan-2021
@version:   1.0
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from errors.metric_measure_errors import * 
from abc import ABC # abstract class

class MetricMeasure(ABC):
    """
    Class that implements the metrics used 
    to analyze the TopDown methodology over NVIDIA's GPUs.
    
    Attributes:
        _name              : str   ;   measure name.
        
        _description       : str   ;   description with information.
        
        _metrics           : dict  ;   dictionary with metric name as key, 
                                        and value of metric as value.
        
        _metrics_desc      : dict  ;   dictionary with metric name as key, 
                                        and description of metric as value.

        _metrics_str       : str   ;   string with the metrics
    """

    def __init_dictionaries(self, metrics : str):
        """
        Initialize data structures in the correct way.
        
        Args:

            metrics             : str   ;   string with the metrics   
        """

        self._metrics : dict = dict()
        self._metrics_desc : dict = dict()
        if metrics != "":
            self._metrics = dict.fromkeys(metrics.replace(" ", "").split(","))
            self._metrics_desc = dict.fromkeys(metrics.replace(" ", "").split(",")) 

        key_metrics : str
        for key_metrics in self._metrics:
            self._metrics[key_metrics] = list()
            self._metrics_desc[key_metrics] = list()
        self._metrics_str : str = metrics
        

    def __check_data_structures(self): 
        """
        Check all data structures for events and metrics are consistent.
        In case they are not, raise exception.

        Raises:
            DataStructuresOfMetricError  ; if metric is not defined in all data structures
        """

        metric_name : str
        for metric_name in self._metrics: 
            if not metric_name in self._metrics_desc:
                raise DataStructuresOfMetricError(metric_name)
        

    def __init__(self, name : str, description : str, metrics : str):
        """
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics   
        """

        self._name : str = name
        self._description : str = description
        self.__init_dictionaries(metrics)
        self.__check_data_structures() # check dictionaries defined correctly
        

    def is_metric(self, metric_name : str) -> bool:
        """
        Check if argument it's a metric or not

        Args:
            metric_name  : str   ; name of the metric

        Returns:
            True if 'metric_name' it's a correct metric or False in other case
        """

        is_in_metrics : bool = metric_name in self._metrics
        is_in_metrics_desc : bool = metric_name in self._metrics_desc
        
        if not (is_in_metrics and is_in_metrics_desc):
            return False
        return True
        
    
    def get_metric_value(self, metric_name : str):# -> list[str]:
        """
        Get the value/s associated with 'metric_name'

        Args:
            metric_name  : str   ; name of the metric

        Returns:
            List with associated value/s 'metric_name' or 'None' if
            'metric_name' doesn't exist or it's not a metric

        """

        if not self.is_metric(metric_name):
            return None
        return self._metrics.get(metric_name)
        

    def set_metric_value(self, metric_name : str, new_value : str) -> bool:
        """
        Update metric with key 'metric_name' with 'new_value' value if 'metric_name' exists.

        Args:
            metric_name     : str   ; name of the metric
            new_value       : str   ; new value to assign to 'metric_name' if name exists
        
        Returns:
            True if the operation was perfomed succesfully or False if not because 'metric_name'
            does not correspond to any metric
        """

        if not (metric_name in self._metrics):
            return False
        
        self._metrics[metric_name].append(new_value)
        return True
        

    def name(self) -> str:
        """ 
        Return measure name.
        
        Returns:
            String with the measure name
        """

        return self._name
        
    
    def description(self) -> str:
        """ 
        Return the description with information.
        
        Returns:
            String with the description
        """
        
        return self._description
        

    def metrics(self) -> dict: 
        """ 
        Return the metrics and their values.
        
        Returns:
            Dictionary with the metrics and their values
        """

        return self._metrics # mirar retornar copias
        

    def metrics_description(self) -> dict: 
        """ 
        Return the metrics and their descriptions.
        
        Returns:
            Dictionary with the metrics and their descriptions
        """

        return self._metrics_desc # mirar retornar copias
        

    def metrics_str(self) -> str:
        """ 
        Returns a string with the metrics

        Returns:
            String with the metrics
        """

        return self._metrics_str
        

class MetricMeasureNsight(MetricMeasure):
    """
    Class that implements the metrics used 
    to analyze the TopDown methodology over NVIDIA's GPUs with
    with nvprof scan tool.
    """
             
    def __init__(self, name : str, description : str, metrics : str):
        """
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
         
        """
        
        super().__init__(name, description, metrics)    
        

    def set_metric_unit(self, metric_name : str, new_unit : str) -> bool:
        """
        Update metric with key 'metric_name' with 'new_value' description if 'metric_name' exists.
        Args:
            metric_name         : str   ; name of the metric
            new_unit     	: str   ; unit to assign to 'metric_name' if name exists
        
        Returns:
            True if the operation was perfomed succesfully or False if not because 'metric_name'
            does not correspond to any metric
        """

        if not metric_name in self._metrics:
            return False
        self._metrics_desc[metric_name] = new_unit
        return True
        
    
    def get_metric_unit(self, metric_name : str) -> str:
        """
        Get the value/s associated with 'metric_name'

        Args:
            metric_name  : str   ; name of the metric

        Returns:
            List with associated value/s 'metric_name' or 'None' if
            'metric_name' doesn't exist or it's not a metric

        """

        if not self.is_metric(metric_name):
            return None
        return self._metrics_desc.get(metric_name)
        

class MetricMeasureNvprof(MetricMeasure):
    """
    Class that implements the metrics and events used 
    to analyze the TopDown methodology over NVIDIA's GPUs with
    with nvprof scan tool.

    Attributes:
        __events            : dict  ;   dictionary with event name as key, 
                                        and value of event as value.
        
        __events_desc       : dict  ;   dictionary with events name as key, 
                                        and description of events as value.
                                        
        __events_str        : str   ;   string with the events
    """

    def __init__(self, name : str, description : str, metrics : str, events : str):
        """
        Set attributtes with argument values.
        
        Args:
            
            name                : str   ;   measure name.
        
            description         : str   ;   description with information.
        
            metrics             : str   ;   string with the metrics
        
            events              : str   ;   string with events
        """

        super().__init__(name, description, metrics)
        self.__init_dictionaries(events)
        self.__check_data_structures() # check dictionaries defined correctly
        
    
    def __init_dictionaries(self, events : str):
        """ 
        Initialize data structures in the correct way.
        
        Args:

            events              : str   ;   string with events

        """

        self.__events : dict = dict()
        self.__events_desc : dict = dict()
        if events != "":
            self.__events = dict.fromkeys(events.replace(" ", "").split(","))
            self.__events_desc = dict.fromkeys(events.replace(" ", "").split(","))
        key_events : str
        for key_events in self.__events:
            self.__events[key_events] = list()
            self.__events_desc[key_events] = list()
        self.__events_str : str = events
        

    def __check_data_structures(self): 
        """
        Check all data structures for events and metrics are consistent.
        In case they are not, raise exception.

        Raises:
            DataStructuresOfEventError  ; if event is not defined in all data structures
        """

        event_name : str
        for event_name in self.__events: 
            if not event_name in self.__events_desc:
                raise DataStructuresOfEventError(event_name)
        
                
    def get_event_value(self, event_name : str):# -> list[str]:
        """
        Get the value/s associated with 'event_name'

        Args:
            event_name  : str   ; name of the event

        Returns:
            List with associated value/s to 'event_name' or 'None' if
            'event_name' doesn't exist or it's not an event

        """

        if self.is_metric(event_name) or not self.is_event(event_name):
            return None
        return self.__events.get(event_name)
        

    def get_event_description(self, event_name : str):# -> list[str]:
        """
        Get the description/s associated with 'event_name'

        Args:
            event_name  : str   ; name of the event

        Returns:
            List with associated description/s to 'event_name' or 'None' if
            'event_name' doesn't exist or it's not an event

        """

        if self.is_metric(event_name) or not self.is_event(event_name):
            return None
        return self._events_desc.get(event_name)
        

    def get_metric_description(self, event_name : str):# -> list[str]:
        """
        Get the description/s associated with 'event_name'

        Args:
            event_name  : str   ; name of the event

        Returns:
            List with associated description/s to 'event_name' or 'None' if
            'event_name' doesn't exist or it's not an event

        """

        if self.is_metric(event_name) or not self.is_event(event_name):
            return None
        return self._metrics_desc.get(event_name)
        

    def set_metric_description(self, metric_name : str, new_description : str) -> bool:
        """
        Update metric with key 'metric_name' with 'new_value' description if 'metric_name' exists.
        Args:
            metric_name         : str   ; name of the metric
            new_description     : str   ; new description to assign to 'metric_name' if name exists
        
        Returns:
            True if the operation was perfomed succesfully or False if not because 'metric_name'
            does not correspond to any metric
        """

        if not metric_name in self._metrics:
            return False
        self._metrics_desc[metric_name] = new_description
        return True
        

    def is_event(self, event_name : str) -> bool:
        """
        Check if argument it's an event or not

        Args:
            event_name  : str   ; name of the event

        Returns:
            True if 'event_name' it's a correct event or False in other case
        """

        is_in_events : bool = event_name in self.__events
        is_in_events_desc : bool = event_name in self.__events_desc
        
        if not (is_in_events and is_in_events_desc):
            return False
        return True
        

    def set_event_value(self, event_name : str, new_value : str) -> bool:
        """
        Update event with key 'event_name' with 'new_value' value if 'event_name' exists.

        Args:
            event_name     : str   ; name of the event
            new_value       : str   ; new value to assign to 'event_name' if name exists
        
        Returns:
            True if the operation was perfomed succesfully or False if not because 'event_name'
            does not correspond to any event
        """

        if not (event_name in self.__events):
            return False
        self.__events[event_name].append(new_value)
        return True
        

    def set_event_description(self, event_name : str, new_description : str) -> bool:
        """
        Update event with key 'event_name' with 'new_value' description if 'event_name' exists.
        Args:
            event_name     : str   ; name of the event
            new_value       : str   ; new description to assign to 'event_name' if name exists
        
        Returns:
            True if the operation was perfomed succesfully or False if not because 'event_name'
            does not correspond to any event
        """

        if not (event_name in self._event):
            return False
        self._events_desc[event_name] = new_description
        return True
        

    def events(self) -> dict: 
        """ 
        Return the events and their values.
        
        Returns:
            Dictionary with the events and their values
        """
        
        return self.__events # mirar retornar copias
        

    def events_description(self) -> dict: 
        """ 
        Return the events and their descriptions.
        
        Returns:
            Dictionary with the events and their descriptions
        """

        return self.__events_desc # mirar retornar copias
        

    def events_str(self) -> str:
        """ 
        Returns a string with the events

        Returns:
            String with the events
        """

        return self.__events_str
        
