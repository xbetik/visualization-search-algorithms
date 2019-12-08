import sys, json, collections

def write_description(description_info):
    """Adds header to input data file which includes CSP description and initial configuration
    
    Parameters:
      description_info (tuple) CSP description in form of tuple: (algorithm name, domains, constraints) 
      
    Returns:
      str_buff (string) String representing a header which includes CSP description and initial config
    """
    str_buff = ""
    if description_info[0] == "1":
        str_buff = "#BACKTRACKING\n"
    elif description_info[0] == "2":
        str_buff = "#FORWARD-CHECKING\n"
    elif description_info[0] == "3":
        str_buff = "#FULL LOOK-AHEAD\n" 
    str_buff += "#"
    for key in list(description_info[1].keys()):
        if not str_buff.endswith("#"):
            str_buff += ","
        str_buff += key
        for value in description_info[1][key]:
            str_buff += " " + str(value)
    str_buff += "\n"
    str_buff += "#"
    for counter, constraint in enumerate(description_info[2], start=1):
        if not str_buff.endswith("#"):
            str_buff += ","
        str_buff += "c" + str(counter) + " : " + constraint
    str_buff+="\n"
    str_buff+="#description_size=16,node_size=450,edge_size=1.5,variable_label_size=25,node_label_size=16,show_frame=false,colored_limit=none,animation_speed=500\n"
    return str_buff

def create_config(solution, nodes, description_info):
    """Creates compact string representing input data file
    
    Parameters:
      solution (list)  List of solutions
      nodes (list) List of node specification
      description_info (tuple) CSP description in form of tuple: (algorithm name, domains, constraints) 
      
    Returns:
      ret_string (string) String representing input data file
    """
    ret_string = write_description(description_info)
    ret_string += "path:=R0;name:=none;order:=1\n"
    for i, node in enumerate(nodes, start=2):
        partial_string = "path:=R0"
        domains = node[0]
        node_name = None
        for domain in domains:
            variable = domain[0]
            value = domain[1]
            partial_string += variable + str(value)
            node_name = value
        partial_string += ";name:=" + str(node_name)
        partial_string += ";order:=" +str(i)
        
        if node[1] == "d":
            partial_string += ";shape:=square;color:=red"
        if any(node[0] == s for s in solution):
            partial_string += ";color:=blank"
        if node[2]:
            partial_string += ";bottom_label:="
            for l in node[2]:
                if l != node[2][0]:
                    partial_string += ","
                partial_string += "(c" + str(l+1) + ")"
        if node[3]:
            partial_string += ";side_label:="
            for l in node[3]:
                if l!=node[3][0]:
                    partial_string += "&&"
                for c in l[2]:
                    if c != l[2][0]:
                        partial_string += ","
                    partial_string += "c" + str(c+1)
                if l[1]:
                    partial_string += "->" + l[0] + ":" + str(set(l[1]))
                else:
                    partial_string += "->" + l[0] + ":{}"
        ret_string += partial_string
        if node != nodes[len(nodes)-1]:
            ret_string += "\n"
    return ret_string

def consistent(partial_solution, constraints, inconsistent_constraints):
    """Checks consistency of an assignment
    
    Parameters:
      partial_solution (dict) Represents partial assignment
      constraints (list) List of constraints
      inconsistent_constraints (list) List of constraints causing inconsistency 
    Returns:
      (boolean) True if an assignment is consistent, False otherwise
    """    
    for i, constraint in enumerate(constraints):
        try:
            if not eval(constraint, partial_solution):
                if i not in inconsistent_constraints:
                    inconsistent_constraints.append(i)
                return False
        except:
            pass
    return True

def backtracking(domains, constraints, partial_solution, solution, nodes):
    """Solves the problem using Backtracking algorithm
    
    Parameters:
      domains (dict) Represents domains as dict(variables:values)
      constraints (list) List of constraints
      partial_solution (dict) Represents partial assignment
      solution (list) List of all the solutions
      nodes (list) List of all the nodes
    Returns:
      Void function
    """
    if not domains:
        solution.append(list(partial_solution.items()))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        values_original = domain[1][:]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            inconsistent_constraints = []
            is_consistent = consistent(partial_solution.copy(), constraints, inconsistent_constraints)
            if is_consistent:
                nodes.append((list(partial_solution.items()), "p", inconsistent_constraints, None))
                backtracking(domains, constraints, partial_solution, solution, nodes)
            else:
                nodes.append((list(partial_solution.items()), "d", inconsistent_constraints, None))
        partial_solution.popitem()
        domains[name] = values_original

def dead_end(accessible_domains):
    """Returns true if the domains is empty; therefore is a dead-end
    
    Parameters:
      accessible_domains (dict) Represents domains as dict(variables:values)
    
    Returns
      (boolean) True if an assignment is dead-end,false otherwise
    """
    return any(value==[] for value in accessible_domains.values())

def select_forward_check(partial_solution, domains, constraints, d_behavior):
    """Forward-checking select function which deletes inconsistent values from the domains 
    
    Parameters:
      partial_solution (dict) Represents partial assignment
      domains (dict) Represents domains as dict(variables:values)
      constraints (list) List of constraints
      solution (list) List of all the solutions
      d_behavior (list) List of tuples representing domain change
      
    Returns:
      accessible_domains (dict) Updated domains
    """
    accessible_domains = {key : [] for key in domains.keys()}
    constraints_applied = {key : [] for key in domains.keys()}
    for variable in domains.keys():
        inconsistent_constraints = []
        for value in domains.get(variable):
            partial_solution[variable] = value
            is_consistent = consistent(partial_solution.copy(), constraints, inconsistent_constraints)
            if is_consistent:
                accessible_domains.get(variable).append(value)
        if accessible_domains.get(variable) != domains.get(variable):
            d_behavior.append((variable, accessible_domains.get(variable)[:], inconsistent_constraints))
        partial_solution.popitem()
    return accessible_domains

def forward_checking(domains, constraints, partial_solution, solution, nodes):
    """Solves the problem using Forward-checking algorithm
    
    Parameters:
      domains (dict) Represents domains as dict(variables:values)
      constraints (list) List of constraints
      partial_solution (dict) Represents partial assignment
      solution (list) List of all the solutions
      nodes (list) List of all the nodes
      
    Returns:
      Void function
    """
    if not domains:
        if consistent(partial_solution.copy(), constraints, []):
            solution.append(list(partial_solution.items()))
        else:
            nodes.pop()
            nodes.append((list(partial_solution.items()), "d", None, None))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        values_original = domain[1][:]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            d_behavior = []
            accessible_domains = select_forward_check(partial_solution, domains, constraints, d_behavior)
            if dead_end(accessible_domains):
                nodes.append((list(partial_solution.items()), "d", None, d_behavior))
            else:
                nodes.append((list(partial_solution.items()), "p", None, d_behavior))
                forward_checking(accessible_domains, constraints, partial_solution, solution, nodes)
        partial_solution.popitem()
        domains[name] = values_original

def revise(constraints, dom_name1, values1, dom_name2, values2, inconsistent_constraints):
    """Revises the edges between two variables dom_name1 and dom_name2
    
    Parameters:
      constraints (list) List of constraints
      dom_name1 (string) Variable number one
      values1 (int) Value assigned to variable number one
      dom_name2 (string) Variable number two
      values2 (int) Value assigned to variable number two
      inconsistent_constraints (list) List of constraints causing inconsistency 
      
    Returns:
      domains (dict) Revised (updated) domains
    """
    changed_domain = []
    for value1 in values1:
        consistent_value_found = False
        for value2 in values2:
            is_consistent = consistent({dom_name1 : value1, dom_name2 : value2}, constraints, inconsistent_constraints)
            if is_consistent:
                consistent_value_found = True
        if consistent_value_found:
            changed_domain.append(value1)
    return changed_domain

def reviseAll(domains, constraints, name, value, d_behavior):
    """Revises all the edges connected to input node (which is identified by name(variable) and value)
    
    Parameters:
      domains (dict) Represents domains as dict(variables:values)
      constraints (list) List of constraints
      name (string) Identifies the variable which is getting all the edges revised
      value (int) Identifies the current assigned value
      d_behavior (list) List of tuples representing domain change
      
    Returns:
      domains (dict) Revised (updated) domains
    """
    domain_queue = [(name, [value])]
    for d in domains.items():
        domain_queue.append((d[0], d[1]))
    while domain_queue:
        name, values = domain_queue.pop(0)
        for d in list(domains.items()):
            if d[0] != name:
                inconsistent_constraints = []
                changed_domain = revise(constraints, d[0], d[1], name, values, inconsistent_constraints)
                if changed_domain != d[1]:
                    domains[d[0]] = changed_domain 
                    changed = True
                    domain_queue.append((d[0], changed_domain))
                    if inconsistent_constraints:
                        d_behavior.append((d[0], changed_domain[:], inconsistent_constraints))
    return domains

def full_look_ahead(domains, constraints, partial_solution, solution, nodes):
    """Solves the problem using Full look-ahead algorithm
    
    Parameters:
      domains (dict) Represents domains as dict(variables:values)
      constraints (list) List of constraints
      partial_solution (dict) Represents partial assignment
      solution (list) List of all the solutions
      nodes (list) List of all the nodes
      
    Returns:
      Void function
    """
    def remove_redudant_behavior(behavior):
        updated_behavior = []
        for i in behavior:
            smallest = True
            for j in behavior:
                if i[0] == j[0] and len(i[1]) > len(j[1]):
                    smallest = False
            if smallest:
                updated_behavior.append(i)
        return updated_behavior

    if not domains:
        if consistent(partial_solution.copy(), constraints, []):
            solution.append(list(partial_solution.items()))
        else:
            nodes.pop()
            nodes.append((list(partial_solution.items()), "d", None, None))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            domains_copy = {key : domains[key][:] for key in domains.keys()}
            d_behavior = []
            changed_domains = reviseAll(domains_copy, constraints, name, value, d_behavior)
            d_behavior = remove_redudant_behavior(d_behavior)
            if any(value == [] for value in changed_domains.values()):
                nodes.append((list(partial_solution.items()), "d", None, d_behavior))
            else:
                nodes.append((list(partial_solution.items()), "p", None, d_behavior))
                full_look_ahead(changed_domains, constraints, partial_solution, solution, nodes)
            partial_solution.popitem()

def parse(dom, constraints):
    """Parses the domains and constraints
    
    Parameters:
      dom (string) Domains
      constraints (string) Constraints
    
    Returns:
      (dict) Represents domains as dict(variables:values)
    """
    dom_temp = dom[1:len(dom)-1]
    dom_temp = dom_temp.replace("{", "[")
    dom_temp = dom_temp.replace("}", "]")
    dom_temp = "{" + dom_temp + "}"
    return json.loads(dom_temp), constraints.split(",")

def solve(algorithm, domains, constraints):
    """Solves the CSP
    
    Parameters:
      algorithm (string) Identifies algorithm '1'-backtracking, '2'-forward-checking, '3'-full look-ahead
      domains (string) Domains
      constraints (string) Constraints
    
    Returns:
      config_str (string) Represents input data file
    """
    domains, constraint_list = parse(domains, constraints)
    options = { 
        "1" : backtracking,
        "2" : forward_checking,
        "3" : full_look_ahead,
        }
    partial_solution = {}
    solution = []
    nodes = []
    domains_copy = {key : domains[key][:] for key in domains.keys()}
    ordered_domains = collections.OrderedDict(sorted(domains_copy.items())[::-1])
    options[algorithm](ordered_domains, constraint_list, partial_solution, solution, nodes)
    description_info = (algorithm, domains, constraint_list)
    config_str = create_config(solution, nodes, description_info)
    return config_str

if __name__ == "__main__":
    args = sys.argv
    algorithm = args[1]
    domains = args[2]
    constraints = args[3]
    config_str = solve(algorithm, domains, constraints)
    f = open("tree_data.txt", "w+")
    f.write(config_str)
    print("Input text data file created. File name: tree_data.txt")
