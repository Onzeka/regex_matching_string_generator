from typing import List
from core.string_generator.character_mutator.character_mutator_meta import MetaCharacterMutator
from core.string_generator.character_mutator.character_mutator_utils_classes import CHARACTER_MUTATOR_CLASSES
import string


class CharacterMutator(MetaCharacterMutator):

    def mutate(self,regex_slice:str,regex:str)->List[str]:
        mutations = []
        if regex_slice != "":
            regex_slice_node_type = self._get_regex_slice_node(regex_slice).type
            character_mutator_class = CHARACTER_MUTATOR_CLASSES.get(regex_slice_node_type)
            if character_mutator_class != None:
                mutator = character_mutator_class(self.parser)
                mutations = mutator.mutate(regex_slice)
        if CharacterMutator._punctuation_needed(regex_slice):
            mutations.extend(CharacterMutator._get_regex_punctuation(regex))
        return mutations

    @staticmethod
    def _get_regex_punctuation(regex)->List[str]:
        return [ char for char in regex if char in string.punctuation ]
    @staticmethod
    def _punctuation_needed(regex_slice:str)->bool:
        for character in CharacterMutator.PUNCTUATION_FLAGED_ESCAPED_CHARACTERS:
            if character in regex_slice:
                return True
        return False

    PUNCTUATION_FLAGED_ESCAPED_CHARACTERS = ['\D','\W','\S']