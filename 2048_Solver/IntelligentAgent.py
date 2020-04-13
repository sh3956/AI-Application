import random
from BaseAI import BaseAI
from random import choices
import math

UP, DOWN, LEFT, RIGHT = range(4)

class IntelligentAgent(BaseAI):
    
    

    
    def monotonicity(self, grid):
        # measure the monotonicity of the board
        # increasing or decreasing monotonically along a row/col
        map_=grid.map
        m=0
        
        for i in range(4):
            diff=map_[i][0]-map_[i][1]
            for j in range(3):
                if (map_[i][j]-map_[i][j+1])*diff <=0:
                    m+=1
                diff=map_[i][j]-map_[i][j+1]
        
        for j in range(4):
            diff=map_[0][j]-map_[1][j]
            for i in range(3):
                if (map_[i][j]-map_[i+1][j])*diff <=0:
                    m+=1
                diff=map_[i][j]-map_[i+1][j]        
        return m
    
    def smoothness(self, grid):
        # measure the differences between neighboring tiles
        # the less the smoothness, the better
        s=0
        map_=grid.map
        
        for i in range(4):
            for j in range(3):
                s += abs(map_[i][j]-map_[i][j+1])
        
        for j in range(4):
            for i in range(3):
                s += abs(map_[i][j]-map_[i+1][j])
                
        return s
    
    
    def complexity(self, grid):
        complexity = 0
        m = grid.map
        size = grid.size
        for row in range(0, size):
            for col in range(0, size):
                if m[row][col] != 0:
                    complexity += math.log(m[row][col])/math.log(2)

        return complexity

    def average_tail_value(self,grid):
        s=0
        c=0
        for i in grid.map:
            for j in i:
                if j!=0:
                    s+=j
                    c+=1
        return s/c
    def weight_map(self, grid):
        weight_matrix=[[15, 14, 13, 12],
                       [8, 9, 10, 11],
                       [7, 6, 5, 4],
                       [0, 1, 2, 3]]
        value=0
         
        for i in range(4):
            for j in range(4):
                value += weight_matrix[i][j]*grid.map[i][j]
                
        return value
         
    def game_over(self, grid):
        if len(grid.getAvailableMoves())==0:
            return -100000
        return 0
    
    def density(self, grid):
        density = 0
        m = grid.map
        size = grid.size
        for row in range(0, size):
            for col in range(0, size):
                if m[row][col] != 0:
                    density += (math.log(m[row][col])/math.log(2))*m[row][col]
        return density
    
    
    def corner(self, grid):
        max_=max(max(grid.map))
        c1=grid.map[0][0]
        c2=grid.map[0][3]
        c3=grid.map[3][0]
        c4=grid.map[3][3]
        
        l0=0.6*grid.map[0][1]
        l1=0.6*grid.map[0][2]
        l2=0.6*grid.map[3][1]
        l3=0.6*grid.map[3][2]
        score=0
        
        
        if c1==max_ or c2==max_ or c3==max_ or c4==max_:
            score=5
        elif l0==max_ or l1==max_ or l2==max_ or l3==max_:
            score=3
           
        c=c1+c2+c3+c4
        l=l0+l1+l2+l3
        
        return score
    
    def eval_2(self, grid):

        num_space=len(grid.getAvailableCells())
        #weighted_map=self.weight_map(grid)
        m=self.monotonicity(grid)
        #num_moves=len(grid.getAvailableMoves())
        #avg_tail_value=self.average_tail_value(grid)
        smooth=self.smoothness(grid)
        #go=self.game_over(grid)
       # complexity=self.complexity(grid)
        #density=self.density(grid)
        #max_weight=self.getMaxTile()
        corner=self.corner(grid)
        
        return num_space + corner
        
    
    def eval_(self,grid):
        # evaluation function of each state for expectimax
        # decides to use a snail weight matrix
        value=0
        weight_matrix=[[4**15, 4**14, 4**13, 4**12],
                       [4**8, 4**9, 4**10, 4**11],
                       [4**7, 4**6, 4**5, 4**4],
                       [4**0, 4**1, 4**2, 4**3]]


        for i in range(4):
            for j in range(4):
                value += weight_matrix[i][j]*grid.map[i][j]
                
        return value
    
    ## maximize with alpha-beta pruning
    def Maximize(self, grid, depth, eval_func, alpha, beta):
    
        return_val=()
        
        if depth == 0:
            return (eval_func(grid),None)

        bestValue = float("-inf")

        for move in grid.getAvailableMoves():
            gridCopy = grid.clone()
            gridCopy.move(move)
            
            result = self.chance(gridCopy, depth-1, eval_func, alpha, beta)
            
            if(bestValue < max(bestValue, result)):
                bestValue = max(bestValue, result)
                return_val = (bestValue, move[0])
            
            if bestValue >= beta:
                break
            if bestValue > alpha:
                alpha=bestValue
            
        return return_val
    
    

    def Minimize(self, grid, depth, eval_func, alpha, beta, cell_values):
            #candidates = []
        best_utility = float("inf")
        
        localGrid = grid.clone()
        
        if depth == 0 or len(grid.getAvailableCells())==0 :
            return (eval_func(grid),None)
        
        else:
        # randomly generate the next step
            for cell in grid.getAvailableCells():
                
                localGrid.setCellValue(cell, cell_values)
                result_min = self.Maximize(localGrid, depth-1, eval_func,alpha, beta)
                # reset it back to 0
                localGrid.setCellValue(cell, 0)
                if len(result_min)==0:
                    return (eval_func(grid),None)
                
                if best_utility > min(best_utility, result_min[0]):
                    best_utility = min(best_utility, result_min[0])
                    return_val = (best_utility, result_min[1])
                    
                if best_utility <= alpha:
                    break
                
                if best_utility < beta:
                    beta=result_min[0]
        
            return return_val
        
    def chance(self, grid, depth, eval_func, alpha, beta):
        return 0.9*self.Minimize(grid, depth, eval_func, alpha, beta, 2)[0]+ 0.1*self.Minimize(grid, depth, eval_func, alpha, beta, 4)[0]
         
        
    
    def getMove(self, grid):
     
        moveset = grid.getAvailableMoves()
        move= self.Maximize(grid,4, self.eval_2, float("-inf"), float("inf"))[1] if moveset else None

        return move if moveset else None
        
        #return self.Maximize(grid, 2, self.eval_2, float("-inf"), float("inf"))[1] if moveset else None
    
    
    
    
    
    
    
    