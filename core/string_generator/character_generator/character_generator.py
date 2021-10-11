from typing import Dict
from core.string_generator.character_generator.character_generator_meta import MetaCharacterGenerator
from core.string_generator.character_generator.character_generator_utils_classes import CHARACTER_GENERATOR_CLASSES



class CharacterGenerator(MetaCharacterGenerator):

    def generate_character(self,regex_slice:str)->str:
        print(self.naturalness_provider.current_string,self.naturalness_provider.cursor)
        character = ""
        if regex_slice != "":
            regex_slice_node_type = self._get_regex_slice_node(regex_slice).type
            character_generator_type = CHARACTER_GENERATOR_CLASSES.get(regex_slice_node_type)
            if character_generator_type != None:
                character_generator = character_generator_type(self.parser)
                character = character_generator.generate_character(regex_slice)
        return character



