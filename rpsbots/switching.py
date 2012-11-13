# See http://overview.cc/RockPaperScissors for more information about rock, paper, scissors
# Similar to switching10 with an additional beat2 and complement function

import random

if input == "":
  hist = ""
  opp_played = []
  beat = {'P': 'S', 'S': 'R', 'R': 'P'}
  beat2 = {'PP': 'S', 'SS': 'R', 'RR':'P', 'PS': 'S', 'PR': 'P', 'RS': 'R', 'RP': 'P', 'SP': 'S', 'SR': 'R'}
  complement = {'PS': 'R', 'PR': 'S', 'RS': 'P', 'RP': 'S', 'SP': 'R', 'SR': 'P'}
  
  score = {'RR': 0, 'PP': 0, 'SS': 0, 'PR': 1, 'RS': 1, 'SP': 1,'RP': -1, 'SR': -1, 'PS': -1,}
  output = random.choice(["R", "P", "S"])

  candidates1 = [output, output]
  candidates2 = [output] * 5
  performance1 = [0, 0]
  performance2 = [(0,0)] * 5
else:
  hist += output.lower()+input
  opp_played.append(input)
  performance1[0] += score[candidates1[0]+input]
  performance1[1] += score[candidates1[1]+input]
  
  for i, p in enumerate(candidates2):
    performance2[i] = ({1:performance2[i][0]+1, 0: performance2[i][0], -1: 0}[score[p+input]],  
                   performance2[i][1]+score[p+input])

  index1 = performance1.index(max(performance1))
  index2 = performance2.index(max(performance2, key=lambda x: x[0]**3+x[1]))
  candidates1[1] = beat[random.choice(opp_played)]
  
  for length in range(min(10, len(hist)-2), 0, -2):
    search = hist[-length:]
    idx = hist.rfind(search, 0, -2)
    if idx != -1:
      my = hist[idx+length].upper()
      opp = hist[idx+length+1]
      candidates2[0] = beat[opp]
      candidates2[1] = beat[beat[my]]
      candidates2[2] = beat2[beat[my] + beat[beat[opp]]]
      candidates2[3] = beat2[beat[opp] + beat[beat[my]]]
      candidates2[4] = complement[''.join(sorted(set(candidates2[0] + candidates2[1] + candidates2[3])))]
      break
  else:
      candidates = [random.choice(['R', 'P', 'S'])] * 5
 
  candidates1[0] = candidates2[index2]
  
  output = candidates1[index1]
