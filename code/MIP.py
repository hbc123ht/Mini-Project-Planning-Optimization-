from ortools.linear_solver import pywraplp

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
    # init 
    data = prepare_input('Data/15points_3days_doChenh92costNho1_5.txt')

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()

    # Creates the variables.
    # x_i_j
    x = list()
    for i in range(data['n']):
        for j in range(data['n']):
            x.append(solver.IntVar(0, 1, 'x_{}_{}'.format(i, j)))

    # t_i
    T = list()
    for i in range(data['n']):
        T.append(solver.IntVar(0, max(data['late']), 'T_{}'.format(i)))


    # constraints
    for i in range(1, data['n']):
        solver.Add(T[i] - T[0] - data['time'][0 * data['n'] + i] * x[0 * data['n'] + i] >= 0)

    for i in range(data['n']):
        solver.Add(x[i * data['n'] + i] == 0)

    for i in range(data['n']):
        solver.Add(solver.Sum(x[i * data['n'] + j] for j in range(data['n'])) == 1)

    for i in range(1, data['n']):
        solver.Add(solver.Sum(x[j * data['n'] + i] for j in range(data['n'])) == 1)

    for i in range(data['n']):
        for j in range(1, data['n']):
            if (i == j):
                continue
            solver.Add(T[i] - T[j] + (data['late'][i] - data['early'][j] + data['delay'][i] + data['time'][i * data['n'] + j]) * x[i * data['n'] + j] <= data['late'][i] - data['early'][j])

    for i in range(0, data['n']):
        solver.Add(T[i] >= data['early'][i])
        solver.Add(T[i] <= data['late'][i])


    print('Number of constraints =', solver.NumConstraints())

    solver.Minimize(solver.Sum(data['cost'][i] * x[i] if i % data['n'] else 0 for i in range(data['n'] ** 2)))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())

        # for i in range(data['n']):
        #     print(T[i].solution_value(), data['early'][i], data['late'][i])

        # for i in range(data['n']):
        #     print([x[i * data['n'] + j].solution_value() for j in range(data['n'])])
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()