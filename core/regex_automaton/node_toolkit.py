import networkx as nx
from core.automaton_path_extractor.automaton_path_extractor import Path
class NodeToolkit:
    def __init__(self,automaton:nx.DiGraph):
         self.automaton = automaton
            
    def is_loop(self,state:int)->bool:
        automaton_node = self.automaton.nodes[state]
        return automaton_node['type'] == 'loop_control'
    def is_regex_slice(self,state:int)->bool:
        automaton_node = self.automaton.nodes[state]
        return automaton_node['type'] == 'regex_slice'

    def get_prefix_suffix_to_loop_path(self,state:int,path: Path):
        loop_node = self.automaton.nodes[state]
        path_prefix = [prefix_state for prefix_state in path if prefix_state < loop_node['loop_start_state']]
        path_suffix = [suffix_state for suffix_state in path if suffix_state > state]
        to_loop_path = [to_loop_state for to_loop_state in path if to_loop_state >= loop_node['loop_start_state'] and to_loop_state < state]
        return path_prefix,path_suffix,to_loop_path

    def get_lower_and_upper_iteration_number(self,state):
        loop_node = self.automaton.nodes[state]
        lower_iteration_number,upper_iteration_number = loop_node['lower_iteration_number'],loop_node['upper_iteration_number']
        if lower_iteration_number == None : lower_iteration_number = 0
        if upper_iteration_number == None : upper_iteration_number = lower_iteration_number+1
        return lower_iteration_number, upper_iteration_number
    
    def get_regex_slice(self,state:int)->str:
        return self.automaton.nodes[state]['regex_slice']