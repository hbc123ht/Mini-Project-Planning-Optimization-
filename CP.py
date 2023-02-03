from ortools.sat.python import cp_model

def prepare_input(path):
    with open(path, 'r') as file: 
        n = int(file.readline()) + 1
        early = []
        late = []
        delay = []
        cost = []
        time = []
        for i in range(n):
            e, l, d = file.readline().strip().split(' ')
            early.append(int(e))
            late.append(int(l))
            delay.append(int(d))
            # delay.append(0)
        for i in range(n):
            for a in file.readline().strip().split(' '):
                cost.append(int(a))
        for i in range(n):
            for a in file.readline().strip().split(' '):
                time.append(int(a))
    data = {}
    data['n'] = n
    data['early'] = early
    data['late'] = late
    data['delay'] = delay
    data['cost'] = cost
    data['time'] = time
    return data
    

def main():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()
    # init 
    data = prepare_input('Data/25points_3days.txt')

    # Creates the variables.
    P = list()
    for i in range(data['n']):
        P.append(model.NewIntVar(0, data['n'] - 1, f'P_{i}'))

    T = list()
    for i in range(data['n']):
        T.append(model.NewIntVar(0, max(data['late']), f'T_{i}'))

    
    # Init Tp
    T_P = list()
    for i in range(data['n']):
        # T_P[i] = T[P[i]]
        T_P.append(model.NewIntVar(0, max(data['late']), f'T_P_{i}'))
        model.AddElement(P[i], T, T_P[i])
        
    # init P_i_i+1
    P_i_i1 = list()
    for i in range(data['n'] - 1):
        P_i_i1.append(model.NewIntVar(0, data['n'] ** 2, f'P_i_i1{i}'))
        model.Add(P_i_i1[i] == P[i] * data['n'] + P[i + 1])

    # init t_p_p
    t_P_P = list()
    cost_P_P = list()
    delay_P = list()
    for i in range(data['n']-1):
        # t_P_P[i] = t[P[i] * N + P[i + 1]]
        t_P_P.append(model.NewIntVar(0, max(data['time']), f't_P_P{i}'))
        model.AddElement(P_i_i1[i], data['time'], t_P_P[i])
        # cost_P_P[i] = data['cost'][P[i] * N + P[i + 1]]
        cost_P_P.append(model.NewIntVar(0, max(data['cost']), f't_P_P{i}'))
        model.AddElement(P_i_i1[i], data['cost'], cost_P_P[i])
        # delay_P[i] = delay[P[i]]
        delay_P.append(model.NewIntVar(0, max(data['delay']), f'delay_P_{i}'))
        model.AddElement(P[i], data['delay'], delay_P[i])

    # init R_P, D_P
    R_P = list()
    D_P = list()
    for i in range(data['n']):
        R_P.append(model.NewIntVar(0, max(data['late']), f'T_P_{i}'))
        D_P.append(model.NewIntVar(0, max(data['late']), f'D_P_{i}'))
        model.AddElement(P[i], data['early'], R_P[i])
        model.AddElement(P[i], data['late'], D_P[i])

    # Creates the constraints.
    
    model.AddAllDifferent(P)

    model.Add(P[0] == 0)
    for i in range(data['n'] - 1):
        model.Add(T_P[i] + t_P_P[i] + delay_P[i] <= T_P[i + 1])

    for i in range(data['n']):
        model.Add(T_P[i] >= R_P[i])
        model.Add(T_P[i] <= D_P[i])

    model.Minimize(sum(cost_P_P[i] for i in range(data['n'] - 1)))

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
        
        # for i in range(1, N):
        #     print(f'P_{i} = {solver.Value(P[i])}, T_P_{i} = {solver.Value(T_P[i])}, t_P_P{i} = {solver.Value(t_P_P[i - 1])}')
        # for i in range(data['n']):
        #     print(solver.Value(P[i]), solver.Value(T_P[i]), data['early'][solver.Value(P[i])], data['late'][solver.Value(P[i])])
        with open('sol.txt', 'w') as f:
            for i in range(1, data['n']):
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