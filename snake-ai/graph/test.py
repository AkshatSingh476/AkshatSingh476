from hamiltonian import Hamiltonian

# j is column (i.e. x) and i is row (i.e. y)
data = [[i*10+j for j in range(3)] for i in range(4)]
print(data)
print(data[1][0])   # first index is row, second is column

for j in range(3):
    print(j)

snake = []
ham = Hamiltonian(0, 0, 6, 6, snake)

if not ham.buildPath(1):
    print("Solution does not exist");
else:
    print("Solution exists");
    ham.printPath()
