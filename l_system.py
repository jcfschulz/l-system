import numpy as np


axiom = "-L"
productions = {"L": "LF+RFR+FL-F-LFLFL-FRFR+", "R": "-LFLF+RFRFR+F+RF-LFL-FR"}

n = 3

s = axiom
for i in range(n):
  snew = ""
  for c in s:
    if productions.has_key(c):
      snew += productions[c]
    else:
      snew += c
  s = snew
  #print "**", s

start = np.array([0.,0.])
delta = np.pi/2.
turn = lambda delta: np.array( [[np.cos(delta),-np.sin(delta)],[np.sin(delta),np.cos(delta)]])
v = np.array([1.,0.])

points.append(start)

for c in s:
  points.append()