from random import randint
import console
import time

class MSBoard:

  command_tip = '''
PyneSweeper V1.1.3

cmd:  dig  flag  mark  pop
arg:  A1 ~ max ; pop: 9 blocks
Icon:
  ░  Unrevealed
  F  Flag
  x  Wrong flag
  #  Bomb
  ?  Unknown
 Num Open block
'''
  outchar = ['# ','x ','? ','F ','░ ','  ','1 ','2 ','3 ','4 ','5 ','6 ','7 ','8 ']
  
  def __init__(self, height:int, width:int, difficulty:int):
    self.chkInit(height, width, difficulty)
    self.height = height
    self.width = width
    self.difficulty = difficulty
    self.dataBoard = [[0] * width for row in range(height)]
    self.userBoard = [[-1] * width for row in range(height)]
  
  def dataReset(self):
    self.dataBoard = [[0] * self.width for row in range(self.height)]
    self.userBoard = [[-1] * self.width for row in range(self.height)]
    
  def chkInit(self, h, w, d):
    assert (h > 1 and h < 27), 'E: Invalid height'
    assert (w > 1 and w < 27), 'E: Invalid Width'
    assert (d > 0 and h < 100), 'E: Invalid Difficulty'
    
  def startGame(self):
    print(self.command_tip)
    input('\nPress Enter to start.')
    self.generate()
    self.gameResult = self.loop()
    print('\nYou Win !') if self.gameResult else print('You Lose.')
    self.endGame()
    # add a game timer ?                            ++++++++++++++++++++++
    
  def generate(self):
    blockNum = self.height * self.width
    bombNum = int(blockNum * self.difficulty / 100) + 1
    tmp_bombPlace = [-1] * bombNum
    for i in range(bombNum):
      p = randint(0, blockNum)
      while(p in tmp_bombPlace):
        p = randint(0, blockNum)
      tmp_bombPlace[i] = p
    for i in tmp_bombPlace:
      try:
        self.dataBoard[i // self.width][i % self.width] = 1
      except :
        pass
    self.updateView()
    
  def loop(self) -> bool:
    state = 'playing'
    while(state == 'playing'):
      move = input().split(' ')
      if(len(move) > 1):
        if(move[0] == 'dig' or move[0] == 'd'):
          state = self.dig(move[1:])
          self.updateView()
        elif(move[0] == 'flag' or move[0] == 'f'):
          self.mark(move[1:], 0)
          self.updateView()
        elif(move[0] == 'mark' or move[0] == 'm'):
          self.mark(move[1:], 1)
          self.updateView()
        else:
          self.updateView()
          print('Invalid move')
    return True if state == 'win' else False
  
  def digFill(self, row, col):
    bnHere = 0
    for i in [row-1, row, row+1]:
      if(i > -1 and i < self.height):
        for j in [col-1, col, col+1]:
          if(j > -1 and j < self.width):
            if(self.dataBoard[i][j]):
              bnHere += 1
    self.userBoard[row][col] = bnHere
  
  def dig(self, place) -> str:
    rtn = 'playing'
    for arg in place:
      (row, col) = self.trans(arg)
      if(row > -1 and col > -1):
        rtn = 'win'
        if(self.dataBoard[row][col] == 0):
          self.digFill(row, col)
          while(self.digExp()):
            self.digExp()
          for row in range(self.height):
            for col in range(self.width):
              if(self.dataBoard[row][col] == 1 and self.userBoard[row][col] != -2):
                rtn = 'playing'
        else:
          rtn = 'lose'
          for row in range(self.height):
            for col in range(self.width):
              if(self.userBoard[row][col] == -2 and self.dataBoard[row][col] == 0):
                self.userBoard[row][col] = -4
              elif(self.userBoard[row][col] > -2 and self.dataBoard[row][col] == 1):
                self.userBoard[row][col] = -5
    return rtn
    
  def digExp(self) -> bool:
    rtn = False
    for row in range(self.height):
      for col in range(self.width):
        if(self.dataBoard[row][col] == 0 and self.userBoard[row][col] == -1):
          for i in [row-1, row, row+1]:
            if(i > -1 and i < self.height):
              for j in [col-1, col, col+1]:
                if(j > -1 and j < self.width):
                  if(i != row or j != col):
                    if(self.userBoard[i][j] == 0):
                      self.digFill(row, col)
                      rtn = True
    return rtn
    
  def mark(self, place, type:int):
    for arg in place:
      (row, col) = self.trans(arg)
      if(row > -1 and col > -1):
        self.userBoard[row][col] = -2 - type
    
  def trans(self, place:str) -> (int, int):
    col = -1
    row = -1
    char = ord(place[0])
    char = char if char < 91 else char - 32
    assert (64 < char < 91), 'Err'
    # 65~90 A~Z  97~ a~z  ASCII
    col = char - 65
    if(len(place) == 2):
      row = int(place[1]) - 1
    elif(len(place) == 3):
      row = int(place[1]) * 10 + int(place[2]) - 1
    if(row >= 0 and row < self.height):
      if(col >= 0 and row < self.width):
        if(self.userBoard[row][col] < 0):
          return (row, col)
    return (-1, -1)
  
  def endGame(self):
    #self.gameResult
    input('Press Enter to restart')
    console.clear()
    self.dataReset()
    self.startGame()
  
  def updateView(self):
    output = '    '
    output += 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
    output = output[0 : 2 * len(self.dataBoard[0]) + 3]
    output += '\n\n'
    for row in range(self.height):
      N = ''
      if(row < 9):
        N = '0' + str(row + 1)
      else:
        N = str(row + 1)
      output += (N + '  ')
      for col in range(self.width):
        d = self.userBoard[row][col]
        if(-6 < d < 9):
          output += self.outchar[d + 5]
        else:
          output += '§ '
      output += '\n'
    console.clear()
    print(output)

  # Difficulty
  # d / 100 of Blocks are bombs

  # dataBoard
  # 0 None
  # 1 Bomb
  
  # userBoard
  # -1 Untouched
  # 0~8 Open, Bomb num.
  # -2 flag
  # -3 mark unknown
  # -4 Wrong flag (result)
  # -5 Bomb (result)

def gameLauncher():
  board = MSBoard(int(input('Board height: ')), int(input('Board Width: ')), int(input('Difficulty: ')))
  board.startGame()

if(__name__ == '__main__'):
  gameLauncher()

''' V1.1.3
增加Flag函数中判定胜利
指令 d b1 b2 … 将dig所有传入的arg
'''