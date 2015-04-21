import numpy as np
import time
import collada

import pylab as plt
import matplotlib.lines as plt_lines
from mpl_toolkits.mplot3d import Axes3D

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
  global turnU_matrix_minus, turnU_matrix_plus, turnU

  p = np.array([0.,0.,0.])
  hlu = np.array([[d,0.,0.], [0.,d,0.], [0.,0.,d]])

  turnU = lambda delta: np.round( np.array([[np.cos(delta),np.sin(delta),0.],[-np.sin(delta),np.cos(delta),0.],[0.,0.,1.]]), 10 )
  turnU_matrix_plus = turnU(delta)
  turnU_matrix_minus = turnU(-delta)
  turnU_matrix_around = turnU(np.pi)
  
  turnL = lambda delta: np.round( np.array([[np.cos(delta),0.,-np.sin(delta)],[0.,1.,0.],[np.sin(delta),0.,np.cos(delta)]]), 10 )
  turnL_matrix_plus = turnL(delta)
  turnL_matrix_minus = turnL(-delta)
  
  turnH = lambda delta: np.round( np.array([[1.,0.,0.],[0.,np.cos(delta),-np.sin(delta)],[0.,np.sin(delta),np.cos(delta)]]), 10 )
  turnH_matrix_plus = turnH(delta)
  turnH_matrix_minus = turnH(-delta)
  
  lines = []
  points = []
  lines_idx = []
  i = 0
  for c in s:
    if   c=="+":
      hlu = np.dot(hlu,turnU_matrix_plus)
    elif c=="-":
      hlu = np.dot(hlu,turnU_matrix_minus)
    elif c=="&":
      hlu = np.dot(hlu,turnL_matrix_plus)
    elif c=="^":
      hlu = np.dot(hlu,turnL_matrix_minus)
    elif c=="\\" or c=="<":
      hlu = np.dot(hlu,turnH_matrix_plus)
    elif c=="/" or c==">":
      hlu = np.dot(hlu,turnH_matrix_minus)
    elif c=="|":
      hlu = np.dot(hlu,turnU_matrix_around)
    elif draw_off.find(c)>=0:
      p = p+hlu[:,0]
    elif draw_on.find(c)>=0:
      lines.append([p,p+hlu[:,0]])
      points.append(p)
      points.append(p+hlu[:,0])
      lines_idx.append(i)
      lines_idx.append(i+1)
      i+=2
      p = p+hlu[:,0]
      
  return lines, np.array(points), np.array(lines_idx)

def export_collada(filename, points, indices):
  mesh = collada.Collada()
  vert_src = collada.source.FloatSource("lineverts-array", points, ('X','Y','Z'))
  geom = collada.geometry.Geometry(mesh, "fractal-geometry", "fractal", [vert_src])

  input_list = collada.source.InputList()
  input_list.addInput(0, 'VERTEX', "#lineverts-array")
  lineset = geom.createLineSet(indices, input_list, "materialref")
  geom.primitives.append(lineset)
  mesh.geometries.append(geom)

  geomnode = collada.scene.GeometryNode(geom)
  node = collada.scene.Node("fractal-node", children=[geomnode])
  myscene = collada.scene.Scene("fractal-scene", [node])
  mesh.scenes.append(myscene)
  mesh.scene = myscene
  mesh.write(filename)

  return mesh

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

#axiom = "A"
#productions = {
#  "A": "B-F+CFC+F-D&F^D-F+&&CFC+F+B//",
#  "B": "A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//",
#  "C": "|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//",
#  "D": "|CFB-F+B|FA&F^A&&FB-F+B|FC//"
#}
#delta = -np.pi/2.
#d = 1.

n = 2

t1 = time.time()
s = string_replacement(axiom, productions, n)
t2 = time.time()
print "time for string replacement: ", t2-t1, "s" 
lines, points, lines_idx = turtle_lines(s, delta, d, "FG")
t3 = time.time()
print "time for lines creation: ", t3-t2, "s" 
export_collada("/tmp/frac.dae", points, lines_idx)
t4 = time.time()
print "time for collada export: ", t4-t3, "s"

print "number of lines: ", len(points)
#print s

fig, ax = plt.subplots()
########### 2D
#for l in lines:
#  plt.plot(*zip(*l), color="b")
#plt.plot(*zip(*points), color="b")
#plt.margins(x=.1, y=.1)

########### 3D
ax = fig.add_subplot(111, projection='3d')
#ax.plot(points[:,0], points[:,1], points[:,2], color="b")
for l in lines:
  ax.plot( [l[0][0],l[1][0]], [l[0][1],l[1][1]], [l[0][2],l[1][2]], color='blue')
ax.set_zlabel("z")
plt.margins(.1)

plt.xlabel("x")
plt.ylabel("y")
plt.show() #block=False)