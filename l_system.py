import numpy as np
import time
import collada

import pylab as plt
import matplotlib.lines as plt_lines
from mpl_toolkits.mplot3d import Axes3D

deg2rad = lambda alpha: alpha*2*np.pi/360.

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

def turtle_lines(s, delta, d, draw_on="F", draw_off="f", round_dec=10):
  p = np.array([0.,0.,0.])
  hlu = np.array([[d,0.,0.], [0.,d,0.], [0.,0.,d]])

  turnU = lambda delta: np.round( np.array([[np.cos(delta),np.sin(delta),0.],[-np.sin(delta),np.cos(delta),0.],[0.,0.,1.]]), round_dec )
  turnU_matrix_plus = turnU(delta)
  turnU_matrix_minus = turnU(-delta)
  turnU_matrix_around = turnU(np.pi)
  
  turnL = lambda delta: np.round( np.array([[np.cos(delta),0.,-np.sin(delta)],[0.,1.,0.],[np.sin(delta),0.,np.cos(delta)]]), round_dec )
  turnL_matrix_plus = turnL(delta)
  turnL_matrix_minus = turnL(-delta)
  
  turnH = lambda delta: np.round( np.array([[1.,0.,0.],[0.,np.cos(delta),-np.sin(delta)],[0.,np.sin(delta),np.cos(delta)]]), round_dec )
  turnH_matrix_plus = turnH(delta)
  turnH_matrix_minus = turnH(-delta)
  
  lines = []
  points = []
  lines_idx = []

  stack = []
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
    elif c=="[":
      stack.append([p,hlu])
    elif c=="]":
      p,hlu = stack.pop()
    elif draw_off.find(c)>=0:
      p = p+hlu[:,0]
    elif draw_on.find(c)>=0:
      if c=="f":
        fac = 0.3
      else: 
        fac=1.
      lines.append([p,p+fac*hlu[:,0]])
      points.append(p)
      points.append(p+fac*hlu[:,0])
      lines_idx.append(i)
      lines_idx.append(i+1)
      i+=2
      p = p+fac*hlu[:,0]
      
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

#axiom = "F-F-F-F"
#productions = {"F": "F-F+F+FF-F-F+F"}
#delta = np.pi/2.

#axiom = "F"
#productions = {"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"}
#delta = np.pi/3.

#axiom = "-F"
#productions = {"F": "F+F-F-F+F"}
#delta = np.pi/2.

#axiom = "F-F-F-F"
#productions = {"F": "F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}
#delta = np.pi/2.

#axiom = "F-F-F-F"
#productions = {"F": "FF-F--F-F"}
#delta = np.pi/2.

#axiom = "F-F-F-F"
#productions = {"F": "F-FF--F-F"}
#delta = np.pi/2.

#axiom = "G"
#productions = {"F": "G+F+G", "G": "F-G-F"}
#delta = np.pi/3.

#axiom = "F"
#productions = {"F": "F+G+", "G": "-F-G"}
#delta = np.pi/2.

#axiom = "---F"
#productions = {"F": "F++F----F++F"}
#delta = np.pi/6.

#axiom = "F++F++F"
#productions = {"F": "F-F++F-F"}
#delta = np.pi/3.

#axiom = "F-F-F-F"
#productions = {"F": "FF-F-F-F-FF"}
#delta = np.pi/2.

#axiom = "F+F+F+F"
#productions = {"F": "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", "f": "ffffff"}
#delta = np.pi/2.

#axiom = "A"
#productions = {
#  "A": "B-F+CFC+F-D&F^D-F+&&CFC+F+B//",
#  "B": "A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//",
#  "C": "|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//",
#  "D": "|CFB-F+B|FA&F^A&&FB-F+B|FC//"
#}
#delta = -np.pi/2.

#axiom = "F"
#productions = {"F": "F[+F]F[-F]F"}
#delta = deg2rad(25.7)

#axiom = "F"
#productions = {"F": "F[+F]F[-F][F]"}
#delta = deg2rad(20.)

#axiom = "F"
#productions = {"F": "FF-[-F+F+F]+[+F-F-F]"}
#delta = deg2rad(22.5)

#axiom = "X"
#productions = {"X": "F[+X]F[-X]+X", "F": "FF"}
#delta = deg2rad(20.)

#axiom = "X"
#productions = {"X": "F[+X][-X]FX", "F": "FF"}
#delta = deg2rad(25.7)

#axiom = "X"
#productions = {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"}
#delta = deg2rad(22.5)

axiom = "A"
productions = {"A": "[&FL!A]/////'[&FL!A]///////'[&FL!A]", "F": "S/////F", "S": "FL", "L": "['''^^{-f+f+f-|-f+f+f}]" }
delta = deg2rad(22.5)

if delta>np.pi:
  print "Warning: delta too high?"

n = 5
d = 1.
plot3D = True #False

t1 = time.time()
s = string_replacement(axiom, productions, n)
t2 = time.time()
print "time for string replacement: ", t2-t1, "s" 
lines, points, lines_idx = turtle_lines(s, delta, d, "FGf", "")
t3 = time.time()
print "time for lines creation: ", t3-t2, "s" 
export_collada("/tmp/frac.dae", points, lines_idx)
t4 = time.time()
print "time for collada export: ", t4-t3, "s"

print "number of lines: ", len(points)
#print s

fig, ax = plt.subplots()
if plot3D==False:
############# 2D
  #plt.plot(*zip(*points), color="b")
  for l in lines:
    plt.plot([l[0][1],l[1][1]], [l[0][0],l[1][0]], color="b")
  plt.margins(x=.1, y=.1)
  plt.xlabel("x")
else:
############# 3D
  ax = fig.add_subplot(111, projection='3d')
  #ax.plot(points[:,2], points[:,1], points[:,1], color="b")
  plt.plot([0.], [0.], [0.], "o", color="r")
  for l in lines:
    ax.plot( [l[0][2],l[1][2]], [l[0][1],l[1][1]], [l[0][0],l[1][0]], color='blue')
  ax.set_zlabel("x")
  plt.margins(.1)
  plt.xlabel("z")
plt.ylabel("y")
plt.show() #block=False)