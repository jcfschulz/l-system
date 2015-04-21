import numpy as np
import time

import pylab as plt
import matplotlib.lines as plt_lines

def string_replacement(axiom, productions, n): 
  s = axiom
  for i in range(n):
    snew = ""
    for c in s:
      if productions.has_key(c):
        snew += productions[c]
      else:
        snew += c
    s = snew
  return s

def turtle_points(s, delta, d, draw_on="F"):
  start = np.array([0.,0.])
  turn = lambda delta: np.round( np.array([[np.cos(delta),-np.sin(delta)],[np.sin(delta),np.cos(delta)]]), 10 )
  v = np.array([0.,d])
  points = []
  points.append(start)
  p = start
  for c in s:
    if c=="-":
      v = np.dot(v,turn(delta))
    elif c=="+":
      v = np.dot(v,turn(-delta))
    elif draw_on.find(c)>=0:
      points.append(points[-1]+v)
  return points

def turtle_lines(s, delta, d, draw_on="F", draw_off="f"):
  start = np.array([0.,0.])
  turn = lambda delta: np.round( np.array([[np.cos(delta),-np.sin(delta)],[np.sin(delta),np.cos(delta)]]), 10 )
  v = np.array([0.,d])
  lines = []
  p = start
  for c in s:
    if c=="-":
      v = np.dot(v,turn(delta))
    elif c=="+":
      v = np.dot(v,turn(-delta))
    elif draw_off.find(c)>=0:
      p = p+v
    elif draw_on.find(c)>=0:
      lines.append([p,p+v])
      p = p+v
  return lines

#axiom = "-L"
#productions = {"L": "LF+RFR+FL-F-LFLFL-FRFR+", "R": "-LFLF+RFRFR+F+RF-LFL-FR"}
#delta = np.pi/2.
#d = 1.

#axiom = "F-F-F-F"
#productions = {"F": "F-F+F+FF-F-F+F"}
#delta = np.pi/2.
#d = 1.

#axiom = "F"
#productions = {"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"}
#delta = np.pi/3.
#d = 1.

#axiom = "-F"
#productions = {"F": "F+F-F-F+F"}
#delta = np.pi/2.
#d = 1.

#axiom = "F-F-F-F"
#productions = {"F": "F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}
#delta = np.pi/2.
#d = 1.

#axiom = "F-F-F-F"
#productions = {"F": "FF-F--F-F"}
#delta = np.pi/2.
#d = 1.

#axiom = "F-F-F-F"
#productions = {"F": "F-FF--F-F"}
#delta = np.pi/2.
#d = 1.

#axiom = "G"
#productions = {"F": "G+F+G", "G": "F-G-F"}
#delta = np.pi/3.
#d = 1.

#axiom = "F"
#productions = {"F": "F+G+", "G": "-F-G"}
#delta = np.pi/2.
#d = 1.

#axiom = "---F"
#productions = {"F": "F++F----F++F"}
#delta = np.pi/6.
#d = 1.

#axiom = "F++F++F"
#productions = {"F": "F-F++F-F"}
#delta = np.pi/3.
#d = 1.

#axiom = "F-F-F-F"
#productions = {"F": "FF-F-F-F-FF"}
#delta = np.pi/2.
#d = 1.

axiom = "F+F+F+F"
productions = {"F": "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", "f": "ffffff"}
delta = np.pi/2.
d = 1.

n = 2
t1 = time.time()
s = string_replacement(axiom, productions, n)
t2 = time.time()
print "time for string replacement: ", t2-t1, "s" 
lines = turtle_lines(s, delta, d, "FG")
t3 = time.time()
print "number of lines: ", len(lines)
print "time for lines creation: ", t3-t2, "s" 


fig, ax = plt.subplots()
for l in lines:
  #ax.add_line(plt_lines.Line2D(*zip(*l), color='blue'))
  plt.plot(*zip(*l), color="b")
plt.margins(x=.1, y=.1)
plt.show()