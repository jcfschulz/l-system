import numpy as np
import time
#import collada
import re
from asteval import Interpreter

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
    if not context_ignores.has_key(c):
      context = c
    i += 1
  return snew

def obtain_symbols(symbols, rule, expr, split_on="\(|,|\)"):
  if rule==None:
    return True
  rule_split = re.split(split_on,rule.replace(" ",""))  # do for all whitespaces
  expr_split = re.split(split_on,expr.replace(" ",""))  # do for all whitespaces
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

def split_on_brackets(string):
  res = []
  s = ""
  openbrackets = 0
  closebrackets = 0
  for c in s:
    s += c
    if c="(":
      res.append(s)
      s = ""

def match_rule(rule, expression, pre_context, post_context):
  global symbols

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
      #if not eval_cond_expr(cond, symbols):
      if not aeval(cond):
        return False

  sfinal = ""
  res_split = re.split("\(|,|\)",rule[4].replace(" ",""))
  if len(res_split)<2:
    return rule[4]
  print rule[4]
  for i in range(len(res_split)/2):
    sfinal += res_split[2*i]
    sfinal += "("
    sfinal += str(aeval(res_split[2*i+1]))
    sfinal += ")"

  return sfinal

aeval = Interpreter()
axiom = "A(1)"
#productions = {"A": {"params": (a), "expression": "A(a+1)B(2*a)", ""   }   }
rule = ("S(i,j,k)","S(a,b,c)",None,"i<a, j>c","F[I(  2*(i+1)   )]")
match_rule(rule, "S(5,6,7)", "S(1,10,3)", "A")