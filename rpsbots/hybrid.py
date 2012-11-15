# See http://overview.cc/RockPaperScissors for more information about rock, paper, scissors
# A hybrid between switching and bayes bot. Randomly choose one of these two strategies
# The idea of this approach is, that it should become more difficult to predict the
# playing style of this bot

if input == '':
    import random
    import collections
    import operator
    rps = ['R', 'P', 'S']
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}
    cede = {'R': 'S', 'P': 'R', 'S': 'P'}
    score = {'RR': 0, 'PP': 0, 'SS': 0, 'PR': 1, 'RS': 1, 'SP': 1,'RP': -1, 'SR': -1, 'PS': -1,}
    cscore = {'RR': 't', 'PP': 't', 'SS': 't', 'PR': 'b', 'RS': 'b', 'SP': 'b','RP': 'c', 'SR': 'c', 'PS': 'c',}
    beatboth = {'RR': 'P', 'PP': 'S', 'SS': 'R', 'PR': 'P', 'RS': 'R', 'SP': 'S','RP': 'P', 'SR': 'R', 'PS': 'S',}
    def shift(n, move):
        for i in range(n%2):
            move = beat[move]
        return move

    def unshift(n, move):
        for i in range(n%2):
            move = cede[move]
        return move

    def counter_prob(probs):
        weighted_list = []
        for h in ['R', 'P', 'S']:
            weighted = 0
            for i, p in enumerate(probs):
                points = score[h+rps[i]]
                weighted += points * p
            weighted_list.append((h, weighted))

        m = max(weighted_list, key=operator.itemgetter(1))[1]
        candidates = [e[0] for e in weighted_list if e[1] == m]
        return random.choice(candidates)
    hist = ""
    patterns = collections.defaultdict(lambda: 10)
    output = random.choice(rps)
    candidates = []
    performance = [0] * 150
    results = [0, 0, 0] # losses, ties, wins
    opp = my = opp2 = my2 = ""
else:
    results[score[output+input]+1] += 1
    losses, ties, wins = results

    if opp and my:
        patterns['ao'+cscore[input+opp]] += 1
        patterns['am'+cscore[input+my]] += 1
    if opp2 and my2:
        patterns['ao2'+cscore[input+opp2]] += 1
        patterns['am2'+cscore[input+my2]] += 1

    patterns['1o'+opp+input] += 1
    patterns['1m'+my+input] += 1
    patterns['1b'+my+opp+input] += 1
    patterns['2o'+opp2+input] += 1
    patterns['2m'+my+input] += 1
    patterns['2b'+my+opp+input] += 1

    for i in range(min(1+len(hist)/2,6), 0, -1):
        patterns[hist[-i*2:]+input] += 1
        pattern = patterns.get(hist[-i*2:], "")
        if pattern:
            for j in range(min(1+len(pattern)/2,6), 0, -1):
                idx = pattern[-j*2:].lower()
                patterns[idx] = patterns.get(idx, "") + output + input
        patterns[hist[-i*2:]] = pattern + output + input

    for i, c in enumerate(candidates):
        if score[c+input] == 1:
            performance[i] += 1
        else:
            performance[i] = 0

    hist += output+input

    my = opp = my2 = opp2 = ""
    for i in range(min(1+len(hist)/2,6), 0, -1):
        pattern = patterns.get(hist[-i*2:], "")
        if pattern:
            my, opp = pattern[-2:]
            for j in range(min(1+len(pattern)/2,6), 0, -1):
                 pattern2 = patterns.get(pattern[-j*2:].lower(), "")
                 if pattern2 != "":
                      my2, opp2 = pattern2[-2:]
                      break
            break
    else:
        candidates = []

    if my and opp:
        candidates = [opp, my, beat[opp], cede[opp], beat[my], cede[my]]
        for i, a in enumerate(candidates[:]):
            for offset in range(3):
                candidates.extend([shift(offset+wins, a), shift(offset+wins+ties, a), shift(offset+losses+ties, a), shift(offset+losses, a)])
                candidates.extend([unshift(offset+wins, a), unshift(offset+wins+ties, a), unshift(offset+losses+ties, a), unshift(offset+losses, a)])

    probs = [1, 1, 1]
    if my and opp:
        probs = [p * patterns['1o'+opp+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['1m'+my+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['1b'+my+opp+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['ao'+cscore[h+opp]] for p,h in zip(probs, rps)]
        probs = [p* patterns['ao'+cscore[h+my]] for p,h in zip(probs, rps)]
                
    if my2 and opp2:
        probs = [p * patterns['2o'+opp2+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['2m'+my2+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['2b'+my2+opp2+h] for p,h in zip(probs, rps)]
        probs = [p * patterns['ao2'+cscore[h+my2]] for p,h in zip(probs, rps)]
        probs = [p * patterns['am2'+cscore[h+my2]] for p,h in zip(probs, rps)]

    s = random.choice(['S', 'B', 'R'])
    if s == 'S':
        output = random.choice(rps)
        if candidates:
            m = max(performance)
            output = random.choice([candidates[i] for i, p in enumerate(performance) if p == m])
    elif s == 'B':
        output = counter_prob(probs)
    else:
        output = beat[random.choice(list(hist))]
