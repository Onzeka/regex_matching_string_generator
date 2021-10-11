from __future__ import annotations
from typing import Callable, Dict
from networkx.algorithms.shortest_paths.unweighted import single_target_shortest_path
from ponicode.parser import CodeParser,Grammar, Node
import networkx as nx
from copy import copy

LOOP_TYPE = ['one_or_more','zero_or_more','count_quantifier']

class RegexAutomatonBuilder:
    def __init__(self):
        self.parser = CodeParser(Grammar('regex'))
    
    def build_regex_automaton(self,regex:str)-> nx.DiGraph:
        self.current_automaton_state = 0
        self.regex = regex
        regex_node = self.parser.parse(regex).root_node.children[0]
        automaton = self._build_regex_automaton(regex_node,0)
        automaton.graph.update({'regex':regex})
        return automaton

    def _build_regex_automaton(self,regex_node:Node,entry_state)-> nx.DiGraph:
        state_specs_getter = RegexAutomatonBuilder.StateSpecsGetter(self,entry_state)
        node_type = regex_node.type
        building_function = self._building_functions.get(node_type,RegexAutomatonBuilder._build_simple_automaton)
        return building_function(self,regex_node,state_specs_getter)

    def _build_term_automaton(self,term_node:Node,state_specs_getter:RegexAutomatonBuilder.StateSpecsGetter)->nx.DiGraph:
        term_automaton = self._init_automaton(state_specs_getter)
        children = term_node.children
        for child in children: 
            child_automaton = self._build_regex_automaton(child,max(term_automaton.nodes))
            term_automaton = nx.compose(child_automaton,term_automaton)
        return term_automaton
    
    
    def _build_disjunction_automaton(self,disjunction_node:Node,state_specs_getter:RegexAutomatonBuilder.StateSpecsGetter)->nx.DiGraph:
        disjunction_parts = [child for child in disjunction_node.children if child.is_named]
        
        disjunction_parts_automatons = [self._build_term_automaton(disjunction_part,state_specs_getter) for disjunction_part in disjunction_parts ]

        disjunction_automaton= self._init_automaton(state_specs_getter)
        exit_state_spec = state_specs_getter.get_exit_state_specs()
        disjunction_automaton.add_node(**exit_state_spec)
        for disjunction_part_automaton in disjunction_parts_automatons:
            disjunction_part_automaton.add_edge(max(disjunction_part_automaton.nodes),exit_state_spec['node_for_adding'])
            disjunction_automaton = nx.compose(disjunction_automaton, disjunction_part_automaton)
        disjunction_automaton.graph.update(({'exit_state':exit_state_spec['node_for_adding']}))
        return disjunction_automaton

    def _build_simple_automaton(self,simple_node:Node,state_specs_getter:RegexAutomatonBuilder.StateSpecsGetter)->nx.DiGraph:
        automaton = nx.DiGraph()
        entry_node_specs = state_specs_getter.get_state_specs()
        simple_node_specs = state_specs_getter.get_state_specs(simple_node)
        automaton.add_node(**entry_node_specs)
        automaton.add_node(**simple_node_specs)
        automaton.add_edge(entry_node_specs["node_for_adding"],simple_node_specs['node_for_adding'])
        automaton.graph.update({'exit_state':simple_node_specs['node_for_adding']})
        return automaton

    def _build_capturing_group(self,capturing_group_node:Node,state_specs_getter:RegexAutomatonBuilder.StateSpecsGetter)->nx.DiGraph:
        encapsuled_node = capturing_group_node.children[1].children[0]
        return self._build_regex_automaton(encapsuled_node,state_specs_getter.entry_state)

    _building_functions: Dict[str, Callable[["RegexAutomatonBuilder", Node, int], nx.DiGraph]] = {
        'term':_build_term_automaton,
        'disjunction':_build_disjunction_automaton,
        'anonymous_capturing_group': _build_capturing_group
    }

    def _init_automaton(self,states_space_getter:RegexAutomatonBuilder.StateSpecsGetter)->nx.DiGraph:
        automaton = nx.DiGraph()
        node_specs = states_space_getter.get_state_specs()
        automaton.add_node(**node_specs)
        return automaton

    class StateSpecsGetter:
        def __init__(self,outer:"RegexAutomatonBuilder",entry_state:int=None) -> None:
            self.outer = outer
            self.entry_state = entry_state
            self.prev_automaton_state = outer.current_automaton_state
        def get_state_specs(self,node:Node=None):
            if node == None : 
                state_specs =  {'node_for_adding':self.entry_state,'type':'control','regex_slice':''}
            else :
                self.outer.current_automaton_state += 1
                
                if node.type in LOOP_TYPE:
                    state_specs = self._get_loop_control_specs(node)
                else:
                    state_specs = self._get_regex_slices_specs(node)
                self.prev_automaton_state += 1 
            return state_specs

        def _get_loop_control_specs(self,loop_node:Node)->Dict:
            if loop_node.type == 'one_or_more':
                lower_iteration_number = 1
                upper_iteration_number = None
            elif loop_node.type == 'zero_or_more':
                lower_iteration_number = 0
                upper_iteration_number = None
            #else : deal with count_quantifier
            specs =  {'node_for_adding':self.outer.current_automaton_state,
            'type':'loop_control',
            'loop_start_state':self.prev_automaton_state,
            'lower_iteration_number':lower_iteration_number,
            'upper_iteration_number':upper_iteration_number,
            'regex_slice':''}
            return specs

        def _get_regex_slices_specs(self,regex_slice_node:Node)->Dict:
            regex_slice = self.outer.parser.get_code(regex_slice_node, self.outer.regex)
            return {'node_for_adding':self.outer.current_automaton_state,'type':'regex_slice','regex_slice':regex_slice}
        def get_exit_state_specs(self)->Dict:
            self.outer.current_automaton_state += 1
            return {'node_for_adding':self.outer.current_automaton_state,'type':'control','regex_slice':''}

        

