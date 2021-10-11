from typing import Dict, List
import networkx as nx


Path = List[int]
class AutomatonPathExtractor:
    
    def find_basis_paths(self,automaton:nx.DiGraph)->List[Path]:
        self.automaton = automaton
        self.automaton.add_edge(max(automaton.nodes),max(automaton.nodes)+1)
        self.automaton_final_state = max(automaton.nodes)
        self.visited_states = set()
        self.paths_list = []
        self._find_basis_paths(0,[])
        return self.paths_list
    def _find_basis_paths(self,current_state:int,path:Path)-> None:
        if current_state == self.automaton_final_state:
            self._mark_path_states_as_visited(path)
            self.paths_list.append(path)
        successors_id = list(self.automaton.successors(current_state))
        path = path + [current_state]
        if current_state in self.visited_states:
            next_state_id = min(successors_id)
            self._find_basis_paths(next_state_id,path)
        else:
            for next_state_id in successors_id:
                self._find_basis_paths(next_state_id,path)
    def _mark_path_states_as_visited(self,path:List[int])->None:
        for state in path:
            self.visited_states.add(state)