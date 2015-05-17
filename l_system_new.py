import numpy as np
import time
import collada
import re
from asteval import Interpreter

#import pylab as plt
#import matplotlib.lines as plt_lines
#from mpl_toolkits.mplot3d import Axes3D

deg2rad = lambda alpha: alpha*2*np.pi/360.

def obtain_symbols(symbols, rule, expr):
  if rule==None:
    return True
  if rule.find("(")<0:
    return True
  rule_symbol = rule[:rule.find("(")]
  expr_symbol = expr[:expr.find("(")]
  if expr_symbol != rule_symbol:
    return False
  rule_params = rule[rule.find("(")+1:rule.rfind(")")].split(",")
  expr_params = expr[expr.find("(")+1:expr.rfind(")")].split(",")
  if len(expr_params)!=len(rule_params):
    print "wrong number of arguments for", expr_symbol, " : ", len(expr_params), "!=", len(rule_params)
    return False
  for i in range(len(expr_params)):
    symbols[rule_params[i]] = float(expr_params[i])
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
  aeval = Interpreter()
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

def string_replacement(sstart, rules, context_ignores=()): 
  snew = ""
  context = [""]
  m = False
  
  for t in split_symbols(sstart):
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

def eval_lsystem(axiom, rules, n):
  string = axiom
  for i in range(n):
    string = string_replacement(string, rules)
  return string


axiom = "F-F-F-F"
rules  = [ (None, "F", None, None, "F-F+F+FF-F-F+F") ]

print eval_lsystem(axiom, rules, 1)