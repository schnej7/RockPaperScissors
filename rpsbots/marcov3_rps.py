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

class bayes:
    def __init__( self ):
        self.hist_probs = dict()

    def record( self, prev, cur ):
        if prev not in self.hist_probs.keys():
            self.hist_probs[prev] = dict()
            self.hist_probs[prev][cur] = 1
        elif cur not in self.hist_probs[prev].keys():
            self.hist_probs[prev][cur] = 1
        else:
            self.hist_probs[prev][cur] += 1

    def predict( self, prev ):
        if cur not in self.hist_probs.keys():
            return random.choice( choices )
        else:
            return max(self.hist_probs[cur].iterkeys(), key=lambda k: self.hist_probs[cur][k])


if input == '':
    bayes1 = bayes()
    turn = 0
    output = 'R'
    in_hist = list( ['x'] * depth )
    out_hist = list( ['x'] * (depth) ) + ['R']

else:
    depth_end = len( in_hist ) - ( 1 )
    depth_begin = len( in_hist ) - ( depth + 1 )
    prev = str( in_hist[ depth_begin:depth_end ] ) + str( out_hist[ depth_begin:depth_end ] )

    cur_end = len( in_hist )
    cur_begin = len( in_hist ) - ( depth )
    cur = str( in_hist[ cur_begin:cur_end ] ) + str( out_hist[ cur_begin:cur_end ] )

    turn += 1
    in_hist += list( input )
    bayes1.record( prev, input )
    output = beats( bayes1.predict( cur ) )
    out_hist += list( output )
