import queue

# 상태를 나타내는 클래스, f(n) 값을 저장한다.
class State:
  def __init__(self, board, n, depth=0):
    self.board = board			# 현재의 보드 상태
    self.depth = depth			# 깊이
    self.n = n			        # queen 갯수

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다.
  def expand(self, moves):
    result = []
    row = sum([1 if 'Q' in r else 0 for r in self.board]) # 현재 퀸이 놓여진 행
    if row < self.n: # 퀸을 전부 다 놓지 않았다면
      for col in range(self.n):
        if self.is_safe(row, col): # 배치 가능한 위치인가
          new_board = [r[:] for r in self.board]  # 보드 복사
          new_board[row][col]='Q'
          result.append(State(new_board,self.n,moves))
    return result
  def is_safe(self, row, col):
    # 열에 퀸이 있는지 확인
    for i in range(row):
      if self.board[i][col] == 'Q':
        return False
    # 왼쪽 대각선 확인
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
      if self.board[i][j] == 'Q':
        return False
    # 오른쪽 대각선 확인
    for i, j in zip(range(row, -1, -1), range(col, self.n)):
      if self.board[i][j] == 'Q':
        return False
    return True

  # f(n)을 계산하여 반환한다.
  def f(self):
    return self.h()+self.g()

  # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다.
  def h(self):
    conflicts = 0 # 충돌 횟수
    row = sum([1 if 'Q' in r else 0 for r in self.board])
    for i in range(row):
            for j in range(i+1,row):
              if self.board[i].index('Q') == self.board[j].index('Q') or \
                      abs(i - j) == abs(self.board[i].index('Q') - self.board[j].index('Q')):
                conflicts+=1
    return conflicts

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
    print_str = f"f(n)={self.f()} h(n)={self.h()} g(n)={self.g()}\n"
    for l in self.board:
      print_str+=str(l)
      print_str+="\n"
    return print_str


n = int(input("n: "))

puzzle = [[" " for _ in range(n)]for _ in range(n)]

# open 리스트는 우선순위 큐로 생성한다.
open_queue = queue.PriorityQueue()
open_queue.put(State(puzzle, n))

closed_queue = [ ]
depth = 0
count = 0

while not open_queue.empty():
  current = open_queue.get()
  count += 1
  print(count)
  print(current)
  if sum([1 if 'Q' in r else 0 for r in current.board]) == n:
      print("탐색 성공")
      break
  depth = current.depth+1
  for state in current.expand(depth):
    if state not in closed_queue and state not in open_queue.queue :
      open_queue.put(state)
  closed_queue.append(current)
else:
  print ('탐색 실패')
