import cplex
from docplex.mp.model import Model

# Simple test to create a model
model = Model(name="test_model")
x = model.binary_var(name="x")
y = model.binary_var(name="y")
model.maximize(x + y)
model.add_constraint(x + y <= 1)

solution = model.solve()

print(solution)
