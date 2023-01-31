import math

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
    
    def back_tracking(u, T, P):
        if (len(P) == N):
            return T
        re = math.inf
        for next_node in range(N):
            if next_node not in P:
                if (T + t[u * N + next_node] <= D[next_node]):
                    P.append(next_node)
                    re = min(re, back_tracking(next_node, max(T + t[u * N + next_node], R[next_node]), P))
                    P.pop()
                
        return re

    N, t, R, D = prepare_input()
    result = math.inf
    for i in range(R[0], D[0]):
        result = min(result, back_tracking(0, i, [0]) - i)

    print(f"Minimize value is {result}")


if __name__ == '__main__':
    main()