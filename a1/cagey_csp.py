# =============================
# Student Names: Crystal Ye, Eli James, Jacob Ma
# Group ID: 54
# Date: February 2, 2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    # - A model of a Cagey grid (without cage constraints) built using only
    #   binary not-equal constraints for both the row and column constraints.

    # n x n grid
    n = cagey_grid[0]

    # domain for each variable
    dom = []
    for i in range(n):
        dom.append(i+1)

    # n^2 variable for n x n grid
    var_arr = []
    for t in itertools.product(dom,dom):
        var_arr.append(Variable('Cell({},{})'.format(t[0],t[1]), dom)) # naming format
        
    # constraints
    cons = []

    # constraints for rows
    varDoms = [list(range(1,n+1)),list(range(1,n+1))]
    
    for row in range(n): # num of rows
        for rcell in itertools.combinations(range(n), 2):
            con = Constraint("C(Row{}-(C{},C{})".format(row+1,rcell[0]+1,rcell[1]+1),
                             [var_arr[row*n+rcell[0]],var_arr[row*n+rcell[1]]])
            sat_tuples = []
            for t in itertools.product(*varDoms):
                if t[0] != t[1]:
                    sat_tuples.append(t) # add when constraint satisfied
            con.add_satisfying_tuples(sat_tuples) # add satisfying constraints
            cons.append(con)
                
    # Constraints for columns
    for col in range(n): # num of rows
        for ccell in itertools.combinations(range(n), 2):
            con = Constraint("C(Col{}-(C{},C{})".format(col+1,ccell[0]+1,ccell[1]+1),[var_arr[col+ccell[0]*n],var_arr[col+ccell[1]*n]])
            sat_tuples = []
            for t in itertools.product(*varDoms):
                if t[0] != t[1]:
                    sat_tuples.append(t) # add when not equal
            con.add_satisfying_tuples(sat_tuples) # add satisfying constraints
            cons.append(con)

    # Creating csp object
    csp = CSP("{}x{}-BinaryGrid".format(n,n), var_arr)
    for c in cons:
        csp.add_constraint(c)
    return csp, var_arr
    
        
def nary_ad_grid(cagey_grid):
    # - A model of a Cagey grid (without cage constraints) built using only n-ary
    #   all-different constraints for both the row and column constraints.
    
    # creating csp object
    n, _ = cagey_grid
    csp = CSP("Cagey Binary")
    
    # n^2 variable for n x n grid
    vars = [[Variable(f'V{i}{j}', domain = list(range(1, n+1))) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            csp.add_var(vars[i][j])

    # adding vars and constraints for columns and rows
    for i in range(n):
        row_vars = vars[i]
        row_constraint = Constraint(f"Row {i}", row_vars)
        all_tuples = [tup for tup in itertools.permutations(range(1, n+1), n)]
        row_constraint.add_satisfying_tuples(all_tuples)
        csp.add_constraint(row_constraint)
        col_vars = [vars[x][i] for x in range(n)]
        col_constraint = Constraint(f"Col {i}", col_vars)
        col_constraint.add_satisfying_tuples(all_tuples)
        csp.add_constraint(col_constraint)
    return csp, vars


def cagey_csp_model(cagey_grid):
    # a model of a Cagey grid built using your choice of (1) binary not-equal, or
    # (2) n-ary all-different constraints for the grid, together with Cagey cage
    # constraints.

    n = cagey_grid[0]
    csp = CSP("Full-Cagey", [])  # initialize
    dom = [v for v in range(1, n + 1)]

    # initialise vars
    # add to csp
    var_arr = []
    for i in itertools.product(range(1, n + 1), repeat=2):
        new_var = Variable(("Cell" + str(i)), dom)
        var_arr.append(new_var)
        csp.add_var(new_var)

    # create scopes
    # create row n-ary constraint
    #add to CSP
    for row in range(1, n + 1):
        row_scope = list()
        for i in range(1, n + 1):
            name = "Cell({}, {})".format(row, i)
            scope_temp = []
            for var in var_arr:
                # get variable that matches name
                # add to scope
                if var.name == name:
                    if var not in scope_temp:
                        scope_temp.append(var)  # n values

            row_scope.extend(scope_temp)
            
        # constraints for each row
        cons = Constraint("N-ary-allDiff-Row({})".format(row), row_scope)

        sat_tuple = [tup for tup in
                     itertools.permutations(range(1, n + 1), n)]
        cons.add_satisfying_tuples(sat_tuple)
        csp.add_constraint(cons)

    # create scopes
    # create column n-ary constraint
    # add to CSP
    for col in range(1, n + 1):
        col_scope = list()
        for i in range(1, n + 1):
            name = "Cell({}, {})".format(i, col)
            scope_temp = []
            for var in var_arr:
                # get var that matches name
                # add to scope
                if var.name == name:
                    if var not in scope_temp:
                        scope_temp.append(var)  # n values

            col_scope.extend(scope_temp)
            
        # create constraint for each column
        cons = Constraint("N-ary-allDiff-Column({})".format(col), col_scope)

        sat_tuple = [tup for tup in
                     itertools.permutations(range(1, n + 1), n)]
        cons.add_satisfying_tuples(sat_tuple)
        csp.add_constraint(cons)

    # cage constraints

    cages = cagey_grid[1]

    for cage in cages:
        target = cage[0] # target value
        cage_vars = cage[1] # list of cells
        cage_op = cage[2] # get cage operator
        var_op_str = "" # build string for naming cage operator variable
        cage_scope = list()

        # build cage constraint scope
        for i in range(len(cage_vars)):
            var_name = "Cell" + str(cage_vars[i])
            for var in var_arr:
                if var.name == var_name:
                    if var not in cage_scope: # check if var not in cage scope
                        cage_scope.append(var)
                        var_op_str += "Var-Cell({},{}), "\
                            .format(cage_vars[i][0], cage_vars[i][1])

        # all cell vars added
        # add operator var to scope
        var_name_string = "Cage_op({}:{}:[{}])"\
            .format(target, cage_op, var_op_str[0:-2]) 

        op_var = Variable(var_name_string, ['+', '-', '/', '*', '?'])
        var_arr.append(op_var)
        csp.add_var(op_var)
        cage_scope.insert(0, op_var)
        # keeping var order same as Constraint name in A1 spec
        cons = Constraint(var_name_string, cage_scope)

        # get satisfying tuples for constraint
        sat_tuples = eval_sat_tuples((len(cage_scope)-1), cage_op, target,
                                     n)
        cons.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(cons)

    return csp, var_arr


def eval_sat_tuples(n, operator, target, grid_size) -> list:
    # An aggregator function to evaluate the constraint,
    # returns [sat_tuples]

    sat_tuples = list()
    # n => no. of cell vars (i.e., excluding cage_op)
    if n == 1:
        return [(operator, target)]

    # grid_size corresponds to highest int in var domain;
    # n is number of variables being assigned here (n-tuple)
    for tup in itertools.product(range(1, grid_size + 1), repeat=n):
        if (operator == '+') or (operator == '?'):
            if sum(tup) == target:  # check if satisfy
                sat = ('+',) + tup
                sat_tuples.append(sat)
        if operator == '*' or (operator == '?'):
            aggr = tup[0]
            for i in range(1, len(tup)):
                aggr *= tup[i]
            if aggr == target:
                sat = ('*',) + tup
                sat_tuples.append(sat)
        if operator == '-' or (operator == '?'):
            aggr = tup[0]
            for i in range(1, len(tup)):
                aggr -= tup[i]
            if aggr == target:
                # add all permutations of this to sat_tuples
                # if one satisfies then all do
                p_list = [p for p in itertools.permutations(tup, n)]
                sat = []
                for p in p_list:
                    sat.append(('-', ) + p)  # include operator
                sat_tuples.extend(sat)
        if operator == '/' or (operator == '?'):
            aggr = tup[0]
            for i in range(1, len(tup)):
                aggr = int(aggr / tup[i])   # exclude
            if aggr == target:
                # add all permutations to sat_tuples
                p_list = [p for p in itertools.permutations(tup, n)]
                sat = []
                for p in p_list:
                    sat.append(('/',) + p)  # include operator
                sat_tuples.extend(sat)

    return sat_tuples

