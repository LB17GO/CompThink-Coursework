def load_dimacs(filename):
    file = open(filename, "r") #opens file
    i=0
    linesList = []
    for x in file: #loops through each line
        items = []
        item = ""
        if(i>0):
            for j in x: #loops through each character in the line
                if (j != " " and j!="\n" and j!="0"): #if j is integer
                    item+=j #appends (does this because a number could possibly multiple characters)
                if(j==" "): #if the next character is a space = end of number
                    items.append(item) #adds another item into list
                    item = ""
            linesList.append(items) #adds list to main list 
        i+=1
    return linesList
    
def simple_sat_solve(clause_set):
    
    variables = set() #set is an ordered non repeating list of elements
    for clause in clause_set: #loops through each clause
        for literal in clause: #loops through each item in clause
            variables.add(abs(literal)) #adds it to the set variables (abs means it ignores negation)

    variables = list(variables)  #converts it into a list
    n = len(variables)  #finds and stores the number of variables

    for i in range(2**n):  #2^n possible assignments
        assignment = {} #dictionary used to store assignments for each variable
        
        #assign True/False based on the binary representation of i, this will change each time j increments
        for j in range(n):
            if (i & (1 << j)) > 0:
                assignment[variables[j]] = True # if bit is 1 assign true
            else:
                assignment[variables[j]] = False #if bit is 0 assign false

        #loops through to check if this assignment satisfies all clauses
        satisfied = True #is true if all the clauses are true
        for clause in clause_set:
            FoundTrue = False #is true if the individual clause is true
            for literal in clause:
                var = abs(literal) #gets variable number and ignores negation
                value = assignment[var] #gets true/false
                if (literal < 0):  # if literal is negative, invert the value
                    value = not value
                if (value==True):  #if at least one literal is True, clause is satisfied
                    FoundTrue = True
            if not FoundTrue: #if no literal was tue, whole thing false
                satisfied = False

        #if we found a satisfying asignment, return it
        if satisfied:
            result = []
            for var in variables:
                if assignment[var]:
                    result.append(var)
                else:
                    result.append(-var)
            return result
        
    return False  #no satisfying assignment found

def branching_sat_solve(clause_set, partial_assignment):

    variables = set() #set is an ordered non repeating list of elements
    for clause in clause_set: #loops through each clause
        for literal in clause: #loops through each item in clause
            variables.add(abs(literal)) #adds it to the set variables (abs means it ignores negation)

    variables = list(variables)  #converts it into a list
    n = len(variables)  #finds and stores the number of variables

    assignment = {} #dictionary used to store assignments for each variable
        
    for x in range(n):
        assignment[variables[x]] = None #initally assigns all variables None

    for x in partial_assignment:
        if(x<0):
            assignment[abs(x)] = False
        else:
            assignment[x] = True
    
    def checker(clause_set, assignment): #this checks whether current assignments work
        
        for clause in clause_set:
            FoundTrue = False #is true if the individual clause is true
            for literal in clause:
                var = abs(literal) #gets variable number and ignores negation
                value = assignment.get(var) #gets true/false
                if (value is None):
                    continue
                if (literal < 0):  # if literal is negative, invert the value
                    value = not value
                if (value==True):  #if at least one literal is True, clause is satisfied
                    FoundTrue = True
                    break
            if not FoundTrue: #if no literal was true, whole thing false
                return False
        return True

    def Sat_Solver(assignment):
        if (checker(clause_set, assignment)==True): #if the current assignments work, the program will return the assignments 
            return assignment
        j=0
        finished = True
        for j in range(n): #if any of the variables don't have assignments then the work isn't finished
            if(assignment[variables[j]] == None):
                finished = False
                break

        if(finished== True): #if it is finished it will have already been checked in the first if statement
            if(checker(clause_set, assignment)==False): #this means it's likely that the current assignments don't work
                return False
        else:
            unassignedVar = variables[j] # this uses the loop we used earlier to find the first variable that has not been assigned
            assignment[unassignedVar] = True #first sets it to true (just to try it out)
            result = Sat_Solver(assignment) #if this doesn't work it will return false
            if (result is not False): #if it doesn't then it works (so far)
                return result #the process will repeat until all the variables have been assigned ard are correct
            
            assignment[unassignedVar] = False #if setting the variable as true didn't work
            return Sat_Solver(assignment) #it will try setting it as false, if this doesn't work the whole premise is wrong
    
    return Sat_Solver(assignment) #returns final assignements or false if unsatisfiable

def unit_propagate(clause_set):
    variables = set() #set is an ordered non repeating list of elements
    for clause in clause_set: #loops through each clause
        for literal in clause: #loops through each item in clause
            variables.add(abs(literal)) #adds it to the set variables (abs means it ignores negation)

    variables = list(variables)  #converts it into a list
    n = len(variables)  #finds and stores the number of variables

    assignment = {} #dictionary used to store assignments for each variable

    for x in range(n):
        assignment[variables[x]] = None #initally assigns all variables None

    
    change_made=True #if no changes are made then no more unit propogation can be performed 
    while (change_made==True):
        change_made=False #sets it as false so we know if any changes have been made
        for clause in clause_set:
            if(len(clause)==1): #for unit clauses
                var=abs(clause[0]) #gets the variable number and ignores negation 
                
                #case1: return contradiction 
                if(assignment[var]!=None): #checks whether unit clause already assigned value
                    if(clause[0]<0 and assignment[var] ==True): #if literal is negative and value true --> contradiction
                        return False, assignment, clause_set #returning assignment and set so that formatting later works
                    elif(assignment[var]==False): #if literal is false, clause false --> contradiction
                        return False, assignment, clause_set #returning assignment so that formatting later works

                
                if(clause[0] <0): #if literal is negative, then for the clause to be true the var must be false
                    assignment[var] = False
                else: #if literal is not negative then it must be true to satisfy the clause
                    assignment[var] = True
                clause_set.remove(clause) #removed satisfied clause from clause set
                change_made=True # change = unit clause removed
                break
           
            clause_found = False

            for literals in clause:
                var = abs(literals) #gets variable number and ignores negation
                value = assignment.get(var) #gets true/false
                if (value is None): #if value hasn't been assigned just continue 
                    continue
                if (literals < 0):  # if literal is negative, invert the value
                    value = not value
                if (value==True):  #if at least one literal is True, clause is satisfied and can be removed
                    clause_found = True
                    break #no need to go though other literals in clause
                elif(value==False): #if a literal's value is false, it can be removed from the clause
                    clause.remove(literals) 
                    change_made=True # change = false literal removed
            if( clause_found==True): #if clause is satisfied, it can be removed
                clause_set.remove(clause)
                change_made=True #change = satisfied clause removed
        
        
        if(len(clause_set)==0): # case2: no clauses left, return dictionary of variables and assignments
            return True, assignment, clause_set # returning true so that formatting works
        
    #case3: returns clauses that can't be worked upon any further and assignments
    return True, assignment, clause_set

def dpll_sat_solve(clause_set, partial_assignment):
    variables = set() #set is an ordered non repeating list of elements
    for clause in clause_set: #loops through each clause
        for literal in clause: #loops through each item in clause
            variables.add(abs(literal)) #adds it to the set variables (abs means it ignores negation)

    variables = list(variables)  #converts it into a list
    n = len(variables)  #finds and stores the number of variables

    assignment = {} #dictionary used to store assignments for each variable

    for x in range(n):
        assignment[variables[x]] = None #initally assigns all variables None

    for x in partial_assignment:
        if(x<0):
            assignment[abs(x)] = False
        else:
            assignment[x] = True
    
    def propagation(clause_set, assignment):
        change_made=True #if no changes are made then no more unit propogation can be performed 
        while (change_made==True):
            change_made=False #sets it as false so we know if any changes have been made
            for clause in clause_set:
                if(len(clause)==1): #for unit clauses
                    var=abs(clause[0]) #gets the variable number and ignores negation 
                
                    #case1: return contradiction 
                    if(assignment[var]!=None): #checks whether unit clause already assigned value
                        if(clause[0]<0 and assignment[var] ==True): #if literal is negative and value true --> contradiction
                            return False, assignment, clause_set #returning assignment and set so that formatting later works
                        elif(assignment[var]==False): #if literal is false, clause false --> contradiction
                            return False, assignment, clause_set #returning assignment so that formatting later works

                
                    if(clause[0] <0): #if literal is negative, then for the clause to be true the var must be false
                        assignment[var] = False
                    else: #if literal is not negative then it must be true to satisfy the clause
                        assignment[var] = True
                    clause_set.remove(clause) #removed satisfied clause from clause set
                    change_made=True # change = unit clause removed
                    break
           
                clause_found = False

                for literals in clause:
                    var = abs(literals) #gets variable number and ignores negation
                    value = assignment.get(var) #gets true/false
                    if (value is None): #if value hasn't been assigned just continue 
                        continue
                    if (literals < 0):  # if literal is negative, invert the value
                        value = not value
                    if (value==True):  #if at least one literal is True, clause is satisfied and can be removed
                        clause_found = True
                        break #no need to go though other literals in clause
                    elif(value==False): #if a literal's value is false, it can be removed from the clause
                        clause.remove(literals) 
                        change_made=True # change = false literal removed
                if( clause_found==True): #if clause is satisfied, it can be removed
                    clause_set.remove(clause)
                    change_made=True #change = satisfied clause removed
        
        
            if(len(clause_set)==0): # case2: no clauses left, return dictionary of variables and assignments
                return True, assignment, clause_set # returning true so that formatting works
        
        #case3: returns clauses that can't be worked upon any further and assignments
        return True, assignment, clause_set




    def checker(clause_set, assignment): #this checks whether current assignments work
        
        for clause in clause_set:
            FoundTrue = False #is true if the individual clause is true
            for literal in clause:
                var = abs(literal) #gets variable number and ignores negation
                value = assignment.get(var) #gets true/false
                if (value is None):
                    continue
                if (literal < 0):  # if literal is negative, invert the value
                    value = not value
                if (value==True):  #if at least one literal is True, clause is satisfied
                    FoundTrue = True
                    break
            if not FoundTrue: #if no literal was true, whole thing false
                return False
        return True
    
    def Sat_Solver(assignment):
        if (checker(clause_set, assignment)==True): #if the current assignments work, the program will return the assignments 
            return assignment
        j=0
        finished = True
        for j in range(n): #if any of the variables don't have assignments then the work isn't finished
            if(assignment[variables[j]] == None):
                finished = False
                break

        if(finished== True): #if it is finished it will have already been checked in the first if statement
            if(checker(clause_set, assignment)==False): #this means it's likely that the current assignments don't work
                return False
        else:
            unassignedVar = variables[j] # this uses the loop we used earlier to find the first variable that has not been assigned
            assignment[unassignedVar] = True #first sets it to true (just to try it out)
            result = Sat_Solver(assignment) #if this doesn't work it will return false
            if (result is not False): #if it doesn't then it works (so far)
                return result #the process will repeat until all the variables have been assigned ard are correct
            
            assignment[unassignedVar] = False #if setting the variable as true didn't work
            return Sat_Solver(assignment) #it will try setting it as false, if this doesn't work the whole premise is wrong
    
    result, assignment, clause_set = propagation(clause_set, assignment)

    if(result == False):
        return False
    elif(len(clause_set) == 0):
        return assignment
    else:
        return Sat_Solver(assignment)
        

clause_set = [
    [1, 2, 3],   # (x1 ∨ x2 ∨ x3)
    [-1, 2],     # (¬x1 ∨ x2)
    [-2, 3],     # (¬x2 ∨ x3)
    [1, -3]      # (x1 ∨ ¬x3)
]
partial_assignment = [3]

dpll_sat_solve(clause_set,partial_assignment)
    
    
    
    
    


           
           
           
            

                    







