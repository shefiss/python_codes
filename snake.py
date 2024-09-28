import pygame as pg
import random

pg.init()

tileSize = 20
scale = 20
speed = 30

maxY = tileSize*scale
maxX = tileSize*scale

screen = pg.display.set_mode((maxX,maxY))
pg.display.set_caption("Snake")
clock = pg.time.Clock()
running = True
dir = "right"
dt = 0

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
    pg.display.set_caption(f"Snake (score: " + score + ")")
    pg.display.flip()
    dt += 1

    clock.tick(60)

pg.quit()
