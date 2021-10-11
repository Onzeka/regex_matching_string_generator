from typing import List, Set
import networkx as nx
from core.regex_automaton.node_toolkit import NodeToolkit
from core.automaton_path_extractor.automaton_path_extractor import Path
import random

class AdditionalPathGenerator:
    def __init__(self,automaton:nx.DiGraph) -> None:
        self.node_toolkit = NodeToolkit(automaton)
        self.mutated_states = set()

    def _get_loop_path_from_path(self,path:Path)-> Path:#generate a valid path with loops
        for state in reversed(path):
            if self.node_toolkit.is_loop(state):
                path_prefix,path_suffix,to_loop_path = self.node_toolkit.get_prefix_suffix_to_loop_path(state,path)
                lower_iteration_number,upper_iteration_number = self.node_toolkit.get_lower_and_upper_iteration_number(state)
                loop_iteration = random.randint(max(1,lower_iteration_number),upper_iteration_number)
                loop_path_prefix = self._get_loop_path_from_path(path_prefix)
                loop_path = self._get_loop_path_from_to_loop_path(to_loop_path,loop_iteration)#recursive
                loop_path_suffix = self._get_loop_path_from_path(path_suffix)
                return loop_path_prefix + loop_path + loop_path_suffix
        return path

    def _get_loop_path_from_to_loop_path(self,to_loop_path:Path,loop_iteration:int)->Path:
        loop_path = []
        for _ in range(loop_iteration):
            loop_path.extend(self._get_loop_path_from_path(to_loop_path))
        return loop_path
    
    def generate_additional_paths(self,path:Path)->List[Path]:
        additional_paths = [self._get_loop_path_from_path(path)]
        for state in reversed(path):
            if self.node_toolkit.is_loop(state):
                path_prefix,path_suffix,to_loop_path = self.node_toolkit.get_prefix_suffix_to_loop_path(state,path)
                #get mutations from prefix
                loop_path = self._get_loop_path_from_path(to_loop_path)
                additional_paths.extend([mutated_prefix + loop_path + path_suffix for mutated_prefix in self.generate_additional_paths(path_prefix)])
                #get mutations from to_loop_path
                prefix_loop_path = self._get_loop_path_from_path(path_prefix)
                loop_iterations = self._get_mutated_loop_iterations(state)
                for loop_iteration in loop_iterations:
                    additional_paths.append(prefix_loop_path + self._get_loop_path_from_to_loop_path(to_loop_path,loop_iteration)+path_suffix)
                return additional_paths
        return additional_paths
    def get_valid_path_from_path(self,path:Path)->str:
        return self._get_loop_path_from_path(path)
    
    def _get_mutated_loop_iterations(self,state:int)-> List[int]:
        lower_iteration_number,upper_iteration_number = self.node_toolkit.get_lower_and_upper_iteration_number(state)
        if state in self.mutated_states : 
            loop_iterations = [random.randint(max(1,lower_iteration_number),upper_iteration_number)]
        else :
            self.mutated_states.add(state)
            loop_iterations = list(set([random.randrange(lower_iteration_number),lower_iteration_number,upper_iteration_number,random.randrange(upper_iteration_number+1,upper_iteration_number+7)]))
        return loop_iterations