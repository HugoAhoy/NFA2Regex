from collections import deque

epsilon = float("inf")

def make_NFA(graph):
    pass

def get_ECLOSE(s, transition):
    """
    Get epsilon closure of state s.
    """
    res = []
    q = deque()
    q.append(s)
    while len(q) > 0:
        head_state = q.popleft()
        res.append(head_state)
        for state in transition[head_state][epsilon]:
            if state not in res:
                q.append(state)
    return res

def extend_delta(s, symbol, transition, eclose_dict):
    res = []
    dest_states = transition[s][symbol]
    for ds in dest_states:
        for s in eclose_dict[ds]:
            if s not in res:
                res.append(s)
    return res


def dfa2regex(DFA):
    start = DFA["start"]
    finals = DFA["finals"]
    transition = DFA["trans"]
    symbols = list(transition[start].keys())
    states = list(transition.keys())
    graph = {}
    for state_i in states:
        graph[state_i] = {}
        for state_j in states:
            graph[state_i][state_j] = None

    for state, trans in transition.items():
        for sym, dest in trans.items():
            if graph[state][dest] is not None:
                graph[state][dest] = graph[state][dest] + '|' + sym
            else:
                graph[state][dest] = sym
    
    print(graph)
    
    # TODO: 路径叠代法


def nfa2dfa(NFA):
    """
    A NFA is a dict, including start state, final states, transition table, symbols.
    NFA structure is 
    """
    start = NFA["start"] # str/int
    finals = NFA["finals"] # set(int/str)
    transition = NFA["trans"] # dict[state, dict[symbol, set(state)]]
    symbols = list(transition[start].keys()) # set(char)
    symbols.pop(symbols.index(epsilon))
    states = list(transition.keys())
    eclose_dict = {}
    for state in states:
        eclose_dict[state] = get_ECLOSE(state, transition)
    Q = [set(eclose_dict[start])]
    T = {}
    q = deque()
    q.append(set(eclose_dict[start]))
    while len(q) > 0:
        head_state_set = q.popleft()
        # Q.append(head_state_set)
        T[str(head_state_set)] = {}
        for sym in symbols:
            next_state = []
            # TODO: compute next states
            for hs in head_state_set:
                next_state = next_state + extend_delta(hs, sym, transition, eclose_dict)
            next_state = set(next_state)
            if next_state not in Q:
                print("*"*30)
                print("Q",Q)
                print("state",next_state)
                print("*"*30)
                Q.append(next_state)
                q.append(next_state)
            T[str(head_state_set)][sym] = str(next_state)

    print("T",T)
    print()
    print("Q",Q)
    print()
    # rename states
    name_dict = {}
    for i, state in enumerate(Q):
        name_dict[str(state)] = i
    new_T = {}
    for state, trans in T.items():
        new_T[name_dict[state]] = {}
        for sym, next_state in trans.items():
            new_T[name_dict[state]][sym] = name_dict[next_state]
    
    dfa_start = name_dict[str(set(eclose_dict[start]))]
    dfa_finals = []
    for state in Q:
        if any(i in state for i in finals):
            dfa_finals.append(name_dict[str(state)])
    return {
        "start":dfa_start,
        "finals":dfa_finals,
        "trans":new_T,
    }


def nfa2regex(NFA):
    dfa = nfa2dfa(NFA)
    regex = dfa2regex(dfa)
    return regex

if __name__ == "__main__":
    # NFA_example_1 = {
    #     "start":"p",
    #     "finals":["r","s"],
    #     "trans":{
    #         "p":{0:[],1:[],epsilon:[]},
    #         "q":{0:[],1:[],epsilon:[]},
    #         "r":{0:[],1:[],epsilon:[]},
    #         "s":{0:[],1:[],epsilon:[]},
    #     }
    # }

    NFA_example_2 = {
        "start":"p",
        "finals":["r"],
        "trans":{
            "p":{"a":[],"b":["q"],"c":["r"],epsilon:["q","r"]},
            "q":{"a":["p"],"b":["r"],"c":["p","q"],epsilon:[]},
            "r":{"a":[],"b":[],"c":[],epsilon:[]},
        }
    }
    
    start = NFA_example_2["start"]
    finals = NFA_example_2["finals"]
    transition = NFA_example_2["trans"]
    symbols = list(transition[start].keys())
    symbols.pop(symbols.index(epsilon))
    states = list(transition.keys())

    print("start",start)
    print("finals",finals)
    print("transition",transition)
    print("symbols",symbols)

    print("eclose")
    for state in states:
        print(state, get_ECLOSE(state, transition))
    
    dfa = nfa2dfa(NFA_example_2)
    print("DFA",dfa)

    dfa2regex(dfa)