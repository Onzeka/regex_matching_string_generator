from typing import Dict
from core.string_generator.character_generator.character_generator_meta import MetaCharacterGenerator
import random
import string



class PatternCharacterGenerator(MetaCharacterGenerator):
    def generate_character(self, regex_slice: str) -> str:# 'a'
        return regex_slice


class IdentityEscapeGenerator(MetaCharacterGenerator):
    def generate_character(self, regex_slice: str) -> str:# '\]'
        return regex_slice[-1]

class AnyCharacterGenerator(MetaCharacterGenerator):# '.'
    def generate_character(self, regex_slice: str) -> str:
        return self._pick_natural_char(string.printable)

class CharacterClassEscapeGenerator(MetaCharacterGenerator):# '/W'
    _class_sets_characters= {
        'w': string.digits + string.ascii_lowercase + string.ascii_uppercase + '_',
        's': string.whitespace,
        'd': string.digits
    }
    def generate_character(self, regex_slice: str) -> str:
        character_class = regex_slice[-1]
        class_set_characters = self._class_sets_characters.get(character_class.lower())
        if character_class.islower():
            characters = class_set_characters
        else:
            characters = [character for character in string.printable if character not in class_set_characters]
        return self._pick_natural_char(characters)


class CharacterClassGenerator(MetaCharacterGenerator):#[a-z0-9]
    def generate_character(self, regex_slice: str) -> str:
        character_class_node = self._get_regex_slice_node(regex_slice)
        children = [child for child in character_class_node.children if child.is_named]
        characters = []
        for child in children:
            child_string = self.parser.get_code(child,regex_slice)
            if child.type == 'class_range' and self._is_class_range_valid(child_string):
                characters.append(self._pick_natural_char(self._get_class_range_values(child_string)))
            else:
                if child.type == 'class_character':
                    character_generator = CHARACTER_GENERATOR_CLASSES.get('pattern_character')(self.parser)
                else:
                    character_generator = CHARACTER_GENERATOR_CLASSES.get(child.type,PatternCharacterGenerator)(self.parser)
                characters.append(character_generator.generate_character(child_string))
        return random.choice(characters)

    @staticmethod
    def _is_class_range_valid(class_range_string:str)->bool:
        lower_char,upper_char = class_range_string[0],class_range_string[-1]
        return ord(lower_char)<ord(upper_char) and any([lower_char in char_set and upper_char in char_set for char_set in [string.digits,string.ascii_uppercase,string.ascii_lowercase]])
    @staticmethod
    def _get_class_range_values(class_range_string:str)->str:
        lower_bound,upper_bound = string.printable.index(class_range_string[0]),string.printable.index(class_range_string[-1])
        return string.printable[lower_bound:upper_bound]

CHARACTER_GENERATOR_CLASSES:Dict[str,MetaCharacterGenerator] = {
    'pattern_character' : PatternCharacterGenerator,
    'identity_escape': IdentityEscapeGenerator,
    'any_character' : AnyCharacterGenerator,
    'character_class_escape': CharacterClassEscapeGenerator,
    'character_class': CharacterClassGenerator
}