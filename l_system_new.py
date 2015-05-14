import numpy as np
import time
import collada
import re
from asteval import Interpreter

#import pylab as plt
#import matplotlib.lines as plt_lines
#from mpl_toolkits.mplot3d import Axes3D

deg2rad = lambda alpha: alpha*2*np.pi/360.

def obtain_symbols(symbols, rule, expr, split_on="\(|,|\)"):
  if rule==None:
    return True
  rule_split = re.split(split_on,rule.replace(" ",""))  # do for all whitespaces
  expr_split = re.split(split_on,expr.replace(" ",""))  # do for all whitespaces
  if expr_split[0]!=rule_split[0]:
    return False
  if len(expr_split)!=len(rule_split):
    print "wrong number of arguments for", expr_split[0], " : ", len(expr_split), "!=", len(rule_split)
    return False
  for i in range(1,len(expr_split)):
    if rule_split[i]=="":     # do better splitting without trailing empty string on match
      continue
    symbols[rule_split[i]] = float(expr_split[i])
  return True

def split_symbols(string, split_mode="single"):
  i = 0
  s = ""
  res = []
  while i<len(string):
    if split_mode=="single" and string[i]==" ":
      i += 1
      continue
    s += string[i]
    if i+1<len(string):
			if string[i+1]=="(":
				brackets = 1
				s += string[i+1]
				i += 2
				while brackets>0:
					s += string[i]
					if string[i]=="(":
						brackets += 1
					elif string[i]==")":
						brackets -= 1
					i += 1
				res.append(s)
				s = ""
				continue
			elif string[i]==" " and split_mode=="space":
			  if len(s.strip())>0:
			    res.append(s.strip())
			  s = ""
			elif split_mode=="single" and len(s)>=1:
				res.append(s)
				s = ""
    i += 1
  if len(s.strip())>0:
    res.append(s.strip())
  return res
      

def match_rule(rule, expression, pre_context, post_context):
  symbols = {}
  if not obtain_symbols(symbols,rule[1],expression):
    return False
  if not obtain_symbols(symbols,rule[0],pre_context):
    return False
  if not obtain_symbols(symbols,rule[2],post_context):
    return False

  aeval.symtable = symbols

  if rule[3] != None:
    conditions = rule[3].replace(" ","").split(",")
    for cond in conditions:
      if not aeval(cond):
        return False

  sfinal = ""
  res_split = split_symbols(rule[4])
  for r in res_split:
    if r.find("(")>=0:
      sfinal += r[:r.find("(")+1]
      temp = aeval(r[r.find("(")+1:-1])
      if type(temp)==tuple:
        sfinal += str(temp[0])
        for t in temp[1:]:
          sfinal += ","
          sfinal += str(t)
      else:
        sfinal += str(temp)
      sfinal += ")"
    else:
      sfinal += r
  return sfinal

def string_replacement_context(sstart, rules, n, context_ignores=()): 
  snew = ""
  context = [""]
  m = False
  
  print sstart
  for t in split_symbols(sstart):
    print t, context[-1]
    if t=="[":
      context.append(context[-1])
      snew += "["
      continue
    elif t=="]":
      context.pop()
      snew += "]"
      continue
    for r in rules:
      m = match_rule(r, t, context[-1], None)
      if not m==False:
        snew += m
        break
    if m==False:
      snew += t

    if not (t[:t.find("(")] in context_ignores):
      context[-1] = t

  return snew

aeval = Interpreter()
axiom = "A(1,2)[BC]D"
rule = ("S(i,j,k)","S(a,b,c)",None,"i<a,j>c","F[I(i)]")

rules = [  (None,"A(i,j)",None,"i<10", "A(i+2,2*j)B"), (None,"B",None,None,"A(1,1)") ]

print match_rule(rule, "S(5,6,7)", "S(1,10,3)", "A")