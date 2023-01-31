from ortools.linear_solver import pywraplp

def prepare_input():
    f = open("SolomonPotvinBengio/rc_207.4.txt", "r")
    N = int(f.readline())
    t = list()
    R = list()
    D = list()
    for i in range(N):
        Ti = f.readline().split(' ')
        for j in range(N):
            t.append(int(float(Ti[j])))
        t.append(0)

    for i in range(N):
        TW = list(filter(None, f.readline().split(' ')))
        R.append(int(float(TW[0])))
        D.append(int(float(TW[1])))
        # R.append(0)
        # D.append(1000)
    R.append(0)
    D.append(10000)
    return N, t, R, D 

def main():
    # init 
    N, t, R, D = prepare_input()
    max_boundary = max(D)

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()

    # Creates the variables.
    # x_i_j
    x = list()
    for i in range(N):
        for j in range(N + 1):
            x.append(solver.IntVar(0, 1, 'x_{}_{}'.format(i, j)))

    # t_i
    T = list()
    for i in range(N + 1):
        T.append(solver.IntVar(0, max_boundary, 'T_{}'.format(i)))


    # constraints
    for i in range(1, N):
        solver.Add(T[i] - T[0] - t[0 * (N + 1) + i] * x[0 * (N + 1) + i] >= 0)

    for i in range(0, N):
        solver.Add(T[i] >= R[i])

    for i in range(N):
        solver.Add(x[i * (N + 1) + i] == 0)

    for i in range(N):
        solver.Add(solver.Sum(x[i * (N + 1) + j] for j in range(N + 1)) == 1)

    for i in range(1, N + 1):
        solver.Add(solver.Sum(x[j * (N + 1) + i] for j in range(N)) == 1)

    solver.Add(x[N] == 0)

    for i in range(1, N):
        for j in range(1, N + 1):
            if (i == j):
                continue
            solver.Add(T[i] - T[j] + (D[i] - R[j] + t[i * (N + 1) + j]) * x[i * (N + 1) + j] <= D[i] - R[j])

    for i in range(0, N):
        solver.Add(T[i] <= D[i])


    print('Number of constraints =', solver.NumConstraints())

    solver.Minimize(T[N] - T[0])


    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())

        for i in range(N + 1):
            print(T[i].solution_value(), R[i], D[i])

        for i in range(N):
            print([x[i * (N + 1) + j].solution_value() for j in range(N + 1)])
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()