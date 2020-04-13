#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import time
import sys
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


## new added functions
    
def return_blocks(one, full_=False):
    '''
    return_blocks is intended to return other tiles in the 3*3 blocks besides input
    input one: 'A1' or 'I9'....
    output: a list of blocks to check
    '''
   
    ROW = "ABCDEFGHI"
    row_group=['ABC', 'DEF', 'GHI']
    COL = "123456789"
    col_group=['123', '456', '789']
    
    if full_==False:
        row_=one[0]
        col_=one[1]
        
        for r in row_group:
            if row_ in r:
                for c in col_group:
                    if col_ in c:
                        perm=[row2+col2 for row2 in r for col2 in c]
                        perm.remove(one)
                        return perm
    elif full_==True:
        all_=[]
        for r in row_group:
            for c in col_group:
                perm=[row2+col2 for row2 in r for col2 in c]
                all_.append(perm)
                
        return all_
            
    
    
def update_one(one, board):
    '''
    update_one is intended to return all the feasible values of one tile
    input: a tile in string
    output: a list of feasible numbers can choose
    
    '''
    ROW = "ABCDEFGHI"
    COL = "123456789"
    result=[1,2,3,4,5,6,7,8,9]
    row_=one[0]
    col_=one[1]
    ROW_=ROW.replace(row_, '')
    COL_=COL.replace(col_, '')
    
    if board[one] != 0 :
        return []
    # first check horizontally:
    for c in COL_:
        if board[row_+c] in result:
            result.remove(board[row_+c])
            
    # then check vertically:
    for r in ROW_:
        if board[r+col_] in result:
            result.remove(board[r+col_])
            
    # check 3*3 blocks:
    check_=return_blocks(one)
    for b in check_:
        if board[b] in result:
            result.remove(board[b])
            
    return result
        
        

def update_feasibles(board):
    ## maintain a dictionary to track all possible numbers for each state that is 0
    ## sort the dictionary by number of feasible states: ascending
    ROW = "ABCDEFGHI"
    COL = "123456789"
    
    feasibles_ = { ROW[r] + COL[c]: update_one(ROW[r] + COL[c], board) for r in range(9) for c in range(9) if board[ROW[r] + COL[c]]==0} 
    feasibles_=dict(sorted(feasibles_.items(), key=lambda x: (len(x[1]), x[0])))
    
    return feasibles_

def check_complete(board):
    '''
    input: current board
    ouput: a boolean on whether this board has all tiles filled in
    '''
    ROW = "ABCDEFGHI"
    COL = "123456789"
    
    for r in ROW:
        for c in COL:
            if board[r+c] == 0:
                return False
    return True

def inference(board, feasibles, one, ROW, COL):
    row_=one[0]
    col_=one[1]
    inference_dict={}
    
    feasibles2=feasibles.copy()
    
    for c_ in COL:
        feasibles2[row_+c_]=update_one(row_+c_, board)
        if len(feasibles2[row_+c_])==1:
            inference_dict[row_+c_]=feasibles2[row_+c_][0]
        
    
    for r_ in ROW:
        feasibles2[r_+col_]=update_one(r_+col_, board)
        if len(feasibles2[r_+col_])==1:
            inference_dict[r_+col_]=feasibles2[r_+col_][0]
    
    
    for b in return_blocks(one):
        feasibles2[b]=update_one(b, board)
        if len(feasibles2[b])==1:
            inference_dict[b]=feasibles2[b][0]
    
    return inference_dict


def check_consistent(var, value, solved_board):
    '''
    var: string such as 'A3'
    value: number such as 5
    solved_board: a dictionary that records current numbers in the tiles
    
    intent to check whether set A3=5 is consistent with current board
    '''
    
    ROW = "ABCDEFGHI"
    COL = "123456789"
    flag=3
    
    row_=var[0]
    col_=var[1]
    
    ## check horizontally
    for c_ in COL:
        if solved_board[row_+c_] ==value:
            print('minus 1 in horizontally: ', row_+c_)
            flag-=1
            
    ## check vertically
    for r_ in ROW:
        if solved_board[r_+col_]==value:
            flag-=1
            
    ## check small blocks
    for b in return_blocks(var):
        if solved_board[b]==value:
            flag-=1
    
    if flag==3:
        return True
    else:
        return False

 

def backtracking(board):
    """Takes a board and returns solved board."""
    ROW = "ABCDEFGHI"
    COL = "123456789"
    
    solved_board = board
    
    ## check whether complete or not
    if check_complete(solved_board): 
        return solved_board
    
    ## update feasibles dictionary for current board
    feasibles=update_feasibles(solved_board)
    var=list(feasibles)[0]
    
    for value in feasibles[var]:
        if check_consistent(var, value, solved_board):
            solved_board[var]=value
            inference_dict=inference(solved_board, feasibles, var, ROW, COL)
            
            Flag=True
            for k, v in inference_dict.items():
                if not check_consistent(k, v, solved_board):
                    Flag=False
                    break
            if Flag:
                for k, v in inference_dict.items():
                    solved_board[k]=v
                    feasibles[k]=0  
                result=backtracking(solved_board)
                
                if result != False:
                    return result
                else:
                    ## clean the board and clean the feasible sets
                    solved_board[var]=0
                    for k in inference_dict.keys():
                        solved_board[k]=0
            
    return False
            




if __name__ == '__main__':
    #  Read boards from source.
    #src_filename = 'sudokus_start.txt'
    #try:
        #srcfile = open(src_filename, "r")
        #srcfile=open('/Users/Renaissance/Desktop/sudokus_start.txt', 'r')  ## hsj added
        #sudoku_list = srcfile.read()
    #except:
       # print("Error reading the sudoku file %s" % src_filename)
       # exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    
    time_=[]
    solved=0

    # Solve each board using backtracking
    #for line in sudoku_list.split("\n"):

       # if len(line) < 9:
           # continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
    line = sys.argv[1]
    board = { ROW[r] + COL[c]: int(line[9*r+c])
              for r in range(9) for c in range(9)}

    # Print starting board. TODO: Comment this out when timing runs.
    #print_board(board)

    # Solve with backtracking
    start_time = time.time()
    solved_board = backtracking(board)
    time_.append(time.time()-start_time)
    
    if solved_board != False:
        solved += 1

    # Print solved board. TODO: Comment this out when timing runs.
    print_board(solved_board)

    # Write board to file
    #outfile.write(board_to_string(solved_board))
    #outfile.write('\n')

    #print("Finishing all boards in file.")
    
    #out_filename2 = 'README.txt'
    #outfile2 = open(out_filename2, "w")
    #outfile2.write("Number of boards solved: "+ str(solved) + '.\n')
    #outfile2.write("Minimum: %.3f seconds" % min(time_) + '.\n')
    #outfile2.write("Maximum: %.3f seconds" % max(time_) + '.\n')
    #outfile2.write("Mean: %.3f seconds" % statistics.mean(time_) + '.\n')
    #outfile2.write("Standard deviation: %.3f seconds" % statistics.stdev(time_) + '.')
    
    
    
    
    
    
    