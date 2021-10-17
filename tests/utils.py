from typing import List
from core.regex_automaton.regex_automaton_builder import RegexAutomatonBuilder
from core.automaton_path_extractor.automaton_path_extractor import AutomatonPathExtractor
from core.automaton_path_extractor.additional_path_generator import AdditionalPathGenerator
from core.string_generator.string_generator import StringGenerator


def generate_strings_from_regex(regex:str)->List[str]:
    builder = RegexAutomatonBuilder()
    automaton = builder.build_regex_automaton(regex)
    paths = AutomatonPathExtractor().find_basis_paths(automaton)
    strings = StringGenerator().generate_strings_from_paths(automaton,paths)
    return strings