import pygame as pg
import random
from pygame.locals import *

pg.init()

#initializing things about the game
tileSize = 20 #game work in tiles (1 tile is for example snakes head, or the cherry)
scale = 20 #this is more like num of tiles in rows and columns
speed = 30
def_font = "monospace"
screen_height = tileSize*scale 
screen_width = tileSize*scale

#initializing the window
screen = pg.display.set_mode((screen_width,screen_height))
clock = pg.time.Clock()

name = "" #this is variable for the players name
cursor_pos_X = screen_width/8 #varaible for the X position of cursor in the text field for the name, it's global, because, the game keeps the name on the title after replaing, so you need to know where you left the cursor

table = [] #table of players, here is writen name and score of a player after game

#loading score from score.txt
def load_table():
    try:
        with open("score.txt", 'r') as file:
            for line in file:
                fields = line.split(" : ")

                x = fields[0]
                y = fields[1][:-1] #[:-1] is there to remove \n at the end of the line otherwise it would be visible in the title screen

                row = [x, y]
                table.append(row)
  
        file.close()
    except:
        pass

#saving score into score.txt, if the file doesn't exist, it will create it, dunno how, probably **magic**
def save_table():
    try:
        file = open("score.txt", 'w')
        l = len(table)
        for i in range(0,l):
            file.write(table[i][0] + " : ")
            file.write(table[i][1] + "\n")

    except:
        pass





def title_screen():
    running = True
    pg.display.set_caption("Snake")

    dt = 0 #dt here and in the rest of the code means delay time, it's because the game runs in 60fps, but for example the snake needs to update only twice a second
    cursor_color = 0 #switch between black and white color of the cursor, just for estetical purpose

    input_active = False
    global name

    main_font = pg.font.SysFont(def_font, 40)
    small_font = pg.font.SysFont(def_font, 20)

    start_game_white = main_font.render("START", True, "white")
    start_game_black = main_font.render("START", True, "black")
    name_prompt = small_font.render("YOUR NAME:", True, "white")
    top_score = small_font.render("SCORE:", True, "white")

    global cursor_pos_X
    cursor_white = small_font.render("_", True, "white")
    cursor_black = small_font.render("_", True, "black")
    
        

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if input_active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        input_active = False
                        
                    elif event.key == pg.K_BACKSPACE:
                        if name != "":
                            cursor_pos_X -= 12
                        name =  name[:-1]
                        
                    elif event.type == pg.KEYDOWN:
                        if len(name) >= 11:
                            pass
                        else:
                            if event.key in range(pg.K_a, pg.K_z):
                                cursor_pos_X += 12
                                name += event.unicode

                            if event.key in range(pg.K_0, pg.K_9):
                                cursor_pos_X += 12
                                name += event.unicode
                            
        screen.fill("black")

        name_input_white = small_font.render(name, True, "white")
        name_input_black = small_font.render(name, True, "black")

        mouse = pg.mouse.get_pos()

        #setting your name
        screen.blit(name_prompt, (screen_width/8,screen_height/8))

        
        if dt == 30:
            cursor_color = (cursor_color + 1)%2 #cursor changing color twice a second, depends on the color of backgrownd as seen on line 135 and 144
            dt = 0

        #most of the code here is just for the buttons to change appearance
        if screen_width/8 <= mouse[0] <= screen_width/8 +200 and screen_height/8 + 30 <= mouse[1] <= screen_height/8 + 50 and input_active == False:
            pg.draw.rect(screen, "white", [screen_width/8,screen_height/8 + 30, 150, 20])
            screen.blit(name_input_black, (screen_width/8,screen_height/8 + 30))
            if event.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(screen, "black", [screen_width/8,screen_height/8 + 30, 150, 20]) #this is there only because I find the button flickering when pressed convinient
                input_active = True

        elif screen_width/8 <= mouse[0] <= screen_width/8 +200 and screen_height/8 + 30 <= mouse[1] <= screen_height/8 + 50 and input_active == True:
            pg.draw.rect(screen, "white", [screen_width/8,screen_height/8 + 30, 150, 20])
            screen.blit(name_input_black, (screen_width/8,screen_height/8 + 30))
            if cursor_color == 1:
                screen.blit(cursor_black, (cursor_pos_X, screen_height/8 + 27))
            else:
                screen.blit(cursor_white, (cursor_pos_X, screen_height/8 + 27))
            
        elif not(screen_width/8 <= mouse[0] <= screen_width/8 +200 and screen_height/8 + 30 <= mouse[1] <= screen_height/8 + 50) and input_active == True:
            screen.blit(name_input_white, (screen_width/8,screen_height/8 + 30))
            
            if cursor_color == 1:
                screen.blit(cursor_white, (cursor_pos_X, screen_height/8 + 27))
            else:
                screen.blit(cursor_black, (cursor_pos_X, screen_height/8 + 27))

            if event.type == pg.MOUSEBUTTONDOWN:
                input_active = False
        
        else:
            screen.blit(name_input_white, (screen_width/8,screen_height/8 + 30))

        
        #score names
        screen.blit(top_score, (250, 10))

        l = len(table)
        for i in range(0,l):
            t1 = small_font.render(table[i][0], True, "white")
            t2 = small_font.render(table[i][1], True, "white")
            screen.blit(t1, (250, 40 + 20*i))
            screen.blit(t2, (350, 40 + 20*i))



        #start game button
        if screen_width/8 <= mouse[0] <= screen_width/8 +120 and screen_height/2 <= mouse[1] <= screen_height/2 + 40:
            pg.draw.rect(screen, "white", [screen_width/8,screen_height/2,120,40])
            screen.blit(start_game_black, (screen_width/8, screen_height/2))
            if pg.mouse.get_pressed() == (1,0,0) and name != "":
                game()
                running = False
        else:
            screen.blit(start_game_white, (screen_width/8, screen_height/2))


        dt += 1
        clock.tick(60)
        pg.display.flip()

#game loop itself
def game():
    speed = 30
    running = True
    dir = "right"
    dt = 0

    global name

    player_pos = pg.Vector2(screen.get_width() / tileSize, screen.get_height() / tileSize)
    snake_size = 0
    snake_tiles = [[player_pos.x,player_pos.y]]

    cherry_exists = False
    cherryX = 0 
    cherryY = 0

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")

        #cherry generator
        collision_found = False
        if cherry_exists == False:
            
            while not(cherry_exists):
                cherryX = random.randint(1,scale-1)*tileSize
                cherryY = random.randint(1,scale-1)*tileSize
                
                #this checks if the cherry spawned in the body of the snake
                for i in range(0, snake_size):
                    if cherryX == snake_tiles[i][0] and cherryY == snake_tiles[i][1]:
                        collision_found = True

                if collision_found == False:
                    cherry_exists = True
                collision_found = False
                 
        #drawing objects

        #body calculation
        i = snake_size
        while i >= 0:
            if dt == speed: #the calculation of the body is done by inheriting, so the first body part behind head is inheriting the position of the head and so on
                if i == 0: #this is the inheriting from head
                    snake_tiles[i][0] = player_pos.x
                    snake_tiles[i][1] = player_pos.y
                    
                else:
                    try: #this is the inheriting of other body parts (it's pretty strait forward)
                        snake_tiles[i][0] = snake_tiles[i-1][0]
                        snake_tiles[i][1] = snake_tiles[i-1][1]
                    except: #when the snake eats a cherry, new body part have to be added, so it tries to inherit to the last part, which doesn't exist, so this will create it
                        x = snake_tiles[i-1][0]
                        y = snake_tiles[i-1][1]
                        new_line = [x,y]
                        snake_tiles.append(new_line)
        #body drawing            
            try:
                pg.draw.rect(screen, "gray", pg.Rect(snake_tiles[i][0], snake_tiles[i][1], tileSize, tileSize))

            except:
                pass #after eating cherry, the new body part is calculated later than the drawing module tries to render it, so this try/except lets the game calculate it
            i -= 1  

        #head render
        pg.draw.rect(screen, "white", pg.Rect(player_pos.x, player_pos.y, tileSize, tileSize))

        #cherry render
        pg.draw.rect(screen, "red", pg.Rect(cherryX, cherryY, tileSize, tileSize))

        #checking if a cherry was eaten
        if cherryX == player_pos.x and cherryY == player_pos.y:
                cherry_exists = False
                snake_size += 1
                if speed > 12: #speed increases every time you eat cherry, but it have to stop at some point
                    speed -= 1
            
        #colision check
        for j in range(3, snake_size): #it starts at 3 because num 0 is the head and 1,2,3 might be problematic
            try:
                if player_pos.x == snake_tiles[j][0] and player_pos.y == snake_tiles[j][1]: #player_pos is the head, snake_tiles is matrix of body parts
                    running = False
            except:
                pass #try/except is there for the same reason as when rendering, if it tries to check colision earlier than calculating the metrix, it will crash
         
        #movement controls
        keys = pg.key.get_pressed() #it is not probably the best possible way to do that, because when two keys are pressed at the same time, it might bug the head inside of the body (I just don't know how to do it better)
        if (keys[pg.K_UP] or keys[pg.K_w]) and dir != "down":
            dir = "up"
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and dir != "up":
            dir = "down"
        elif (keys[pg.K_LEFT] or keys[pg.K_a]) and dir != "right":
            dir = "left"
        elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and dir != "left":
            dir = "right"

        #movement it self
        #as in normal snake, the snake moves by it self, you just control the direction
        if dt == speed:
            match dir:
                case "up":
                    if player_pos.y == 0:
                        running = False
                    else:
                        player_pos.y -= tileSize

                case "down":
                    if player_pos.y == screen_height - tileSize:
                        running = False
                    else:
                        player_pos.y += tileSize

                case "left":
                    if player_pos.x == 0:
                        running = False
                    else:
                        player_pos.x -= tileSize

                case "right":
                    if player_pos.x == screen_width - tileSize:
                        running = False
                    else:
                        player_pos.x += tileSize

            dt = 0


        
            
        #the score is added to the caption along with the name
        score = str(snake_size)
        pg.display.set_caption(f"Snake (" + name + "'s score: " + score + ")")


        pg.display.flip()
        dt += 1

        clock.tick(60)

    game_over(score=score)
    

def game_over(score): #the score is passed between the functions and not a global variable, because this way it's assured the ingame score will be reseted everytime
    running = True
    main_font = pg.font.SysFont(def_font, 40)
    small_font = pg.font.SysFont(def_font, 20)

    global name
    global table

    #adding to a score table
    
    row = [name, score]
    l = len(table)

    name_exists = False
    for i in range(0, l):
        if name == table[i][0] and score > table[i][1]: #this part checks if the name already exists in the scoreboard and if the score is higher than the last one
            name_exists = True
            table[i][0] = name
            table[i][1] = score
        elif name == table[i][0] and score <= table[i][1]:
            name_exists = True
    if not(name_exists):
        table.append(row)
    name_exists = False
    save_table()

    pg.display.set_caption("Snake (GAME OVER)")

    game_over_white = main_font.render("GAME OVER", True, "white")
    score_white =small_font.render("Your score is " + str(score), True, "white")

    play_again_white = main_font.render("PLAY AGAIN?", True, "white")
    play_again_black = main_font.render("PLAY AGAIN?", True, "black")

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")

        screen.blit(game_over_white, (screen_width/5 + 10, screen_height/3))
        screen.blit(score_white, (screen_width/4 + 10, screen_height/3 + 50))

        mouse = pg.mouse.get_pos()

        #again, a lot of code just for the button interact with mouse cursor
        if screen_width/6 <= mouse[0] <= screen_width/6 +260 and screen_height/5 + 200 <= mouse[1] <= screen_height/5 + 240:
            pg.draw.rect(screen, "white", [screen_width/6,screen_height/5 + 200,260,40])
            screen.blit(play_again_black, (screen_width/6, screen_height/5 + 200))
            if pg.mouse.get_pressed() == (1,0,0):
                title_screen()
                running = False
        else:
            screen.blit(play_again_white, (screen_width/6, screen_height/5 + 200))



        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    load_table()
    title_screen()

pg.quit()