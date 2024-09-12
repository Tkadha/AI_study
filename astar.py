import queue

# bug: 무한루프에 빠진다. 어딘지 찾아야함 중복검사가 실패 할 수 있음

# 상태를 나타내는 클래스, f(n) 값을 저장한다.
class State:
  def __init__(self, board, goal, depth=0,parent=None):
    self.board = board			# 현재의 보드 상태
    self.depth = depth			# 깊이
    self.goal = goal			# 목표 상태
    self.parent = parent

  # i1과 i2를 교환하여서 새로운 상태를 반환한다.
  def get_new_board(self, i1, i2, depth):
    new_board = self.board[:]
    new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
    return State(new_board, self.goal, depth, self)

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다.
  def expand(self, moves):
    result = []
    i = self.board.index(0)		# 숫자 0(빈칸)의 위치를 찾는다.
    if not i in [0, 3, 6] :		# LEFT 연산자
      result.append(self.get_new_board(i, i-1, moves))
    if not i in [0, 1, 2] :		# UP 연산자
      result.append(self.get_new_board(i, i-3, moves))
    if not i in [2, 5, 8]:		# RIGHT 연산자
      result.append(self.get_new_board(i, i+1, moves))
    if not i in [6, 7, 8]:		# DOWN 연산자
      result.append(self.get_new_board(i, i+3, moves))
    return result

  # f(n)을 계산하여 반환한다.
  def f(self):
    return self.h2()+self.g()


  # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다.
  # 현재 제 위치에 있지 않은 타일의 개수를 계산하여 반환한다.
  def h(self):  # h1
    score = 0
    for i in range(9):
            if self.board[i]!=0 and self.board[i] != self.goal[i]:
                score += 1
    return score

  def h2(self): # h2
    score = 0
    for i in range(9):
      if self.board[i] != 0:
        index = self.goal.index(self.board[i])
        score += abs(i-index)//3 + abs(i-index) % 3
    return score



  # 시작 노드로부터의 깊이를 반환한다.
  def g(self):
    return self.depth

  def __eq__(self, other):
    return self.board == other.board

  def __ne__(self, other):
    return self.board != other.board

  # 상태와 상태를 비교하기 위하여 less than 연산자를 정의한다.
  def __lt__(self, other):
    return self.f() < other.f()

  def __gt__(self, other):
    return self.f() > other.f()

  # 객체를 출력할 때 사용한다.
  def __str__(self):
    return f"f(n)={self.f()} h(n)={self.h()} g(n)={self.g()}\n"+\
    str(self.board[:3]) +"\n"+\
    str(self.board[3:6]) +"\n"+\
    str(self.board[6:]) +"\n"

def print_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
    res_count = 1
    for m in reversed(path):    # 뒤집어야 시작점 부터 순서대로 출력
        print(res_count)
        print(m)
        res_count+=1
# 초기 상태
puzzle = [2, 8, 3,
          1, 6, 4,
          7, 0, 5]
# 목표 상태
goal = [1, 2, 3,
        8, 0, 4,
        7, 6, 5]

# open 리스트는 우선순위 큐로 생성한다. 
open_queue = queue.PriorityQueue()
open_queue.put(State(puzzle, goal))

closed_queue = [ ]
depth = 0
count = 0

while not open_queue.empty():
  current = open_queue.get()
  count += 1
  print(count)
  print(current)
  if current.board == goal:
      print("탐색 성공")
      print_path(current)
      break
  depth = current.depth+1
  for state in current.expand(depth):
    if state not in closed_queue and state not in open_queue.queue :
      open_queue.put(state)
  closed_queue.append(current)
else:
  print ('탐색 실패')
