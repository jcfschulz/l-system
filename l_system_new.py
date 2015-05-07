import numpy as np
import time
import collada
import re

#import pylab as plt
#import matplotlib.lines as plt_lines
#from mpl_toolkits.mplot3d import Axes3D

deg2rad = lambda alpha: alpha*2*np.pi/360.

def string_replacement_context(sstart, productions, n, context_ignores=()): 
  s = sstart
  snew = ""
  context = ""
  i = 0
  while i<len(s):
    c = s[i]
    if productions.has_key(c):
      snew += productions[c]
    else:
      snew += c
    if !context_ignores.has_key(c):
      context = c
    i += 1
  return snew

axiom = "A(1)"
#productions = {"A": {"params": (a), "expression": "A(a+1)B(2*a)", ""   }   }
rule = ("S(i,j,k)","S(a,b,c)",None,"i<a, j>c","F[I(i+1)]")

def multi_split(a,delims,split_on=","):
  for c in delims:
    a=str.replace(a,c,split_on)
  return a.split(split_on)

def obtain_symbols(symbols, rule, expr):
  if rule==None:
    return True
  rule_split = re.split("\(|,|\)",rule.replace(" ",""))  # do for all whitespaces
  expr_split = re.split("\(|,|\)",expr.replace(" ",""))  # do for all whitespaces
  if expr_split[0]!=rule_split[0]:
    return False
  if len(expr_split)!=len(rule_split):
    print "wrong number of arguments for", expr_split[0], " : ", len(expr_split), "!=", len(rule_split) # better status message
    return False
  for i in range(1,len(expr_split)):
    if rule_split[i]=="":     # do better splitting without trailing empty string on match
      continue
    symbols[rule_split[i]] = float(expr_split[i])
  return True

def eval_cond_expr(expr, symbols):
  # parse brackets

  found_prev = False
  comparing_operators = ("<",">","!=","==")
  op = ""
  for c in comparing_operators:
    cnt = expr.count(c)
    if cnt>1 or (cnt>0 and found_prev==True):
      print "Wrong usage of operator", c, ". Maybe use brackets?"   # raise error
      return 
    elif cnt==1:
      expr_split = expr.split(c)
      op = c
      found_prev = True

  if op=="<":
    return symbols[expr_split[0]]<symbols[expr_split[1]]
  elif op==">":
    return symbols[expr_split[0]]>symbols[expr_split[1]]
  elif op=="==":
    return symbols[expr_split[0]]==symbols[expr_split[1]]
  elif op=="!=":
    return symbols[expr_split[0]]!=symbols[expr_split[1]]
  else:
    print "unknown operator", op   # raise error
    return

def eval_math(expr, symbols):
  operands = expr.split("+")
  return symbols[operands[0]]+symbols[operands[1]]

def match_rule(rule, expression, pre_context, post_context):
  global symbols

  symbols = {}
  if not obtain_symbols(symbols,rule[1],expression):
    return False
  if not obtain_symbols(symbols,rule[0],pre_context):
    return False
  if not obtain_symbols(symbols,rule[2],post_context):
    return False

  if conditions != None:
    conditions = rule[3].replace(" ","").split(",")
    for cond in conditions:
      if not eval_cond_expr(cond, symbols):
        return False

  sfinal = ""
  res_split = re.split("\(|,|\)",rule[4].replace(" ",""))
  if len(res_split)<2:
    return rule[4]
  for i in range(len(res_split)/2):
    sfinal += res_split[2*i]
    sfinal += "("
    sfinal += str(eval_math(res_split[2*i+1], symbols))
    sfinal += ")"

  return sfinal