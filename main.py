from docplex.mp.model import Model

# Define sets
conference_sessions = 40
slots = 7
length_of_paper_range = 4
NbrGrps = 20

Sessions = range(1, conference_sessions + 1)
Slots = range(1, slots + 1)
PaperRangeIndex = range(1, length_of_paper_range + 1)
Groups = range(1, NbrGrps + 1)

# Parameters
papers_range = [3, 4, 5, 6]
np = [14, 23, 12, 9, 9, 6, 10, 4, 10, 7, 6, 5, 3, 5, 6, 4, 3, 12, 7, 16, 4, 5, 14, 11, 4, 3, 10, 6, 6, 4, 13, 3, 4, 9, 5, 4, 11, 6, 6, 8]
npMax = [4, 6, 6, 4, 4, 5, 3]
max_parallel_sessions = 11
session_groups = [
    [1], [2], [3], [], [], [], [6], [7], [7, 8], [10], [8], [8, 11], [5, 8], 
    [3, 8], [7], [13], [13], [14], [], [8], [16], [16], [20], [17], [13], 
    [], [9], [11], [11, 12], [9], [6, 19], [], [], [18], [10], [5], [16], 
    [4, 5], [8, 12], [7, 15]
]

# Define sets
# conference_sessions = 3
# slots = 2
# length_of_paper_range = 2
# NbrGrps = 2

# Sessions = range(1, conference_sessions + 1)
# Slots = range(1, slots + 1)
# PaperRangeIndex = range(1, length_of_paper_range + 1)
# Groups = range(1, NbrGrps + 1)

# # Parameters
# papers_range = [2, 3]
# np = [3, 3, 3]
# npMax = [2, 3]
# max_parallel_sessions = 2
# session_groups = [[1], [2], [3]]



def var_x(s, c, l):
    return (s-1) * slots * length_of_paper_range + (c-1) * length_of_paper_range + l

max_var_x = var_x(conference_sessions, slots, length_of_paper_range)

def var_z(s, c):
    return max_var_x + (s - 1) * slots + c

# Model
mdl = Model()

# Decision Variables
x = {(s, c, l): mdl.integer_var(name=f'x_{s}_{c}_{l}') for s in Sessions for c in Slots for l in PaperRangeIndex}
y = mdl.integer_var_dict(((s1, s2, c, g) for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups), name="y")
z = {(s, c): mdl.binary_var(name=f'z_{s}_{c}') for s in Sessions for c in Slots}
session_allocated = mdl.binary_var_matrix(Sessions, Slots, name="session_allocated")

# Objective Function: Minimize working-group conflicts
num_conflicts = mdl.sum(y[s1, s2, c, g] for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups if g in session_groups[s1-1] and g in session_groups[s2-1])
mdl.minimize(num_conflicts)

# First Constraint: At most one amount of papers chosen for a (session, slot) pair
for s in Sessions:
    for c in Slots:
        mdl.add_constraint(mdl.sum(x[s, c, l] for l in PaperRangeIndex) <= 1)

# Second Constraint: Subdivision of a session into slots covers all the papers in the session
for s in Sessions:
    mdl.add_constraint(mdl.sum(x[s, c, l] * papers_range[l-1] for c in Slots for l in PaperRangeIndex) == np[s-1])

# Third Constraint: The subdivision respects the maximum length of each slot
for s in Sessions:
    for c in Slots:
        for l in PaperRangeIndex:
            if papers_range[l-1] > npMax[c-1]:
                mdl.add_constraint(x[s, c, l] == 0)

# Fourth Constraint: Number of parallel sessions is not exceeded for each slot
for c in Slots:
    mdl.add_constraint(mdl.sum(session_allocated[s, c] for s in Sessions) <= max_parallel_sessions)

# Implementing equivalence transformation for z variables
for s in Sessions:
    for c in Slots:
        z_var = z[s, c]
        x_vars = [x[s, c, l] for l in PaperRangeIndex]
        mdl.add_constraints(x_var <= z_var for x_var in x_vars)
        mdl.add_constraint(z_var <= mdl.sum(x_var for x_var in x_vars))

# Conflict constraints similar to Max-SAT with integer y_var
for s1 in Sessions:
    for s2 in Sessions:
        if s1 < s2:
            common_groups = set(session_groups[s1 - 1]).intersection(session_groups[s2 - 1])
            for c in Slots:
                for g in common_groups:
                    y_var = y[s1, s2, c, g]
                    # Conflict when both sessions are in the same slot
                    mdl.add_constraint(y_var >= z[s1, c] + z[s2, c] - 1)
                    for l1 in PaperRangeIndex:
                        for l2 in PaperRangeIndex:
                            # Conflict when both sessions have papers in the same slot
                            mdl.add_constraint(y_var >= x[s1, c, l1] + x[s2, c, l2] - 1)

# Solve the model
solution = mdl.solve()

# Display function
def display_assignments_by_slot_with_counts(model, slots, papers_range, conference_sessions):
    print("Assignment of Sessions to Slots with Paper Counts:")
    for s in Sessions:
        for c in Slots:
            for l in PaperRangeIndex:
                if x[s, c, l].solution_value > 0:  # Check if the variable is assigned
                    print(f"  Conference Session {s} in slot {c} with {papers_range[l-1]} papers")

if solution:
    print(f"Model has cost: {solution.objective_value}")
    display_assignments_by_slot_with_counts(solution, slots, papers_range, conference_sessions)
    # Print the number of conflicts
    total_conflicts = num_conflicts.solution_value
    print(f"Total number of conflicts: {total_conflicts}")
else:
    print("No solution found")