# =============================
# Student Names: Crystal Ye, Eli James, Jacob Ma
# Group ID: 54
# Date: February 2, 2024
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''

    # Initialize two variables to track the maximum degree and the variable that holds the maximum degree
    max_degree_var = None
    max_degree = float("-inf")

    # Initialize a variable that gets all the unassigned variables in the CSP
    unassigned_vars = csp.get_all_unasgn_vars()

    # Iterate through each of the unassigned variables
    # Calculate the degree of the current variable with the number of constraints that involve that variable
    for var in unassigned_vars:
        degree_of_var = len(csp.get_cons_with_var(var))
        # If the degree of this variable is greater than the current maximum degree, update the max_degree variable
        # with the current variable with the higher degree
        if degree_of_var > max_degree:
            max_degree = degree_of_var
            max_degree_var = var

    # Return the variable with the maximum degree
    return max_degree_var

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''

    #initialize the first variable
    temp = csp.get_all_vars()[0]

    #for each unassigned variable in the CSP, get the domain size
    for var in csp.get_all_unasgn_vars():
        current_domain_size = var.cur_domain_size()
        #check if the current domain is more constrained than temp
        if current_domain_size < temp.cur_domain_size():
            #if so, temp becomes the new, most constrained var.
            temp = var 
    return temp
