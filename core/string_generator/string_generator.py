from sys import prefix
from typing import List,Dict, Tuple
from ponicode.parser import CodeParser,Grammar, Node
from core.automaton_path_extractor.automaton_path_extractor import Path
from core.string_generator.character_generator.character_generator import CharacterGenerator
from core.string_generator.character_mutator.character_mutator import CharacterMutator
from core.automaton_path_extractor.additional_path_generator import AdditionalPathGenerator
from core.regex_automaton.node_toolkit import NodeToolkit
import networkx as nx
import random



class StringGenerator:
    def __init__(self):
        self.parser = CodeParser(Grammar('regex'))
        self.character_generator = CharacterGenerator(self.parser)
        self.character_mutator = CharacterMutator(self.parser)

    def generate_strings_from_paths(self,automaton:nx.DiGraph,paths:List[Path])->List[str]:
        self.automaton = automaton
        self.nodetoolkit = NodeToolkit(automaton)
        self.additional_path_generator = AdditionalPathGenerator(automaton)
        self.mutated_states = set()
        generated_strings = []
        for path in paths:
            generated_strings.extend(self._generate_strings_from_path(path))
        return generated_strings
    
    def _get_mutated_strings(self,valid_path:Path)->List[str]:
        regex_slices = self._get_regex_slices_from_path(valid_path)
        base_chars = self._get_chars_from_regex_slices(regex_slices)
        mutated_strings = [''.join(base_chars)]
        for index,regex_slice in enumerate(regex_slices):
            state = valid_path[index]
            if state not in self.mutated_states:
                if self.nodetoolkit.is_regex_slice(state):
                    mutations = self.character_mutator.mutate(regex_slice,self.automaton.graph['regex'])
                    mutated_strings.extend([''.join(base_chars[:index]+[mutation]+base_chars[index+1:]) for mutation in mutations])
                self.mutated_states.add(state)
        return mutated_strings

    def _get_chars_from_regex_slices(self,regex_slices:List[str])->List[str]:
        self.character_generator.init_naturalness()
        return [self.character_generator.generate_character(regex_slice) for regex_slice in regex_slices]
        
    def _get_string_from_path(self,path:List[str]):
        regex_slices = self._get_regex_slices_from_path(path)
        return ''.join(self._get_chars_from_regex_slices(regex_slices))

    def _generate_strings_from_path(self,path:Path)-> List[str]:
        strings = []
        
        additional_paths = self.additional_path_generator.generate_additional_paths(path)
        print(additional_paths)
        strings.extend([self._get_string_from_path(additional_path) for additional_path in additional_paths])

        valid_path = self.additional_path_generator.get_valid_path_from_path(path)
        print(valid_path)
        strings.extend(self._get_mutated_strings(valid_path))

        return strings

    def _get_regex_slices_from_path(self,path:Path)-> List[str]:
        return [self.nodetoolkit.get_regex_slice(state) for state in path]


