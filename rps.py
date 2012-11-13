import random

def beats( a ):
    if a == 'R':
        return 'P'
    if a == 'P':
        return 'S'
    if a == 'S':
        return 'R'

choices = list(['R','P','S'] )
depth = 3

def record( cur ):
    depth_end = len( in_hist ) - ( 1 )
    depth_begin = len( in_hist ) - ( depth + 1 )
    prev = str( in_hist[ depth_begin:depth_end ] ) + str( out_hist[ depth_begin:depth_end ] )

    if prev not in hist_probs.keys():
        hist_probs[prev] = dict()
        hist_probs[prev][cur] = 1
    elif cur not in hist_probs[prev].keys():
        hist_probs[prev][cur] = 1
    else:
        hist_probs[prev][cur] += 1

def predict( ):
    cur_end = len( in_hist )
    cur_begin = len( in_hist ) - ( depth )
    cur = str( in_hist[ cur_begin:cur_end ] ) + str( out_hist[ cur_begin:cur_end ] )
    if cur not in hist_probs.keys():
        return random.choice( choices )
    else:
        return max(hist_probs[cur].iterkeys(), key=lambda k: hist_probs[cur][k])


if input == '':
    turn = 0
    hist_probs = dict()
    output = 'R'
    in_hist = list( ['x'] * depth )
    out_hist = list( ['x'] * (depth) ) + ['R']

else:
    turn += 1
    in_hist += list( input )
    record( input )
    output = beats( predict() )
    out_hist += list( output )
