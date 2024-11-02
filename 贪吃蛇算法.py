from GreedySnake import *
def copy_map():
    global map,WIDTH,HEIGHT
    MAP = []
    for i in range(WIDTH):
        MAP.append([])
        for j in range(HEIGHT):
            MAP[i].append(map[i][j])
    return MAP
def search_priority(x,y):#坐标越靠边界，返回的值越小
    global WIDTH,HEIGHT
    return min(x,y,WIDTH-x-1,HEIGHT-y-1)
def game_start():
    global Snake
    #开始游戏
    while True:
        screen.fill('black')
        algorithm()
        for Event in event.get():
            #玩家是否主动退出
            if Event.type == QUIT:
                return
            if judge_direction_key(Event) == True:
                break
        if game_over() == True:
            print('游戏结束，蛇的长度是{}'.format(len(Snake.body)))
            return
        Snake.move()
        Draw()
        display.update()
        time.sleep(interval)
        if len(Snake.body) == 400:
            print('恭喜你，你的贪吃蛇程序终于吃满全屏了')
            print('以此祝贺该程序的作者：杨熠！！！！！！')
            input('按任意键结束')
            return
def search(x,y,n):
    #判断当前坐标是否能为第n步,如果找到了食物，返回True
    #用于广度优先搜索
    global map,WIDTH,HEIGHT
    if out_edge(x,y) == True:
        return False
    if map[x][y] != 0 and map[x][y] != -2:
        return False
    for i,j in [[-1,0],[1,0],[0,1],[0,-1]]:
        x1,y1 = x+i , y+j
        if out_edge(x1,y1) == True:
            continue
        if map[x1][y1] == n-1:
            if map[x][y] == -2:
                map[x][y] = n
                return True
            map[x][y] = n
            return False
    return False
def forth():
    global WIDTH,HEIGHT
    step = 2#步骤一定要从2开始
    while True:
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if search(i,j,step) == True:
                    return
        step += 1
def back(x,y):#返回从蛇头到指定坐标的方向
    global map,Food,Snake
    global WIDTH,HEIGHT
    #先确定下一步要走哪个地方
    step = map[x][y]
    while map[x][y] != 2:
        for i,j in [[-1,0],[1,0],[0,-1],[0,1]]:
            x1 ,y1 = x+i , y+j
            if out_edge(x1,y1) == True:
                continue
            if map[x1][y1] == step-1:
                x,y = x1 , y1
                break
        step -= 1
    #确定好新的方向
    x0,y0 = Snake.body[0][0] , Snake.body[0][1]
    for i in [[1,0,'right'],[-1,0,'left'],[0,-1,'up'],[0,1,'down']]:
        x1,y1 = x0+i[0] , y0+i[1]
        if out_edge(x1,y1) == True:
            continue
        if x==x1 and y==y1:
            return i[2]
    return Snake.direction
def find(x,y):#深度优先搜索
    global BOOL,map
    global WIDTH,HEIGHT
    if out_edge(x,y) == True:
        return
    if map[x][y] == -2:
        BOOL = True
        return
    if map[x][y] == -1 or map[x][y] == 1:
        return
    map[x][y] = 1
    for i in [[-1,0],[1,0],[0,-1],[0,1]]:
        find( x+i[0] , y+i[1] )
def if_find_food():#判断是否能找到食物，能则返回True
    global map,Snake,BOOL
    global WIDTH,HEIGHT
    #修改好地图
    #将身体部分赋值为-1,果实赋值为-2，步骤为整数
    for i in Snake.body:
        map[i[0]][i[1]] = -1
    x , y = Snake.body[0][0] , Snake.body[0][1]
    map[x][y] = 1   #蛇头为第一步
    map[Food.x][Food.y] = -2
    #准备深度优先搜索
    BOOL = False
    x,y = Snake.body[0][0] , Snake.body[0][1]
    map[x][y] = 0
    find(x,y)
    #将map的数据修改回来
    set_map()
    return BOOL
def food_way_direction():
    global Food,map,Snake
    # 将身体部分赋值为-1,果实赋值为-2，步骤为整数
    for i in Snake.body:
        map[i[0]][i[1]] = -1
    x, y = Snake.body[0][0], Snake.body[0][1]
    map[x][y] = 1  # 蛇头为第一步
    map[Food.x][Food.y] = -2
    forth()#开始广度优先搜索
    direction = back(Food.x,Food.y)#回溯，查找最佳方向
    set_map()#把map变回原来的样子（十分重要！！！！）
    return direction
def find_tail(x,y,step):
    global map,BOOL
    if BOOL == True:
        return
    if map[x][y] == -2:
        BOOL = True
        map[x][y] = step
        return
    if map[x][y] != 0:
        return
    map[x][y] = step
    for i in [[-1,0],[1,0],[0,-1],[0,1]]:
        x1,y1 = x+i[0] , y+i[1]
        if out_edge(x1,y1) == True:
            continue
        find_tail(x1,y1,step+1)
def if_find_tail():
    global Snake, map,Food
    global WIDTH, HEIGHT
    # 尾巴设置为-2，身体设置为-1，头设置为0
    map[Food.x][Food.y] = 0
    map[Snake.body[0][0]][Snake.body[0][1]] = 0
    for i in Snake.body[1:-1]:
        map[i[0]][i[1]] = -1
    map[Snake.body[-1][0]][Snake.body[-1][1]] = -2
    # 开始深度优先搜索（找尾巴）
    global BOOL
    BOOL = False
    find_tail(Snake.body[0][0], Snake.body[0][1], 1)
    set_map()  # 将地图设置会原样
    return BOOL
def tail_way_direction():#追着尾巴走
    global Snake,map
    global WIDTH,HEIGHT
    #尾巴设置为-2，身体设置为-1，头设置为0
    map[ Snake.body[0][0] ][ Snake.body[0][1] ] = 0
    for i in Snake.body[1:-1]:
        map[i[0]][i[1]] = -1
    map[ Snake.body[-1][0] ][ Snake.body[-1][1] ] = -2
    #开始深度优先搜索（找尾巴）
    global BOOL
    BOOL = False
    find_tail( Snake.body[0][0] , Snake.body[0][1] , 1)
    #回溯查找最佳方向
    direction = Snake.direction
    if BOOL == True:
        direction = back(Snake.body[-1][0],Snake.body[-1][1])
    set_map()
    return direction
Num = 1
def simulate():
    global Snake,screen,Food
    BOOL = if_find_food()
    if BOOL == False:
        return False
    length = len(Snake.body)
    '''备份'''
    Snake_ = snake()
    Snake_.body = []
    for i in range(length):
        Snake_.body.append([0,0])
        Snake_.body[i][0],Snake_.body[i][1] = Snake.body[i][0],Snake.body[i][1]
    Snake_.direction = Snake.direction
    Food_ = food()
    Food_.x,Food_.y = Food.x,Food.y
    '''模拟'''
    BOOL2 = True
    while length==len(Snake.body):
        if if_find_food() == False:
            BOOL = False
            BOOL2 = False
            break
        Snake.turn_direction(food_way_direction())
        Snake.move()
        # if game_over() == True:
        #     return
        # screen.fill('black')
        # Draw()
        # display.update()
        # time.sleep(interval)
    global Num
    # print(Num)
    Num += 1
    if BOOL2:
        BOOL = if_find_tail()
    '''回归原样'''
    Snake.body = []
    for i in range(length):
        Snake.body.append([0,0])
        Snake.body[i][0],Snake.body[i][1] = Snake_.body[i][0],Snake_.body[i][1]
    Snake.direction = Snake_.direction
    Food.x,Food.y = Food_.x,Food_.y
    set_map()
    return BOOL
def algorithm():
    global map,Snake,Food
    global interval
    '''
    地图大小为20x20
    0代表空
    1代表蛇的身体
    2代表果实
    '''
    direction = Snake.direction
    if simulate() == True:
        '''如果能吃到食物且吃到食物后可以找到尾巴'''
        direction = food_way_direction()
    else:
        direction = tail_way_direction()
    Snake.turn_direction(direction)
    set_map()
interval = 0.05
game_start()