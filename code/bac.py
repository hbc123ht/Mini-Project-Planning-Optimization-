import math

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

def back_tracking(u, current_time, current_cost, current_route):
    global best_cost
    if (best_cost < current_cost + (data['n'] - len(current_route)) * min_cost):
        return
    if (len(current_route) == data['n']):
        best_cost = min(best_cost, current_cost)
        return 
    re = math.inf
    for next_node in range(data['n']):
        if next_node not in current_route:
            if (current_time + data['time'][u * data['n'] + next_node] + data['delay'][u] <= data['late'][next_node]):
                current_route.append(next_node)
                back_tracking(next_node, \
                                max(current_time + data['time'][u * data['n'] + next_node] + data['delay'][u], data['early'][next_node]),\
                                current_cost + data['cost'][u * data['n'] + next_node], \
                                current_route)
                current_route.pop()
            
    return 

def main():
    
    global best_cost, data, min_cost
    best_cost = math.inf
    data = prepare_input('Data/10points_1day.txt')
    min_cost = min(data['cost'])
    import time
    # get the start time
    st = time.time()
    
    for i in range(data['early'][0], data['late'][0] + 1):
        back_tracking(0, i, 0, [0])
    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    print(f"Minimize value is {best_cost}")


if __name__ == '__main__':
    main()