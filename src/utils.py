import math
import operator

def dist(p1, p2):
  return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def midpoint(p1, p2):
  return [int((p1[0]+p2[0])/2), (p1[1]+p2[1])/2]

def normalize(vec):
  vec_len = math.sqrt(vec[0]**2 + vec[1]**2)
  norm_vec = map(operator.div, vec, [vec_len, vec_len])
  return norm_vec