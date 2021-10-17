from abc import ABC,abstractmethod
import random
from typing import List, Union
from ponicode.parser import CodeParser,Node

class MetaCharacterGenerator(ABC):
    def __init__(self,parser:CodeParser)->None:
        self.parser = parser
        self.naturalness_provider = MetaCharacterGenerator.NaturalnessProvider

    def _get_regex_slice_node(self,regex_slice:str)->Node:
        return self.parser.parse(regex_slice).root_node.children[0].children[0]
    
    def _pick_natural_chars_from_list(self,list:str)->List:
        char = self.naturalness_provider.get_char()
        chars = []
        if char != None and char.upper() in list:
            chars.append(char.upper())
        elif char != None and char.lower() in list:
            chars.append(char.lower())
        
        return chars
    
    def init_naturalness(self)->None:
        MetaCharacterGenerator.NaturalnessProvider.init()
    
    def update_naturalness(self)->None:
        MetaCharacterGenerator.NaturalnessProvider.update()
        
    @abstractmethod
    def generate_character(self,regex_slice:str)->str:
        raise NotImplementedError
    
    class NaturalnessProvider:
        NATURAL_STRINGS = [
            "redananas",
            "supersayah",
            "blackadibou",
            "rainbowponicorn",
            "yellowrenul",
            "greenclairo",
            "blackandyellow"
        ]
        cursor = 0
        current_string = random.choice(NATURAL_STRINGS)
        @staticmethod
        def init():
            MetaCharacterGenerator.NaturalnessProvider.cursor = 0
            MetaCharacterGenerator.NaturalnessProvider.current_string = random.choice(MetaCharacterGenerator.NaturalnessProvider.NATURAL_STRINGS)
        @staticmethod
        def get_char()-> Union[None,str]:
            if MetaCharacterGenerator.NaturalnessProvider.cursor >= len(MetaCharacterGenerator.NaturalnessProvider.current_string):
                return None
            else:
                char = MetaCharacterGenerator.NaturalnessProvider.current_string[MetaCharacterGenerator.NaturalnessProvider.cursor]
                return char
        def update()->None:
            MetaCharacterGenerator.NaturalnessProvider.cursor += 1
            if MetaCharacterGenerator.NaturalnessProvider.cursor >= len(MetaCharacterGenerator.NaturalnessProvider.current_string):
                MetaCharacterGenerator.NaturalnessProvider.init()