from pygame import *
import time,random
class snake():
    def __init__(self):
        global map
        self.body=[[11,10],[10,10],[9,10]]#列表的每一项是坐标，第一个坐标代表头的位置
        self.direction='right'#方向4个，每个都是小写单词
        for i in self.body:
            map[i[0]][i[1]] = 1
    def turn_direction(self,direction):#转蛇头
        Di=['left','right','up','down']
        if self.direction in Di[0:2] and direction in Di[2:]:
            self.direction = direction
        if self.direction in Di[2:] and direction in Di[0:2]:
            self.direction = direction
    def move(self):#让蛇移动
        global WIDTH,HEIGHT
        #预留蛇尾的位置，为吃到食物变长做准备
        x , y = self.body[-1][0],self.body[-1][1]
        map[x][y] = 0
        for i in range(len(self.body)-1,0,-1):
            self.body[i][0] = self.body[i-1][0]
            self.body[i][1] = self.body[i-1][1]
        if self.direction == 'right':
            self.body[0][0] += 1
        elif self.direction == 'left':
            self.body[0][0] -= 1
        elif self.direction == 'up':
            self.body[0][1] -= 1
        elif self.direction == 'down':
            self.body[0][1] += 1
        #判断是否吃到食物
        if out_edge(self.body[0][0],self.body[0][1]) == True:
            return
        map[ self.body[0][0] ][ self.body[0][1] ] = 1
        if judge_eat_food() == True:
            # print('eat food')
            map[x][y] = 1
            self.body.append([x,y])
class food():
    def __init__(self):
        self.x, self.y = 0, 0
def out_edge(x,y):
    global WIDTH,HEIGHT
    if x<0 or x>=WIDTH or y<0 or y>=HEIGHT:
        return True
    return False
def draw_rect(x,y,color):
    global screen,WIDTH,HEIGHT
    rect = Rect(x*40+4,y*40+4,32,32)
    draw.rect(surface=screen,rect=rect,color=color)
def draw_snake():
    global Snake
    draw_rect(Snake.body[0][0],Snake.body[0][1],'blue')
    for i in Snake.body[1:]:
        draw_rect(i[0],i[1],'green')
def draw_food():
    global Food
    draw_rect(Food.x,Food.y,'red')
def Draw():#注意区分首字母大小写！这个和pygame的draw不一样！！！！！！！
    draw_snake()
    draw_food()
def judge_direction_key(Event):#判断按键能否改变方向，能则改变方向
    global Snake
    if Event.type != KEYDOWN:
        return False
    if Event.key == K_RIGHT or Event.key == K_d:
        Snake.turn_direction('right')
        return True
    if Event.key == K_LEFT or Event.key == K_a:
        Snake.turn_direction('left')
        return True
    if Event.key == K_UP or Event.key == K_w:
        Snake.turn_direction('up')
        return True
    if Event.key== K_DOWN or Event.key == K_s:
        Snake.turn_direction('down')
        return True
def set_food():
    global Food,map,WIDTH,HEIGHT
    while True:
        x,y = random.randint(0,WIDTH-1),random.randint(0,HEIGHT-1)
        if map[x][y] == 0:
            map[x][y] = 2
            Food.x , Food.y = x , y
            break
def judge_eat_food():#吃到食物时返回True
    global Snake,Food
    x , y = Snake.body[0][0],Snake.body[0][1]
    if Food.x == x and Food.y == y:
        map[x][y] = 1
        set_food()
        return True
    return False
def set_map():
    global map,Snake,Food
    global WIDTH,HEIGHT
    for i in range(WIDTH):
        for j in range(HEIGHT):
            map[i][j] = 0
    for i in Snake.body:
        x , y = i[0],i[1]
        map[x][y] = 1
    map[Food.x][Food.y] = 2
def set():
    #初始化设置
    global screen,Snake,interval,map,Food
    global WIDTH,HEIGHT
    WIDTH , HEIGHT = 20 , 20
    map = []
    for i in range(WIDTH):
        map.append([])
        for j in range(HEIGHT):
            map[i].append(0)
    '''
    0代表空位置
    1代表蛇身
    2代表果实
    '''
    Snake = snake()
    Food = food()
    set_food()
    init()
    size = width, height = 800,800#地图20x20,其中一个坐标占据40*40像素
    screen = display.set_mode(size)
    display.set_caption('贪吃蛇')
    interval = 0.1
def game_over():
    global Snake
    for i in Snake.body[1:]:
        if i == Snake.body[0]:
            return True
    if out_edge(Snake.body[0][0],Snake.body[0][1]) == True:
        return True
    return False
def Q(map):
    global WIDTH,HEIGHT
    for j in range(HEIGHT):
        for i in range(WIDTH):
            print('{:>2}'.format(map[i][j]),end=' ')
        print()
set()