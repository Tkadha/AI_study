# 상태를 나타내는 클래스

# 2020182042 최준하
class State:
  def __init__(self, board, goal, depth=0,parent=None):
    self.board = board
    self.depth = depth
    self.goal = goal
    self.parent = parent # 부모 저장

  # i1과 i2를 교환하여서 새로운 상태를 반환한다. 
  def get_new_board(self, i1, i2, depth):
    new_board = self.board[:]
    new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
    return State(new_board, self.goal, depth, self)

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다. 
  def expand(self, depth):
    result = []
    i = self.board.index(0)	# 숫자 0(빈칸)의 위치를 찾는다. 
    if not i in [0, 3, 6] :		# LEFT 연산자 
      result.append(self.get_new_board(i, i-1, depth))
    if not i in [0, 1, 2] :		# UP 연산자 
      result.append(self.get_new_board(i, i-3, depth))
    if not i in [2, 5, 8]:		# RIGHT 연산자 
      result.append(self.get_new_board(i, i+1, depth))
    if not i in [6, 7, 8]:		# DOWN 연산자 
      result.append(self.get_new_board(i, i+3, depth))
    return result

  # 객체를 출력할 때 사용한다. 
  def __str__(self):
    return str(self.board[:3]) +"\n"+\
        str(self.board[3:6]) +"\n"+\
        str(self.board[6:]) +"\n"+\
        "------------------"

  def __eq__(self, other):			# 이것을 정의해야 in 연산자가 올바르게 계산한다.
    return self.board == other.board

  def __ne__(self, other):			# 이것을 정의해야 in 연산자가 올바르게 계산한다.
    return self.board != other.board

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

# open 리스트
open_queue = [ ]
open_queue.append(State(puzzle, goal))

closed_queue = [ ]
depth = 0

count=1

find_depth = 0
root = State(puzzle,goal)

find_way=False

while find_way != True:
    open_queue = []
    open_queue.append(State(puzzle, goal))
    closed_queue = []
    depth = 0
    while len(open_queue) != 0:
      current = open_queue.pop(0)			# OPEN 리스트의 앞에서 삭제
      print(count)
      count += 1
      print(current)
      if current.board == goal:
          print("탐색 성공")
          print_path(current)   # 최적의 경로 출력
          find_way=True
          break
      depth = current.depth + 1
      closed_queue.append(current)
      if depth > find_depth:    # 정해진 깊이만큼 탐색하면 처음부터 다시
          find_depth+=1         # 깊이 추가
          continue
      if depth > 5:
          continue
      for state in current.expand(depth):
          if (state in closed_queue) or (state in open_queue):	# 이미 거쳐간 노드이면
              continue				# 노드를 버린다.
          else:
              open_queue.append(state)		# OPEN 리스트의 끝에 추가

print("2020182042 최준하")