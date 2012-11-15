import random

def beats( a ):
    if a == 'R':
        return 'P'
    if a == 'P':
        return 'S'
    if a == 'S':
        return 'R'

choices = list(['R','P','S'] )
num_algos = 5
depth1 = 1
depth2 = 4
depth3 = 4
depth4 = 2
depth5 = 3

max_depth = max( list( [ depth1, depth2, depth3 ] ) )

class bootstrap:
    def __init__( self, num ):
        self.guess_hist = []
        self.good_hist = [[0] * (num + 1)]
        self.good = [0] * (num + 1)
        self.prev = [None] * (num+1)
        self.turn = [0] * (num+1)

    def update( self, actual_prev ):
        good_hist_row = []
        for i in range( len(self.prev) ):
            if i < len(self.prev) and self.prev[i] != None and self.prev[i] == actual_prev:
                self.good[i] += 1
            if self.turn[i] != 0:
                good_hist_row.append( float( self.good[i] ) / float( self.turn[i] ) )
            else:
                good_hist_row.append( 0 )
        self.good_hist.append( good_hist_row )

    def predict( self, guesses ):
        freq = dict()
        for choice in choices:
            freq[choice] = 0

        legit_guess = False
        for i in range( len(guesses) ):
            if guesses[i] != None:
                self.turn[i] += 1
                legit_guess = True
                freq[ guesses[i] ] += float( self.good[i] ) / float( self.turn[i] )
            self.prev[i] = guesses[i]

        #If no algorithm knows, then just guess
        if not legit_guess:
            return random.choice( choices )
        max_freq = max(freq.iterkeys(), key=lambda k: freq[k])
        sum_freq = sum( freq.values() )
        max_freq_val = freq[ max_freq ]
        if sum_freq > 0:
            self.guess_hist.append( max_freq_val / sum_freq )
        self.prev[ num_algos ] = max_freq
        self.turn[ num_algos ] += 1
        return beats( self.prev[ num_algos ] )

    def plot( self ):
        print sum( self.guess_hist ) / float( len( self.guess_hist ) )

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
            return None
        else:
            return max(self.hist_probs[cur].iterkeys(), key=lambda k: self.hist_probs[cur][k])


if input == '':
    turn = 0
    boot = bootstrap( num_algos )
    m1 = marcov()
    m2 = marcov()
    m3 = marcov()
    m4 = marcov()
    m5 = marcov()
    output = 'R'
    in_hist = list( ['x'] * max_depth )
    out_hist = list( ['x'] * (max_depth) ) + ['R']

else:
    turn += 1
    #if turn % 999 == 0:
    #    boot.plot()

    guesses = [None] * num_algos

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
    guesses[0] = m1.predict( cur1 )

    #m2
    depth_end2 = len( in_hist ) - ( 1 )
    depth_begin2 = len( in_hist ) - ( depth2 + 1 )
    prev2 = str( in_hist[ depth_begin2:depth_end2 ] )

    cur_end2 = len( in_hist )
    cur_begin2 = len( in_hist ) - ( depth2 )
    cur2 = str( in_hist[ cur_begin2:cur_end2 ] )

    m2.record( prev2, input )
    guesses[1] = m2.predict( cur2 )

    #m3
    depth_end3 = len( in_hist ) - ( 1 )
    depth_begin3 = len( in_hist ) - ( depth3 + 1 )
    prev3 = str( out_hist[ depth_begin3:depth_end3 ] )

    cur_end3 = len( in_hist )
    cur_begin3 = len( in_hist ) - ( depth3 )
    cur3 = str( out_hist[ cur_begin3:cur_end3 ] )

    m3.record( prev3, out_hist[-1] )
    guesses[2] = beats( m3.predict( cur3 ) )

    #m4
    depth_end4 = len( in_hist ) - ( 1 )
    depth_begin4 = len( in_hist ) - ( depth4 + 1 )
    prev4 = str( in_hist[ depth_begin4:depth_end4 ] ) + str( out_hist[ depth_begin4:depth_end4 ] )

    cur_end4 = len( in_hist )
    cur_begin4 = len( in_hist ) - ( depth4 )
    cur4 = str( in_hist[ depth_begin4:depth_end4 ] ) + str( out_hist[ cur_begin4:cur_end4 ] )

    m4.record( prev4, input )
    guesses[3] = m4.predict( cur4 )

    #m5
    depth_end5 = len( in_hist ) - ( 1 )
    depth_begin5 = len( in_hist ) - ( depth5 + 1 )
    prev5 = str( out_hist[ depth_begin5:depth_end5 ] )

    cur_end5 = len( in_hist )
    cur_begin5 = len( in_hist ) - ( depth5 )
    cur5 = str( out_hist[ cur_begin5:cur_end5 ] )

    m5.record( prev5, out_hist[-1] )
    guesses[4] = beats( m5.predict( cur5 ) )

    #guess

    #boost on all marcov chains
    boot.update( input )
    output = boot.predict( guesses )

    #record guess
    out_hist += list( output )
