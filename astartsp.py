import queue
import random
import copy

# 상태를 나타내는 클래스, f(n) 값을 저장한다. 
class State:
  def __init__(self, cities, goal, depth=0):
    self.list = cities			# 현재의 보드 상태
    self.depth = depth			# 깊이
    self.goal = goal			# 목표 상태

  # i1과 i2를 교환하여서 새로운 상태를 반환한다. 
  def get_new_board(self, i1, i2, depth):
    new_board = self.board[:]
    new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
    return State(new_board, self.goal, depth)

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다. 
  def expand(self, moves):
    result = []
    for x in range(6):
      if not x in self.list:
        list2 = copy.deepcopy(self.list)
        list2.append(x)
        result.append(State(list2,self.goal,moves))
    return result

  # f(n)을 계산하여 반환한다. 
  def f(self):
    return self.h()+self.g()

  # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다. 
  # 현재 제 위치에 있지 않은 타일의 개수를 계산하여 반환한다. 
  def h(self):
    score = 0
    hcities = copy.deepcopy(self.list)
    li = 6 -len(hcities)
    for i in range(li):
      edge = 99999
      next = 99999
      for j in range(6):
        if j != hcities[-1] and j not in hcities:
          if dist[hcities[-1]][j] < edge:
            edge = dist[hcities[-1]][j]
            next = j
      if next != 99999:
        score = score + dist[hcities[-1]][next]
        hcities.append(next)
    if len(hcities) == 6:
      score = score + dist[hcities[-1]][hcities[0]]
    return score

  # 시작 노드로부터의 깊이를 반환한다. 
  def g(self):
    score = 0
    for i in range(len(self.list)-1):
      score = score + dist[self.list[i]][self.list[i+1]]
    return score

  def __eq__(self, other):
    return sorted(self.list) == sorted(other.list)

  def __ne__(self, other):
    return sorted(self.list) != sorted(other.list)

  # 상태와 상태를 비교하기 위하여 less than 연산자를 정의한다. 
  def __lt__(self, other):
    return self.f() < other.f()

  def __gt__(self, other):
    return self.f() > other.f()

  # 객체를 출력할 때 사용한다. 
  def __str__(self):
    return f"f(n)={self.f()} h(n)={self.h()} g(n)={self.g()}\n"+\
    str(self.list[:]) + "\n"

# 도시간의 거리 행렬
dist = [[0,5,2,6,4,5],
        [5,0,7,1,3,6],
        [2,7,0,6,3,3],
        [6,1,6,0,2,4],
        [4,3,3,2,0,5],
        [5,6,3,4,5,0]]
goal=[0,1,2,3,4,5]
cities=[]
cities.append(random.randint(0,5))

# open 리스트는 우선순위 큐로 생성한다. 
open_queue = queue.PriorityQueue()
open_queue.put(State(cities, goal))

closed_queue = [ ]
depth = 0
count = 0

while not open_queue.empty():
  current = open_queue.get()
  count += 1
  print("[단계" + str(count)+"]")
  print("current.cities: " + str(current.list))
  print("goal: " + str(goal))
  if sorted(current.list) == sorted(goal):
      print("탐색 성공")
      break
  depth = current.depth+1
  for state in current.expand(depth):
    if state not in closed_queue and state not in open_queue.queue :
      open_queue.put(state)
  closed_queue.append(current)
else:
  print ('탐색 실패')
