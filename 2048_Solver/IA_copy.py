#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:05:53 2020

@author: Renaissance
"""

    # minimize with alpha-beta pruning
    def Minimize2(self, grid, depth, eval_func, alpha, beta):
            # suppose a random computer player
        cell_values = [2,4]
        localGrid = grid.clone()
            
        if depth == 0 or len(grid.getAvailableCells())==0 :
                return (eval_func(grid),None)
            
        else: 
            
            cell_value=choices(cell_values, [0.9, 0.1])[0]
            cell=choices(grid.getAvailableCells())[0]
            
            localGrid.setCellValue(cell, cell_value)
            result_min = self.Maximize(localGrid, depth-1, eval_func, alpha, beta)
            localGrid.setCellValue(cell, 0)
            
            if len(result_min)==0:
                return (eval_func(grid),None)
            
            if result_min[0] < beta:
                beta=result_min[0]
            
            return (result_min[0], result_min[1])
            