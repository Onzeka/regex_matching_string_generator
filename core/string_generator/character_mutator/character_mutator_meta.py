from abc import ABC,abstractmethod
from typing import  List
from ponicode.parser import CodeParser,Node


class MetaCharacterMutator(ABC):
    def __init__(self,parser:CodeParser)->None:
        self.parser = parser
    
    def _get_regex_slice_node(self,regex_slice:str)->Node:#duplicate from character_generator_meta
        return self.parser.parse(regex_slice).root_node.children[0].children[0] 
   
    
    @abstractmethod
    def mutate(self,regex_slice:str)->List[str]:
        raise NotImplementedError