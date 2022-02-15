from pprint import pprint

class TW_TapeAutomata:
    def __init__(self):
        self.Q = []
        self.S = []
        self.start = None
        self.accept = None
        self.reject = None
        self.debug = True

    
    def add_state(self, index, direction=None, transitions=[]):
        state = { 'direction': direction, 'index': index, 'next': {} }
        for t in transitions:
            state['next'][t[0]] = t[1]
            if not t[0] in self.S:
                self.S.append(t[0])
        self.Q.append(state)


    def set_accept(self, index):
        self.accept = index


    def set_reject(self, index):
        self.reject = index


    def parse(self, state, n):
        if 'accept' in state.lower():
            self.add_state(n+1, None, [])
            self.set_accept(n+1)
        elif 'reject' in state.lower():
            self.add_state(n+1, None, [])
            self.set_reject(n+1)
        else:
            input_string = state.split(' ')
            direction = input_string[0]
            transitions = []
            for i in input_string[1:]:
                t = i[1:-1]
                t = t.split(',')
                transitions.append((t[0].strip(), t[1].strip()))
            self.add_state(n+1, direction, transitions)

    
    def check_string(self, string):
        return all(s in self.S for s in string)

        
    def run_twa(self, string):
        idx = 1             # string index
        state = self.start  # initial state
        while True:
            if state['index'] == self.accept:       # accept
                print('Accept!')
                break
            elif state['index'] == self.reject:     # reject
                print('Reject!')
                break

            current = string[idx]

            if self.debug:
                print(f'State: {state["index"]}')
                print(f'Direction: {state["direction"]}')
                print(f'Character: {current}', end='\n==========================\n')

            next_state = state['next'][current]
            state = self.Q[int(next_state)-1]     # next state

            if state['direction'] == 'right':
                idx += 1
            else:
                idx -= 1

    
    def initialize_twa(self):
        self.start = self.Q[0]


    def display_twa(self):
        print()
        print('=== STATES ===')
        pprint(self.Q)
        print()
        print('=== STIMULUS/SYMBOLS ===')
        pprint(self.S)


TWA = TW_TapeAutomata()

try:
    # load from a file
    with open('a_odd_or_b_even.txt') as f:
        lines = f.readlines()
        print('=== PROGRAM ===')
        for i in range(len(lines)):
            if any(x in lines[i] for x in ['accept', 'reject']):
                line = ''.join(c for c in lines[i].split(' ')[1] if c != '\n')
            else:
                line = ' '.join(lines[i][:-1].split(' ')[1:])
            print(f'{i+1}) {line}')
            TWA.parse(line, i)
except FileNotFoundError as e:
    print('No test file found.', end='\n\n')
    # input program manually
    num = input('Number of states: ')
    if num not in ['', '0']:
        num = int(num)

        print('Enter program string:')
        for n in range(num):
            state = input(f'{n+1}) ')
            TWA.parse(state, n)

TWA.display_twa()

while True:
    string = input("\nType 'exit' to close\nEnter string: ")
    print()
    if string == 'exit':
        break
    if TWA.check_string(string):
        TWA.initialize_twa()
        TWA.run_twa(f'#{string}#')
    else:
        print('Invalid character found in string!\n')