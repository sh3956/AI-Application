

from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
from heapq import heappush, heappop
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        new_config=self.config.copy()
        if self.blank_index >=3:
            new_cost = self.cost + 1

            new_config[self.blank_index]=self.config[self.blank_index-3]
            new_config[self.blank_index-3]=0
            
            new_=PuzzleState(new_config, self.n, parent=self, action='Up', cost=new_cost)
        
            return new_
        return None
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_config=self.config.copy()
        if self.blank_index < 6:
            new_cost = self.cost + 1

            new_config[self.blank_index]=self.config[self.blank_index+3]
            new_config[self.blank_index+3]=0
        
            return PuzzleState(new_config, self.n, parent=self, action='Down', cost=new_cost)
        return None
      
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_config=self.config.copy()
        if self.blank_index != 0 and self.blank_index != 3 and self.blank_index != 6:
            new_cost = self.cost + 1

            new_config[self.blank_index]=self.config[self.blank_index-1]
            new_config[self.blank_index-1]=0
        
            return PuzzleState(new_config, self.n, parent=self, action='Left', cost=new_cost)
        return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        new_config=self.config.copy()
        if self.blank_index != 2 and self.blank_index != 5 and self.blank_index != 8:
            new_cost = self.cost + 1
            new_config[self.blank_index]=self.config[self.blank_index+1]
            new_config[self.blank_index+1]=0

            return PuzzleState(new_config, self.n, parent=self, action='Right', cost=new_cost)
        return None
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children
    

        
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state_list):
    state=state_list[0]
    node=state_list[1]
    time=state_list[2]
    ram=state_list[3]
    max_level=state_list[4]
    
    def back_track(final_state):
        path=[]
        level=0
        while final_state!=None:
            level+=1
            path.insert(0, final_state.action)
            if final_state.parent==None:
                break
            final_state=final_state.parent
        return [path[1:], level]
    
    path=back_track(state)[0]
    cost=state.cost
    level=back_track(state)[1]
    
            
    ### Student Code Goes here

    
    with open('output.txt', 'w') as f:
        print('path_to_goal:', path, file=f)
        print('cost_of_path:', cost, file=f)
        print('nodes_expanded:', node, file=f)
        print('search_depth:', level-1, file=f)
        print('max_search_depth:', max_level, file=f)
        print('running time:', time, file=f)
        print('max_ram_usage:', ram, file=f)


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time  = time.time()
    max_level=initial_state.cost
    node_expanded=0
    visited=set()
    queue=[]
    queue.append(initial_state)
    visited.add(tuple(initial_state.config))
    
    while queue:
        c=queue.pop(0)
        if test_goal(c):
            end_time=time.time()
            ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return writeOutput([c, node_expanded, end_time-start_time, ram, max_level])
        else: 
            c.children=c.expand()
            node_expanded += 1
            for child in c.children:
                if not tuple(child.config) in visited:
                    max_level = max(max_level, child.cost)
                    queue.append(child)
                    visited.add(tuple(child.config))
                    
    return 'no found'
    

def dfs_search(initial_state):
    """DFS search"""
    start_time  = time.time()
    
    frontier=[]
    all_=set()
    frontier.append(initial_state)
    node_expanded=0
    max_level=initial_state.cost
   
    while len(frontier)!=0:
        state=frontier.pop(-1)
        all_.add(tuple(state.config))
        
        if test_goal(state):
            end_time=time.time()
            ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return writeOutput([state,node_expanded, end_time-start_time, ram, max_level])
        
        state.children=state.expand()
        node_expanded+=1
        
        for child in state.children[::-1]:
            if not tuple(child.config) in all_:
                max_level=max(max_level, child.cost)
                frontier.append(child)
                all_.add(tuple(child.config))
                
    return 'not found'

    
def A_star_search(initial_state):
    """A * search"""
    start_time=time.time()
    def key_decrease(state, dictionary):
        for key, value in dictionary.items():
            if state.config==key.config and calculate_total_cost(state) > calculate_total_cost(child):
                dictionary[key]=calculate_total_cost(child)
                break
        return dictionary

            
    action_order={'Initial':0, 'Up':1, 'Down':2, 'Left':3, 'Right':4} 
    insert_t={}          
    count=0
    frontier={}
    fs=set()
    frontier[initial_state]=calculate_total_cost(initial_state)
    insert_t.update({initial_state:time.time()})
    fs.add(tuple(initial_state.config))
    all_=set()
    max_level=0
    node_expanded=0
    
    while len(frontier)!=0:
        state=list(frontier.keys())[0]
        frontier.pop(state)
        fs.remove(tuple(state.config))
        all_.add(tuple(state.config))
        
        if test_goal(state):
            end_time=time.time()
            ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return writeOutput([state, node_expanded, end_time-start_time, ram, max_level])
        
        state.children=state.expand()
        node_expanded+=1
        for child in state.children:
            if tuple(child.config) not in all_:
                max_level=max(max_level, child.cost)
                #frontier[child]=calculate_total_cost(child) 
                frontier.update({child:calculate_total_cost(child)})
                insert_t.update({child: time.time()})
                frontier=dict(sorted(frontier.items(), key=lambda x: (x[1], action_order[x[0].action],insert_t[x[0]])))
                fs.add(tuple(child.config))
                all_.add(tuple(child.config))
                
            elif tuple(child.config) in fs:
                frontier=key_decrease(child, frontier)
    return 'not found'  
    

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    dist_=0
    for i in range(len(state.config)):
        dist_ += calculate_manhattan_dist(i, state.config[i], state.n)
    
    return float(state.cost + dist_)

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    board=[[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    return abs(board[idx][0]-board[value][0]) + abs(board[idx][1]-board[value][1])
    
    
def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    return puzzle_state.config==[0,1,2,3,4,5,6,7,8]

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    begin_state=[6,1,8,4,0,2,7,3,5]
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()