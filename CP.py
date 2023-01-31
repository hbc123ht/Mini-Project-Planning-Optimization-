"""Simple solve."""
from ortools.sat.python import cp_model

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

    for i in range(N):
        TW = list(filter(None, f.readline().split(' ')))
        R.append(int(float(TW[0])))
        D.append(int(float(TW[1])))

    return N, t, R, D 
    

def main():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # init 
    N, t, R, D = prepare_input()
    max_boundary = max(D)

    # Creates the variables.
    P = list()
    for i in range(N):
        P.append(model.NewIntVar(0, N - 1, f'P_{i}'))

    T = list()
    for i in range(N):
        T.append(model.NewIntVar(0, max_boundary, f'P_{i}'))

    
    # Init Tp
    T_P = list()
    for i in range(N):
        # T_P[i] = T[P[i]]
        T_P.append(model.NewIntVar(0, max_boundary, f'T_P_{i}'))
        model.AddElement(P[i], T, T_P[i])

    # init P_i_i+1
    P_i_i1 = list()
    for i in range(N - 1):
        P_i_i1.append(model.NewIntVar(0, max_boundary, f'P_i_i1{i}'))
        model.Add(P_i_i1[i] == P[i] * N + P[i + 1])

    # init t_p_p
    t_P_P = list()
    for i in range(N-1):
        # t_P_P[i] = t[P[i] * N + P[j]]
        t_P_P.append(model.NewIntVar(0, max_boundary, f't_P_P{i}'))
        model.AddElement(P_i_i1[i], t, t_P_P[i])

    # init R_P, D_P
    R_P = list()
    D_P = list()
    for i in range(N):
        R_P.append(model.NewIntVar(0, max_boundary, f'T_P_{i}'))
        D_P.append(model.NewIntVar(0, max_boundary, f'D_P_{i}'))
        model.AddElement(P[i], R, R_P[i])
        model.AddElement(P[i], D, D_P[i])

    # Creates the constraints.
    
    model.AddAllDifferent(P)

    model.Add(P[0] == 0)
    for i in range(N - 1):
        model.Add(T_P[i] + t_P_P[i] <= T_P[i + 1])

    for i in range(N):
        model.Add(T_P[i] >= R_P[i])
        model.Add(T_P[i] <= D_P[i])

    model.Minimize(T_P[N - 1] - T_P[0])

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
        
        # for i in range(1, N):
        #     print(f'P_{i} = {solver.Value(P[i])}, T_P_{i} = {solver.Value(T_P[i])}, t_P_P{i} = {solver.Value(t_P_P[i - 1])}')
        for i in range(N):
            print(solver.Value(P[i]), solver.Value(T_P[i]), R[solver.Value(P[i])], D[solver.Value(P[i])])
        with open('sol.txt', 'w') as f:
            for i in range(1, N):
                f.write(f'{solver.Value(P[i])} ')
    else:
        print('No solution found.')

    # Statistics.
    print('\nStatistics')
    print(f'  status   : {solver.StatusName(status)}')
    print(f'  conflicts: {solver.NumConflicts()}')
    print(f'  branches : {solver.NumBranches()}')
    print(f'  wall time: {solver.WallTime()} s')


if __name__ == '__main__':
    main()