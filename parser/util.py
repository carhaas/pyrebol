#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collections import defaultdict
import sys

ARITY_SEP = '@'
ARITY_STR = 's'
ARITY_ANY = '*'
#Alan€Brooke,€1st€Viscount€Alanbrooke
def after_nth(mrl, token, n):
  while n > 0:
    try:
      #m = re.search(r'\b%s\b' % re.escape(token), mrl)
      m = re.search(r'\b%s\b' % re.sub(r'([\.\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])', r'\\\1', token), mrl)
      #m = re.search(r'(^|[(, ])%s[(),]' % token, mrl)
      mrl = mrl[m.end()-1:]
      n = n - 1;
    except:
      print "Warning error on token %s in mrl %s" % (token,mrl)
  return mrl

def count_arguments(s):
  args = False;
  parens = 0;
  commas = 0;
  i = 0
  #while parens >= 0 and i < len(s):
  while i < len(s) and ((not args and parens == 0) or (args and parens > 0)):
    c = s[i:i+1]
    if c == '(':
      args = True
      parens += 1
    elif c == ')':
      parens -= 1
    elif parens == 1 and c == ',':
      commas += 1
    elif parens < 1 and c == ',':
      break
    i += 1
  if args:
   return commas + 1
  else:
    assert commas == 0
    return 0

def fun_to_mrl(mrl, star_top=False):
  mrl = mrl.strip()
  print mrl
  mrl = re.sub(r"' *([A-Za-z0-9_ ]+?) *'", lambda x: '%s%s%s' % (x.group(1).replace(' ', '_'), ARITY_SEP, ARITY_STR), mrl)
  mrl = re.sub(r'\s+', ' ', mrl)
  mrl_noparens = re.sub(r'[\(\)]', ' ', mrl)
  mrl_noparens = re.sub(r'\s+', ' ', mrl_noparens)
  mrl_nocommas = re.sub(r',', ' ', mrl_noparens)
  mrl_nocommas = re.sub(r'\s+', ' ', mrl_nocommas)

  mrl_labeled_tokens = []
  seen = defaultdict(lambda:0)
  for token in mrl_nocommas.split():
    seen[token] += 1
    args = count_arguments(after_nth(mrl, token, seen[token]))
    #print token, args, after_nth(mrl, token, seen[token])
    if token[-len(ARITY_SEP)-len(ARITY_STR):] == '%s%s' % (ARITY_SEP, ARITY_STR):
      mrl_labeled_tokens.append(token)
    else:
      mrl_labeled_tokens.append('%s%s%d' % (token, ARITY_SEP, args))

  if star_top:
    tok = mrl_labeled_tokens[0]
    sep = tok.rindex(ARITY_SEP)
    mrl_labeled_tokens[0] = tok[:sep] + ARITY_SEP + ARITY_ANY
  print ' '.join(mrl_labeled_tokens)
  return ' '.join(mrl_labeled_tokens)

def overpass_to_mrl(mrl, star_top=False):
  mrl = mrl.strip()
  #mrl = re.sub("([A-Za-zöäüßÖÄÜîûâêôéáíúóîûâ])'([A-Za-zöäüßÖÄÜîûâêôéáíúóîûâ])", r"\1XXXXX\2", mrl)
  mrl = re.sub(" ", r"€", mrl)
  mrl = re.sub(r"(?<=([^,\(\)]))'(?=([^,\(\)]))", r"XXXXX", mrl)#edited
  mrl = re.sub(r"' *(.+?) *'", lambda x: '%s%s%s' % (x.group(1).replace(' ', '€'), ARITY_SEP, ARITY_STR), mrl)
  #the following line needs changing somehow
  #mrl = re.sub(r"' *([A-Za-z0-9 ,_\-:öäüßÖÄÜîûâêôéáíúóîûâ'=]+?) *'", lambda x: '%s%s%s' % (x.group(1).replace(' ', '€'), ARITY_SEP, ARITY_STR), mrl)
  mrl = re.sub(r'\s+', ' ', mrl)
  #mrl = "count(area(keyval(name,Leeds@s)),node(keyval(name,How€R€U?@s)))"
  mrl_noparens = re.sub(r'[\(\)]', ' ', mrl)
  mrl_noparens = re.sub(r'\s+', ' ', mrl_noparens)
  mrl_nocommas = re.sub(r',', ' ', mrl_noparens)
  mrl_nocommas = re.sub(r'\s+', ' ', mrl_nocommas)
  #print mrl_nocommas
  mrl_labeled_tokens = []
  seen = defaultdict(lambda:0)
  for token in mrl_nocommas.split():
    #print token
    seen[token] += 1
    if token.endswith("@s"):
      mrl_labeled_tokens.append(token)
      continue
    args = count_arguments(after_nth(mrl, token, seen[token]))
    #print token, args, after_nth(mrl, token, seen[token])
    #if token[-len(ARITY_SEP)-len(ARITY_STR):] == '%s%s' % (ARITY_SEP, ARITY_STR):
    #  mrl_labeled_tokens.append(token)
    #else:
    mrl_labeled_tokens.append('%s%s%d' % (token, ARITY_SEP, args))

  if star_top:
    tok = mrl_labeled_tokens[0]
    sep = tok.rindex(ARITY_SEP)
    mrl_labeled_tokens[0] = tok[:sep] + ARITY_SEP + ARITY_ANY
  joined = ' '.join(mrl_labeled_tokens)
  joined = re.sub("XXXXX", r"'", joined)
  return joined
