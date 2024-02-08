# =============================
# Student Names: Crystal Ye, Eli James, Jacob Ma
# Group ID: 54
# Date: February 2, 2024
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for constraint in csp.get_cons_with_var(newVar):
        if constraint.get_n_unasgn() == 0:
            vals = []
            vars = constraint.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not constraint.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable, value pairs and return '''
   
    # Initialize an empty list to keep track of variables that were pruned
    pruned = []

    # If there is no new variable given, get all of the constraints from the CSP
    if not newVar:
        cons = csp.get_all_cons()
    else:
        # If a new variable is given, get constraints that the variable is involved with
        cons = csp.get_cons_with_var(newVar)

    # Iterate through all of the constraints in the set of constraints
    # Check if there is a single uninstantiated variable in the cosntraint and get the variable
    for c in cons:
        if c.get_n_unasgn() == 1:
            var = c.get_unasgn_vars()[0]
            # Iterate through the variable's domain
            # If the constraint does not have support for the value in the domain, prune the value from the variable's domain
            for element in var.cur_domain():
                if not c.has_support(var, element):
                    var.prune_value(element)
                    # If the path of the prune variable is not in the 'pruned' list, append it to the list
                    path = (var, element)
                    if path not in pruned:
                        pruned.append(path)

            # If the current domain of the variable is empty after pruning, the CSP is not satisfiable in the current state
            # Return as false and the pruned list
            if var.cur_domain_size() == 0:
                return False, pruned

    # Return True and the list of pruned variable, value pairs if all of the requirements are satisfied
    return True, pruned


def remove_inconsistent_from_domain(constraint):
    pruned = []
    for var in constraint.get_unasgn_vars():
        current_domain= var.cur_domain()
        current_domain_copy = current_domain.copy()

        #prune values which violate constraints
        for val in current_domain_copy:
            if not constraint.check_var_val(var, val):
                var.prune_value(val)
                pruned.append((var, val))
                current_domain.remove(val)

    return pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    pruned = []
    #if new var is none, we do initial GAC 
    if not newVar:
        for constraint in csp.get_all_cons():
            #prune values from call constraints
            pruned+=remove_inconsistent_from_domain(constraint)
    else:
        #GAC for constraints involving the recent variable
        for constraint in csp.get_cons_with_var(newVar):
            #prune values only from newVar constraints
            pruned+=remove_inconsistent_from_domain(constraint)

    return True, pruned


