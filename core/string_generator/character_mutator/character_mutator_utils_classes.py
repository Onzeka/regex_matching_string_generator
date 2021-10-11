from ctypes import util
from typing import Dict, List, Tuple
from core.string_generator.character_mutator.character_mutator_meta import MetaCharacterMutator
import random
import string




class AnyCharacterMutator(MetaCharacterMutator):# '.'
    def mutate(self, regex_slice: str) -> List[str]:
        return [random.choice(string.digits),random.choice(string.ascii_uppercase),random.choice(string.ascii_lowercase)]



class CharacterClassEscapeMutator(MetaCharacterMutator):# '/W'
    def _get_w_class_mutations(self):
        return [random.choice(string.digits),random.choice(string.ascii_uppercase),random.choice(string.ascii_lowercase),'_']
    
    def _get_s_class_mutations(self):
        return [random.choice(string.whitespace)]
   
    def _get_d_class_mutations(self):
        return [random.choice(string.digits)]
    
    def _get_upper_class_mutations(self):
        return [random.choice(string.digits),random.choice(string.ascii_uppercase),random.choice(string.ascii_lowercase),'_',random.choice(string.whitespace)]
    _class_sets_characters= {
        'w': _get_w_class_mutations,
        's': _get_s_class_mutations,
        'd': _get_d_class_mutations
    }
    def mutate(self, regex_slice: str) -> List[str]:
        character_class = regex_slice[-1]
        return CharacterClassEscapeMutator._class_sets_characters.get(character_class,CharacterClassEscapeMutator._get_upper_class_mutations)(self)



class CharacterClassMutator(MetaCharacterMutator):#[a-z0-9]
    
    def mutate(self, regex_slice: str) -> List[str]:
        character_class_node = self._get_regex_slice_node(regex_slice)
        children = [child for child in character_class_node.children if child.is_named]
        mutations = []
        for child in children:
            child_string = self.parser.get_code(child,regex_slice)
            print(child.type)
            util_mutator = CharacterClassMutator._TYPE_TO_MUTATOR.get(child.type,CharacterClassMutator.ClassCharacterMutator)(self.parser)
            mutations.extend(util_mutator.mutate(child_string))
        return mutations
    @staticmethod
    def _get_char_super_set(char:str)->str:
        for super_set in [string.digits,string.ascii_lowercase,string.ascii_uppercase,string.punctuation]:
            if char in super_set:
                return super_set

    class ClassRangeMutator(MetaCharacterMutator):
        def mutate(self, regex_slice: str) -> List[str]:
            in_range_characters , out_range_characters = self._get_class_range_values_and_class_range_outter_values(regex_slice) 
            mutations = [random.choice(in_range_characters)]
            if out_range_characters != '' :
                mutations.append(random.choice(out_range_characters))
            return mutations

        @staticmethod
        def _is_class_range_valid(class_range_string:str)->bool:
            lower_char,upper_char = class_range_string[0],class_range_string[-1]
            return ord(lower_char)<ord(upper_char) and CharacterClassMutator._get_char_super_set(lower_char) == CharacterClassMutator._get_char_super_set(upper_char)

        @staticmethod
        def _get_class_range_values_and_class_range_outter_values(class_range_string:str)->Tuple[List[str],List[str]]:  
            char_super_set = CharacterClassMutator._get_char_super_set(class_range_string[0])
            lower_bound,upper_bound = char_super_set.index(class_range_string[0]),char_super_set.index(class_range_string[-1])
            return char_super_set[lower_bound:upper_bound] , char_super_set[:lower_bound]+char_super_set[upper_bound+1:]
    
    class ClassCharacterMutator(MetaCharacterMutator):
        def mutate(self, regex_slice: str) -> List[str]:
            mutations = [regex_slice]
            print(regex_slice)
            char_super_set = CharacterClassMutator._get_char_super_set(regex_slice)
            mutations.append(random.choice(char_super_set.replace(regex_slice,'')))
            return mutations

    class IdentityEscapeMutator(MetaCharacterMutator):
        def mutate(self, regex_slice: str) -> List[str]:
            return [regex_slice[-1]]

    _TYPE_TO_MUTATOR:Dict[str,MetaCharacterMutator] = {
        'class_range': ClassRangeMutator,
        'class_character':ClassCharacterMutator,
        'identity_escape': IdentityEscapeMutator
    }
    


CHARACTER_MUTATOR_CLASSES:Dict[str,MetaCharacterMutator] = {
    'any_character' : AnyCharacterMutator,
    'character_class_escape': CharacterClassEscapeMutator,
    'character_class': CharacterClassMutator
}
