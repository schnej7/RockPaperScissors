import copy
import random

'''
This is a very simplistic model.
Will try something more complex and interesting next.
'''

class SuffixTrie(object):
    '''
    Suffix Trie data structure that is used to hold the used sequences
    rock paper and scissors.
    '''

    def __init__(self):
        self.root = {'count':0}

    def insert_sequence(self, sequence):
        '''
        Inserts the sequence in the list sequence into the suffix trie.
        '''

        current = self.root
        current['count'] += 1
        for s in sequence:
            try:
                current = current[str(s)]
                current['count'] += 1
            except KeyError:
                current[str(s)] = {'count':1, 'value':s}
                current = current[str(s)]

    def delete_sequence(self, sequence):
        '''
        Removes the sequence from the trie and updates the counts.
        '''

        current = self.root
        for s in sequence:
            try:
                current = current[str(s)]
            except KeyError:
                return
        word_count = current['count']
        current = self.root
        current['count'] -= word_count
        for s in sequence:
            current = current[str(s)]
            current['count'] -= word_count
            if current['count'] <= 0:
                del current
                return

    def get_count(self, subseq=[]):
        '''
        Returns the total number of insertions into the suffix trie that begin
        with the subsequence subseq.  If the subsequence [] is used then it
        will return the number of sequences in the list.
        '''
        if subseq == []:
            return self.root['count']
        else:
            current = self.root
            for s in subseq:
                try:
                    current = current[str(s)]
                except KeyError:
                    return 0
            return current['count']

def cond_prob(move, seq, st):
    '''
    Returns the probability of the move given that the sequence.
    '''

    l = []
    for s in seq:
        l.append(s)
    l.append(move)
    #smoothing
    st.insert_sequence(l)
    
    seq_count = st.get_count(seq)
    move_count = st.get_count(l)
    
    
    st.delete_sequence(l)
    if seq_count == 0:
        return 0
    prob = float(move_count) / seq_count
    return prob

moves = ["R", "P", "S"]
beats = {"P":"S", "S":"R", "R":"P"}
if input == "":
    st = SuffixTrie()
    st.insert_sequence("RPS")
    sequence = []
    output = moves[random.randint(0, 2)]
    
else:
    window = 4 #4 seems like a good number
    sequence.append(input)
    if len(sequence) > 4:
        st.insert_sequence(sequence[-4:])
        current = sequence[-3:]

        p = cond_prob("P", current, st)
        s = cond_prob("S", current, st)
        r= cond_prob("R", current, st)
        
        if r > s and r > p:
            output = beats["R"]
        elif s > p and s > r:
            output = beats["S"]
        elif p > s and p > r:
            output = beats["P"]
        else:
            output = moves[random.randint(0, 2)] 

    else:
        output = moves[random.randint(0, 2)]
