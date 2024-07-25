# grade 11 comp sci

import pygame
import random 
import time

pygame.init()
SIZE = (600,600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Pytris!')

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (100,100,100)
PINK = (255,105,180)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
AQUA = (0,255,255)
LIGHTGRAY = (150,150,150)
DARKGRAY = (75,75,75)
DARKERGRAY = (50,50,50)
WHITE = (255,255,255)
DARKGREEN = (0,100,0)
DARKRED = (100,0,0)

highscore = 0
screen.fill(BLACK)
myfont = pygame.font.SysFont(None,30)
homescreen1 = pygame.image.load("s1.png")
homescreen2 = pygame.image.load("s2.png")
instruction = pygame.image.load("ins.png")
lore = pygame.image.load("lore.png")

#pieces 0-t 1-J 2-L 3-z 4-s 5-o 6-i
#each rotated position of the pieces is stored in the pieces lists
pieces = [[[BLACK,PINK,BLACK],[PINK,PINK,PINK]],
          [[BLUE,BLACK,BLACK],[BLUE,BLUE,BLUE]],
          [[BLACK,BLACK,ORANGE],[ORANGE,ORANGE,ORANGE]],
          [[RED,RED,BLACK],[BLACK,RED,RED]],
          [[BLACK,GREEN,GREEN],[GREEN,GREEN,BLACK]],
          [[YELLOW,YELLOW],[YELLOW,YELLOW]],
          [[AQUA,AQUA,AQUA,AQUA]]
          ]

pieces1 = [[[PINK,BLACK],[PINK,PINK],[PINK,BLACK]],
           [[BLUE,BLUE,BLACK],[BLUE,BLACK,BLACK],[BLUE,BLACK,BLACK]],
           [[ORANGE,BLACK,BLACK],[ORANGE,BLACK,BLACK],[ORANGE,ORANGE,BLACK]],
           [[BLACK,RED],[RED,RED],[RED,BLACK]],
           [[GREEN,BLACK],[GREEN,GREEN],[BLACK,GREEN]],
           [[YELLOW,YELLOW],[YELLOW,YELLOW]],
           [[AQUA],[AQUA],[AQUA],[AQUA]]
]

pieces2 = [[[PINK,PINK,PINK],[BLACK,PINK,BLACK]],
           [[BLUE,BLUE,BLUE],[BLACK,BLACK,BLUE]],
           [[ORANGE,ORANGE,ORANGE],[ORANGE,BLACK,BLACK]],                      
           [[RED,RED,BLACK],[BLACK,RED,RED]],
           [[BLACK,GREEN,GREEN],[GREEN,GREEN,BLACK]],
           [[YELLOW,YELLOW],[YELLOW,YELLOW]],
           [[AQUA,AQUA,AQUA,AQUA]]
]

pieces3 = [[[BLACK,PINK],[PINK,PINK],[BLACK,PINK]],
           [[BLACK,BLUE],[BLACK,BLUE],[BLUE,BLUE]],
           [[ORANGE,ORANGE],[BLACK,ORANGE],[BLACK,ORANGE]],
           [[BLACK,RED],[RED,RED],[RED,BLACK]],
           [[GREEN,BLACK],[GREEN,GREEN],[BLACK,GREEN]],
           [[YELLOW,YELLOW],[YELLOW,YELLOW]],
           [[AQUA],[AQUA],[AQUA],[AQUA]]
]

#tetris grid
tetris_grid = []
for col in range(20):
    tetris_grid += [[BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK]]
garbage_grid = []
for col in range(20):
    garbage_grid += [[0,0,0,0,0,0,0,0,0,0]]

def resetgrid():
    global tetris_grid, garbage_grid, savepiece, score
    score = 0
    savepiece = 7
    tetris_grid = []
    for col in range(20):
        tetris_grid += [[BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK]]
    garbage_grid = []
    for col in range(20):
        garbage_grid += [[0,0,0,0,0,0,0,0,0,0]]

def writetext(text,x,y):
    word = myfont.render(text, 1, WHITE)	
    screen.blit(word, (x,y))	

#this clears everything on the tetris grid, then adds the garbage layer on. 
def cleargrid():
    global tetris_grid
    for col in range(20):
        for row in range(10):
            if tetris_grid[col][row] != BLACK or GRAY:
                tetris_grid[col][row] = BLACK
            if garbage_grid[col][row] == 1:
                tetris_grid[col][row] = GRAY

#draw grid
def drawgrid():
    block_size = 25
    board_position = (150,50)
    for col in range(20):
        for row in range(10): #this is very very cool because it is customizable --> you can make the grid smaller or larger by changing the general variable
            pygame.draw.rect(screen,tetris_grid[col][row],(board_position[0]+row*block_size,board_position[1]+col*block_size,block_size,block_size))
            pygame.draw.rect(screen,DARKGRAY,(board_position[0]+row*block_size,board_position[1]+col*block_size,block_size,block_size),1)

#this function draws the pieces onto the actual tetris board
def drawpiece(shapenum,x,y,piecepos):
    if piecepos == 0:
        piece = pieces[shapenum]
    elif piecepos == 1:
        piece = pieces1[shapenum]
    elif piecepos == 2:
        piece = pieces2[shapenum]
    elif piecepos == 3:
        piece = pieces3[shapenum]
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if i < len(tetris_grid) and j < len(tetris_grid[i]) and piece[i][j] != BLACK: #restrictions, if black wont draw, len so it doesnt crash
                tetris_grid[y+i][x+j] = piece[i][j]

#this creates the very cool tetris bag
def generatebag():  
    numbers = [0,1,2,3,4,5,6]
    random.shuffle(numbers)
    return numbers

#this function updates the garbage.
def updategarbage(currentpiece,x,y):
    global garbage_grid
    lineclearcount = 0 
    for i in range(len(currentpiece)):
        for j in range(len(currentpiece[i])):
            if currentpiece[i][j] != BLACK and GRAY: #makes sure doesnt add garbage to empty spaces
                    garbage_grid[y + i][x + j] = 1
    for i in garbage_grid:
        if i.count(1) == 10:
            lineclearcount += 1
            garbage_grid.remove(i) #line clear
            garbage_grid.insert(0,[0,0,0,0,0,0,0,0,0,0]) #pushing all pieces to bottom, adding fresh row on top
    return lineclearcount

def checkcollision(x, y, shape):
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j] != BLACK: #black = no collision
                #colision at x = 0 or 10, y = 20
                if x + j < 0 or x + j >= 10 or y + i >= 20:
                    return True
                #colision with garbage
                if tetris_grid[y+i][x+j] == GRAY: #checks if the hypothetical grids the will be occupied by the tetris piece is equal to Gray
                    return 7
    return False 

#this function draws the queue of the pieces --> up to 5 pieces 
def drawqueue(bag):
    queuegrid = []
    for col in range(16): #resets the grid
        queuegrid += [[BLACK,BLACK,BLACK,BLACK]]
    for x in range(5):
        piecenum = bag[x+1] #the next piece, not the current piece
        piece = pieces[piecenum]
        for i in range(len(piece)): 
            for j in range(len(piece[i])): #this mirors the piece from the pieces list onto the queue grid
                if i < len(queuegrid[i]) and j < len(queuegrid[i]) and piece[i][j] != BLACK: #prevents BLACK spaces from printing, restrictions in case crash
                    queuegrid[3*x+i][0+j] = piece[i][j] #sets spaces between the pieces
    block_size = 22
    board_position = (425,50)
    for col in range(16):
        for row in range(4):
            pygame.draw.rect(screen,queuegrid[col-1][row-1],(board_position[0]+row*block_size,board_position[1]+col*block_size,block_size,block_size))

#pieces 0-t 1-J 2-L 3-z 4-s 5-o 6-i
#this function draws the shadow piece of the current piece by using similar code a the hard-drop --> this time does not actually register 
def drawshadow(shapenum, x, y, piecepos):
    if piecepos == 0:
        piece = pieces[shapenum]
    elif piecepos == 1:
        piece = pieces1[shapenum]
    elif piecepos == 2:
        piece = pieces2[shapenum]
    elif piecepos == 3:
        piece = pieces3[shapenum]
    landpos = y
    piececolors = [(185,35,70),(0,0,185),(185,95,0),(185,0,0),(0,185,0),(185,185,0),(0,185,185)] #darkened colors 
    color = piececolors[shapenum]
    while checkcollision(x, landpos + 1, piece) == False: #keep the piece going down until collision detected
        landpos += 1
    for i in range(len(piece)): #this mirors the piece from the pieces list onto the current grid
        for j in range(len(piece[i])):
            if i < len(tetris_grid) and j < len(tetris_grid[i]) and piece[i][j] != BLACK: #prevents BLACK spaces from printing, restrictions in case crash
                tetris_grid[landpos + i][x + j] = color
#this function draws the currently saved piece
def drawsave(save):
    piece = pieces[save]
    savegrid = []
    #setting color grid for drawing
    for col in range(4):
        savegrid += [[BLACK,BLACK,BLACK,BLACK]]
    for i in range(len(piece)): #this mirors the piece from the pieces list onto the current grid
            for j in range(len(piece[i])):
                if i < len(savegrid[i]) and j < len(savegrid[i]) and piece[i][j] != BLACK: #prevents BLACK spaces from printing, restrictions in case crash
                    savegrid[i][j] = piece[i][j]
    block_size = 25 #customizable 
    board_position = (50,50) #customizable
    for col in range(4):
        for row in range(4):
            pygame.draw.rect(screen,savegrid[col][row],(board_position[0]+row*block_size,board_position[1]+col*block_size,block_size,block_size))

#this function is the lose screen --> pops up before the game function ends. 
def losescreen(scored):
    screen.fill(BLACK)
    writetext("The E-Waste flooded planet Earth. Score: " + str(scored),80,100)
    writetext("E-waste makes up 70% of the total toxic waste!",65,150)
    pygame.display.flip()

#this is the game function. It will return nothing when the game is finished, but the highscore/scores will update
def game():
    screen.fill(BLACK)
    global savepiece, highscore
    gravitytimer = time.time()
    KEY_RIGHT = False
    KEY_LEFT = False
    KEY_DOWN = False 
    bag = generatebag()
    secondbag = generatebag()
    score = 0
    while True:
        #death locations
        if tetris_grid[0][3] == GRAY or tetris_grid[0][6] == GRAY or tetris_grid[0][4] == GRAY or tetris_grid[0][5] == GRAY or tetris_grid[0][7] == GRAY:
            if score > highscore: #update highscore file
                highscore = score
                highscorefile = open("scores.txt","w")
                highscorefile.write(str(highscore))
                highscorefile.close()
            losescreen(score)
            pygame.time.wait(4000)
            return None
        drawqueue(bag)
        bag += [secondbag.pop()]
        if secondbag == []:
            secondbag = generatebag()
        piecenum = bag.pop(0)
        grid_posx = 3
        grid_posy = 0
        pieceposition = 0
        #states
        KEY_RIGHT = False
        KEY_LEFT = False
        KEY_DOWN = False
        while True:
            pygame.draw.rect(screen,BLACK,(420,420,150,200))
            writetext("Score:",420,500)
            writetext(str(score),505,500)
            writetext("HScore:",420,470)
            writetext(str(highscore),515,470)
            cleargrid()
            drawshadow(piecenum,grid_posx,grid_posy,pieceposition)
            if savepiece != 7:
                drawsave(savepiece)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print("Exit")
                    quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        KEY_LEFT = True
                    if e.key == pygame.K_RIGHT:
                        KEY_RIGHT = True
                    if e.key == pygame.K_UP: #CLOCKWISE
                            if pieceposition == 3:
                                pieceposition = 0
                            else:
                                pieceposition += 1 
                            if checkcollision(grid_posx+1,grid_posy,currentpiece) == True and currentpiece[0][0] != YELLOW: #this is the wall kick system --> prevents collision with wall
                                if len(currentpiece[0]) == 1:
                                    grid_posx -= 2
                                grid_posx -= 1
                            #brute force bottom wallkick with long I piece
                            if grid_posx == 8 and currentpiece[0][0] == AQUA:
                                grid_posx -= 2
                            if grid_posx == 7 and currentpiece[0][0] == AQUA:
                                grid_posx -= 1
                            if grid_posy == 18 and currentpiece[0][0] != AQUA:
                                grid_posy -= 1
                            elif grid_posy == 19 and currentpiece[0][0] == AQUA:
                                grid_posy -= 3
                            elif grid_posy == 18 and currentpiece[0][0] == AQUA:
                                grid_posy -= 2
                            elif grid_posy == 17 and currentpiece[0][0] == AQUA:
                                grid_posy -= 1
                    if e.key == pygame.K_r:
                        return
                    if e.key == pygame.K_w: #COUNTERCLOCKWISE
                        if pieceposition == 0:
                            pieceposition = 3
                        else: 
                            pieceposition -= 1  
                        #wallkick for the counterclockwise rotation system
                        if checkcollision(grid_posx+1,grid_posy,currentpiece) == True and currentpiece[0][0] != YELLOW:
                                if len(currentpiece[0]) == 1:
                                    grid_posx -= 2
                                grid_posx -= 1
                        if grid_posx == 8 and currentpiece[0][0] == AQUA:
                            grid_posx -= 2
                        if grid_posx == 7 and currentpiece[0][0] == AQUA:
                            grid_posx -= 1
                        if grid_posy == 18 and currentpiece[0][0] != AQUA:
                            grid_posy -= 1
                        elif grid_posy == 19 and currentpiece[0][0] == AQUA:
                            grid_posy -= 3
                        elif grid_posy == 18 and currentpiece[0][0] == AQUA:
                            grid_posy -= 2
                        elif grid_posy == 17 and currentpiece[0][0] == AQUA:
                            grid_posy -= 1
                    if e.key == pygame.K_e: #180
                        if pieceposition == 3:
                            pieceposition = 1
                        elif pieceposition == 2:
                            pieceposition = 0
                        else:
                            pieceposition += 2
                    if e.key == pygame.K_SPACE: #HARDDROP
                        while checkcollision(grid_posx, grid_posy + 1, currentpiece) == False:
                            grid_posy += 1
                    if e.key == pygame.K_DOWN:
                        KEY_DOWN = True
                    if e.key == pygame.K_c:
                        #savepiece
                        if savepiece == 7:
                            bagpiece = bag[1]
                            savepiece = piecenum
                            piecenum = bag.pop(0)
                            bag.insert(0,bagpiece)
                            grid_posx,grid_posy = (3,0)
                            drawqueue(bag)
                            bag.remove(bagpiece)
                        else:
                            temppiecepos = piecenum
                            piecenum = savepiece
                            savepiece = temppiecepos
                            grid_posx,grid_posy = (3,0)

                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT:
                        KEY_LEFT = False 
                    if e.key == pygame.K_RIGHT:
                        KEY_RIGHT = False
                    if e.key == pygame.K_DOWN:
                        KEY_DOWN = False
            #getting the piece list from the pieces 3 dimentional list
            if pieceposition ==0:
                currentpiece = pieces[piecenum] 
            elif pieceposition == 1:
                currentpiece = pieces1[piecenum]
            elif pieceposition == 2:
                currentpiece = pieces2[piecenum]
            elif pieceposition ==3: 
                currentpiece = pieces3[piecenum]
            #GRAVITY
            if time.time() - gravitytimer >= 0.5:
                gravitytimer = time.time()
                if checkcollision(grid_posx,grid_posy+1,currentpiece) == False:
                    grid_posy += 1
            if checkcollision(grid_posx,grid_posy+1,currentpiece) == True or checkcollision(grid_posx,grid_posy+1,currentpiece) == 7: #set garabage collision to "7"
                if KEY_DOWN == False: #only updates block when down arrow is released
                    addthistoscore = updategarbage(currentpiece,grid_posx,grid_posy)-1
                    if addthistoscore > 0:
                        score += addthistoscore*5
                    break

            #LEFT AND RIGHT WALLS
            if KEY_LEFT and checkcollision(grid_posx-1,grid_posy,currentpiece) == False:
                grid_posx -= 1
            if KEY_RIGHT and checkcollision(grid_posx+1,grid_posy,currentpiece) == False:
                grid_posx += 1
            if KEY_DOWN and checkcollision(grid_posx,grid_posy+1,currentpiece) == False:
                if grid_posy <= 20:
                    grid_posy += 1

            drawpiece(piecenum, grid_posx, grid_posy,pieceposition)
            drawgrid()
            pygame.draw.line(screen,DARKRED,(150,125),(400,125))
            pygame.display.flip()
            myClock.tick(20)

#this is the main menu function - returns true if the play button is pressed. 
def mainmenu():
    mx, my = 0, 0
    rect_start = pygame.Rect(50,200,200,30)
    rect_quit = pygame.Rect(50,275,100,30)
    rect_start_outline = pygame.Rect(45,195,217,47)
    rect_quit_outline = pygame.Rect(45,270,117,47)
    rect_question = pygame.Rect(515,515,85,85)
    rect_lore = pygame.Rect(0,515,85,85)
    while True:
        home = (0,0,homescreen1.get_width(),homescreen1.get_height())
        screen.blit(homescreen1, home)
        button = 0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Exit")
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos          
                button = e.button
            elif e.type == pygame.MOUSEMOTION:
                mx, my = e.pos 
        pygame.draw.rect(screen,DARKERGRAY,rect_start_outline)
        pygame.draw.rect(screen,DARKERGRAY,rect_quit_outline)
        pygame.draw.rect(screen,DARKGRAY,rect_start)
        pygame.draw.rect(screen,DARKGRAY,rect_quit)
        if rect_start.collidepoint(mx, my):
            pygame.draw.rect(screen, DARKGREEN, rect_start)
            if button == 1:
                screen.fill(BLACK)
                return True
        elif rect_quit.collidepoint(mx,my):
            pygame.draw.rect(screen, DARKRED, rect_quit)
            if button == 1:
                print("Player_Quit")
                exit()
        elif rect_lore.collidepoint(mx,my):
            instructionmenu = (0,0,instruction.get_width(),instruction.get_height())
            screen.blit(instruction, instructionmenu)
        elif rect_question.collidepoint(mx,my):
            loremenu = (0,0,lore.get_width(),lore.get_height())
            screen.blit(lore, loremenu)
        pygame.display.flip()

savepiece = 7

#highscore file reading
highscorefileread = open("scores.txt","r")
text = highscorefileread.readline()
if text == "":
    highscore = 0
else:
    highscore = int(text)
highscorefileread.close()
myClock = pygame.time.Clock()

#main loop
while mainmenu() == True:
    resetgrid()
    game()
