import random

def beats( a ):
    if a == 'R':
        return 'P'
    if a == 'P':
        return 'S'
    if a == 'S':
        return 'R'

choices = list(['R','P','S'] )
depth1 = 3
depth2 = 5
depth3 = 2

max_depth = max( list( [ depth1, depth2, depth3 ] ) )

class marcov:
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

    def predict( self, cur ):
        if cur not in self.hist_probs.keys():
            return random.choice( choices )
        else:
            return max(self.hist_probs[cur].iterkeys(), key=lambda k: self.hist_probs[cur][k])


if input == '':
    m1 = marcov()
    m2 = marcov()
    m3 = marcov()
    output = 'R'
    in_hist = list( ['x'] * max_depth )
    out_hist = list( ['x'] * (max_depth) ) + ['R']

else:
    #record the last move
    in_hist += list( input )

    #train

    #m1
    depth_end1 = len( in_hist ) - ( 1 )
    depth_begin1 = len( in_hist ) - ( depth1 + 1 )
    prev1 = str( in_hist[ depth_begin1:depth_end1 ] ) + str( out_hist[ depth_begin1:depth_end1 ] )

    cur_end1 = len( in_hist )
    cur_begin1 = len( in_hist ) - ( depth1 )
    cur1 = str( in_hist[ cur_begin1:cur_end1 ] ) + str( out_hist[ cur_begin1:cur_end1 ] )

    m1.record( prev1, input )

    #m2
    depth_end2 = len( in_hist ) - ( 1 )
    depth_begin2 = len( in_hist ) - ( depth2 + 1 )
    prev2 = str( in_hist[ depth_begin2:depth_end2 ] )

    cur_end2 = len( in_hist )
    cur_begin2 = len( in_hist ) - ( depth2 )
    cur2 = str( in_hist[ cur_begin2:cur_end2 ] )

    m2.record( prev2, input )

    #m3
    depth_end3 = len( in_hist ) - ( 1 )
    depth_begin3 = len( in_hist ) - ( depth3 + 1 )
    prev3 = str( in_hist[ depth_begin3:depth_end3 ] ) + str( out_hist[ depth_begin3:depth_end3 ] )

    cur_end3 = len( in_hist )
    cur_begin3 = len( in_hist ) - ( depth3 )
    cur3 = str( in_hist[ cur_begin3:cur_end3 ] ) + str( out_hist[ cur_begin3:cur_end3 ] )

    m3.record( prev3, input )

    #guess

    #boost on all marcov chains
    freq = dict()
    for choice in choices:
        freq[choice] = 0
    freq[ m1.predict( cur1 ) ] += 1
    freq[ m2.predict( cur2 ) ] += 1
    freq[ m3.predict( cur3 ) ] += 1
    max_freq = max(freq.iterkeys(), key=lambda k: freq[k])
    max_freq_val = freq[ max_freq ]
    ties = 0
    for key in freq.keys():
        if freq[key] == max_freq_val:
            ties += 1
    if ties > 1:
        #if there is a tie then use the best chain
        output = beats( m1.predict( cur1 ) )
    else:
        output = beats( max_freq )

    #record guess
    out_hist += list( output )
