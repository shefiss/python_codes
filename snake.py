import pygame as pg
import random
from pygame.locals import *
import time

pg.init()

tileSize = 20
scale = 20
speed = 30

maxY = tileSize*scale
maxX = tileSize*scale

screen = pg.display.set_mode((maxX,maxY))

clock = pg.time.Clock()

name = ""


def title_screen():
    running = True
    pg.display.set_caption("Snake")

    input_active = False
    global name

    main_font = pg.font.SysFont("monospace", 40)
    small_font = pg.font.SysFont("monospace", 20)

    start_game_white = main_font.render("START", True, "white")
    start_game_black = main_font.render("START", True, "black")
    name_prompt = small_font.render("YOUR NAME:", True, "white")

    
    
    

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if input_active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        input_active = False
                    elif event.key == pg.K_BACKSPACE:
                        name =  name[:-1]
                    elif event.type == pg.KEYDOWN:
                        name += event.unicode
                

        screen.fill("black")

        name_input_white = small_font.render(name, True, "white")
        name_input_black = small_font.render(name, True, "black")

        mouse = pg.mouse.get_pos()

        #setting your name
        screen.blit(name_prompt, (maxX/8,maxY/8))

        



        if maxX/8 <= mouse[0] <= maxX/8 +200 and maxY/8 + 30 <= mouse[1] <= maxY/8 + 50 and input_active == False:
            pg.draw.rect(screen, "white", [maxX/8,maxY/8 + 30, 200, 20])
            screen.blit(name_input_black, (maxX/8,maxY/8 + 30))
            if event.type == pg.MOUSEBUTTONDOWN:
                input_active = True

        elif maxX/8 <= mouse[0] <= maxX/8 +200 and maxY/8 + 30 <= mouse[1] <= maxY/8 + 50 and input_active == True:
            pg.draw.rect(screen, "white", [maxX/8,maxY/8 + 30, 200, 20])
            screen.blit(name_input_black, (maxX/8,maxY/8 + 30))
            

        elif not(maxX/8 <= mouse[0] <= maxX/8 +200 and maxY/8 + 30 <= mouse[1] <= maxY/8 + 50) and input_active == True:
            screen.blit(name_input_white, (maxX/8,maxY/8 + 30))
            if event.type == pg.MOUSEBUTTONDOWN:
                input_active = False
        
        else:
            screen.blit(name_input_white, (maxX/8,maxY/8 + 30))

        
            




        #start game button
        if maxX/8 <= mouse[0] <= maxX/8 +120 and maxY/2 <= mouse[1] <= maxY/2 + 40:
            pg.draw.rect(screen, "white", [maxX/8,maxY/2,120,40])
            screen.blit(start_game_black, (maxX/8, maxY/2))
            if pg.mouse.get_pressed() == (1,0,0):
                game()
                running = False
        else:
            screen.blit(start_game_white, (maxX/8, maxY/2))


        

        pg.display.flip()

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

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")

        #cherry generator
        
        if cherry_exists == False:
            ranX = random.randint(1,scale-1)*tileSize
            ranY = random.randint(1,scale-1)*tileSize
            cherry_exists = True

        

        #drawing objects

        #body
        i = snake_size
        while i >= 0:
            if dt == speed:
                if i == 0:
                    snake_tiles[i][0] = player_pos.x
                    snake_tiles[i][1] = player_pos.y
                    
                else:
                    try:
                        snake_tiles[i][0] = snake_tiles[i-1][0]
                        snake_tiles[i][1] = snake_tiles[i-1][1]
                    except:
                        x = snake_tiles[i-1][0]
                        y = snake_tiles[i-1][1]
                        new_line = [x,y]
                        snake_tiles.append(new_line)
                    
            try:
                pg.draw.rect(screen, "gray", pg.Rect(snake_tiles[i][0], snake_tiles[i][1], tileSize, tileSize))

            except:
                pass
            i -= 1  

        #head
        pg.draw.rect(screen, "white", pg.Rect(player_pos.x, player_pos.y, tileSize, tileSize))

        #cherry
        pg.draw.rect(screen, "red", pg.Rect(ranX, ranY, tileSize, tileSize))

        if ranX == player_pos.x and ranY == player_pos.y:
                cherry_exists = False
                snake_size += 1
                if speed > 12:
                    speed -= 1
            
        #colision check
        for j in range(3, snake_size):
            if player_pos.x == snake_tiles[j][0] and player_pos.y == snake_tiles[j][1]:
                running = False
        
        
                

        #movement controls
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and dir != "down":
            dir = "up"
        elif keys[pg.K_DOWN]and dir != "up":
            dir = "down"
        elif keys[pg.K_LEFT] and dir != "right":
            dir = "left"
        elif keys[pg.K_RIGHT] and dir != "left":
            dir = "right"


        if dt == speed:

            


            match dir:
                case "up":
                    if player_pos.y == 0:
                        running = False
                    else:
                        player_pos.y -= tileSize

                case "down":
                    if player_pos.y == maxY - tileSize:
                        running = False
                    else:
                        player_pos.y += tileSize

                case "left":
                    if player_pos.x == 0:
                        running = False
                    else:
                        player_pos.x -= tileSize

                case "right":
                    if player_pos.x == maxX - tileSize:
                        running = False
                    else:
                        player_pos.x += tileSize

            dt = 0


        
            

        score = str(snake_size)
        pg.display.set_caption(f"Snake (" + name + "'s score: " + score + ")")
        pg.display.flip()
        dt += 1

        clock.tick(60)

    game_over(score=score)
    

def game_over(score):
    running = True
    main_font = pg.font.SysFont("monospace", 40)
    small_font = pg.font.SysFont("monospace", 20)

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

        screen.blit(game_over_white, (maxX/5 + 10, maxY/3))
        screen.blit(score_white, (maxX/4 + 10, maxY/3 + 50))

        mouse = pg.mouse.get_pos()

        if maxX/6 <= mouse[0] <= maxX/6 +260 and maxY/5 + 200 <= mouse[1] <= maxY/5 + 240:
            pg.draw.rect(screen, "white", [maxX/6,maxY/5 + 200,260,40])
            screen.blit(play_again_black, (maxX/6, maxY/5 + 200))
            if pg.mouse.get_pressed() == (1,0,0):
                title_screen()
                running = False
        else:
            screen.blit(play_again_white, (maxX/6, maxY/5 + 200))



        pg.display.flip()


if __name__ == "__main__":
    title_screen()

pg.quit()
