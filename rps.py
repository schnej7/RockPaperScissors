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
depth3 = 5
depth4 = 2

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
    turn = 0
    a1 = 0
    g1 = None
    m1 = marcov()
    a2 = 0
    g2 = None
    m2 = marcov()
    a3 = 0
    g3 = None
    m3 = marcov()
    a4 = 0
    g4 = None
    m4 = marcov()
    output = 'R'
    in_hist = list( ['x'] * max_depth )
    out_hist = list( ['x'] * (max_depth) ) + ['R']

else:
    turn += 1

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
    if g1 != None and g1 == beats( input ):
        a1 += 1

    #m2
    depth_end2 = len( in_hist ) - ( 1 )
    depth_begin2 = len( in_hist ) - ( depth2 + 1 )
    prev2 = str( in_hist[ depth_begin2:depth_end2 ] )

    cur_end2 = len( in_hist )
    cur_begin2 = len( in_hist ) - ( depth2 )
    cur2 = str( in_hist[ cur_begin2:cur_end2 ] )

    m2.record( prev2, input )
    if g2 != None and g2 == beats( input ):
        a2 += 1

    #m3
    depth_end3 = len( in_hist ) - ( 1 )
    depth_begin3 = len( in_hist ) - ( depth3 + 1 )
    prev3 = str( out_hist[ depth_begin3:depth_end3 ] )

    cur_end3 = len( in_hist )
    cur_begin3 = len( in_hist ) - ( depth3 )
    cur3 = str( out_hist[ cur_begin3:cur_end3 ] )

    m3.record( prev3, input )
    if g3 != None and g3 == beats( input ):
        a3 += 1

    #m4
    depth_end4 = len( in_hist ) - ( 1 )
    depth_begin4 = len( in_hist ) - ( depth4 + 1 )
    prev4 = str( in_hist[ depth_begin4:depth_end4 ] ) + str( out_hist[ depth_begin4:depth_end4 ] )

    cur_end4 = len( in_hist )
    cur_begin4 = len( in_hist ) - ( depth4 )
    cur4 = str( in_hist[ depth_begin4:depth_end4 ] ) + str( out_hist[ cur_begin4:cur_end4 ] )

    m4.record( prev4, input )
    if g4 != None and g4 == beats( input ):
        a4 += 1

    #guess

    #boost on all marcov chains
    freq = dict()
    for choice in choices:
        freq[choice] = 0

    g1 =  m1.predict( cur1 ) 
    g2 =  m2.predict( cur2 ) 
    g3 =  beats( beats (m3.predict( cur3 ) ) )
    g4 =  m4.predict( cur4 ) 
    freq[ g1 ] += float( a1 ) / float( turn )
    freq[ g2 ] += float( a2 ) / float( turn )
    freq[ g3 ] += float( a3 ) / float( turn )
    freq[ g4 ] += float( a4 ) / float( turn )

    max_freq = max(freq.iterkeys(), key=lambda k: freq[k])
    max_freq_val = freq[ max_freq ]
    ties = 0
    for key in freq.keys():
        if freq[key] == max_freq_val:
            ties += 1
    if ties > 1:
        #if there is a tie then use the first chain
        output = beats( m1.predict( cur1 ) )
    else:
        output = beats( max_freq )

    #record guess
    out_hist += list( output )
