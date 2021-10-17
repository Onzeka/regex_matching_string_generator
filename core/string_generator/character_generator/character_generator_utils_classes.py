from typing import Dict, List
from core.string_generator.character_generator.character_generator_meta import MetaCharacterGenerator
import random
import string
from abc import abstractmethod

class UtilCharacterGenerator(MetaCharacterGenerator):
    def generate_character(self, regex_slice: str) -> str:
        character_sets = self.get_character_sets(regex_slice)
        natural_chars = []
        characters = []
        for character_set in character_sets:
            natural_chars.extend(self._pick_natural_chars_from_list(character_set))
            characters.append(random.choice(character_set))
        if natural_chars != []:
            self.update_naturalness()
            return random.choice(natural_chars)
        else : 
            return random.choice(characters)
    @abstractmethod
    def get_character_sets(self,regex:int)->List[str]:
        raise NotImplementedError

class PatternCharacterGenerator(UtilCharacterGenerator):
    def get_character_sets(self, regex_slice: str) -> str:# 'a'
        return [regex_slice]


class IdentityEscapeGenerator(UtilCharacterGenerator):
    def get_character_sets(self, regex_slice: str) -> str:# '\]'
        return [regex_slice[-1]]

class AnyCharacterGenerator(UtilCharacterGenerator):# '.'
    def get_character_sets(self, regex_slice: str) -> str:
        return [string.digits,string.ascii_uppercase,string.ascii_lowercase,string.whitespace,string.punctuation]

class CharacterClassEscapeGenerator(UtilCharacterGenerator):# '/W'
    _character_sets= {
        'w': [string.digits , string.ascii_lowercase , string.ascii_uppercase , '_'],
        's': [string.whitespace],
        'd': [string.digits]
    }
    def get_character_sets(self, regex_slice: str) -> str:
        character_class = regex_slice[-1]
        character_sets = self._character_sets.get(character_class.lower())
        if character_class.isupper():
            negated_set = self._get_negated_set_from_character_sets(character_sets)
            characters = [negated_set]
        else:
            characters = character_sets
        return characters

    def _get_negated_set_from_character_sets(self,character_sets:List[str])->str:
        set_to_negate = ''
        for character_set in character_sets:
            set_to_negate+=character_set
        return ''.join([char for char in string.printable if char not in set_to_negate])
        

class CharacterClassGenerator(UtilCharacterGenerator):#[a-z0-9]
    def get_character_sets(self, regex_slice: str) -> List[str]:
        character_class_node = self._get_regex_slice_node(regex_slice)
        children = [child for child in character_class_node.children if child.is_named]
        characters = []
        for child in children:
            child_string = self.parser.get_code(child,regex_slice)
            if child.type == 'class_range' and self._is_class_range_valid(child_string):
                characters.append(self._get_class_range_values(child_string))
            else:
                if child.type == 'class_character':
                    character_generator = CHARACTER_GENERATOR_CLASSES.get('pattern_character')(self.parser)
                else:
                    character_generator = CHARACTER_GENERATOR_CLASSES.get(child.type,PatternCharacterGenerator)(self.parser)
                characters.extend(character_generator.get_character_sets(child_string))
        return characters

    @staticmethod
    def _is_class_range_valid(class_range_string:str)->bool:
        lower_char,upper_char = class_range_string[0],class_range_string[-1]
        return ord(lower_char)<ord(upper_char) and any([lower_char in char_set and upper_char in char_set for char_set in [string.digits,string.ascii_uppercase,string.ascii_lowercase]])
    @staticmethod
    def _get_class_range_values(class_range_string:str)->str:
        lower_bound,upper_bound = string.printable.index(class_range_string[0]),string.printable.index(class_range_string[-1])
        return string.printable[lower_bound:upper_bound]

CHARACTER_GENERATOR_CLASSES:Dict[str,UtilCharacterGenerator] = {
    'pattern_character' : PatternCharacterGenerator,
    'identity_escape': IdentityEscapeGenerator,
    'any_character' : AnyCharacterGenerator,
    'character_class_escape': CharacterClassEscapeGenerator,
    'character_class': CharacterClassGenerator
}