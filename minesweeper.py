import pygame
import random
import numpy as np

pygame.init()

screen_width = 600
screen_height = 700
field_size = screen_width
control_panel_size = screen_height-field_size
default_font = "monospace"


screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Mine Sweeper")

#sizes: 7, 11, 14, 19
grid_size = 11
difficulty = 1
tile_size = field_size/(grid_size + 1)

mouse_hold_left = False
mouse_hold_right = False
grid_visible = np.full((grid_size,grid_size), 0)


def mouse_pressed_left():
    global mouse_hold_left
    if pygame.mouse.get_pressed()[0] == True and mouse_hold_left == False:
        mouse_hold_left = True
        return True
    elif pygame.mouse.get_pressed()[0] == True and mouse_hold_left == True:
        return False
    elif pygame.mouse.get_pressed()[0] == False and mouse_hold_left == True:
        mouse_hold_left = False
        return False
    else:
        return False

def mouse_pressed_right():
    global mouse_hold_right
    if pygame.mouse.get_pressed()[2] == True and mouse_hold_right == False:
        mouse_hold_right = True
        return True
    elif pygame.mouse.get_pressed()[2] == True and mouse_hold_right == True:
        return False
    elif pygame.mouse.get_pressed()[2] == False and mouse_hold_right == True:
        mouse_hold_right = False
        return False
    else:
        return False

def draw_text(string, size, color):
    font = pygame.font.SysFont(default_font, int(size))
    return font.render(string, True, color)


def calculate_grid(mouse_pressed_position, grid):
    
    for i in range(0,grid_size*difficulty):
        tile_item = 9
        tile_x = mouse_pressed_position[0]
        tile_y = mouse_pressed_position[1]

        

        while tile_item == 9 or ((tile_x == mouse_pressed_position[0] and tile_y == mouse_pressed_position[1])
                                or (tile_x == mouse_pressed_position[0]+1 and tile_y == mouse_pressed_position[1])
                                or (tile_x == mouse_pressed_position[0]-1 and tile_y == mouse_pressed_position[1])
                                or (tile_x == mouse_pressed_position[0] and tile_y == mouse_pressed_position[1]+1)
                                or (tile_x == mouse_pressed_position[0] and tile_y == mouse_pressed_position[1]-1)
                                or (tile_x == mouse_pressed_position[0]+1 and tile_y == mouse_pressed_position[1]+1)
                                or (tile_x == mouse_pressed_position[0]-1 and tile_y == mouse_pressed_position[1]-1)
                                or (tile_x == mouse_pressed_position[0]+1 and tile_y == mouse_pressed_position[1]-1)
                                or (tile_x == mouse_pressed_position[0]-1 and tile_y == mouse_pressed_position[1]+1)):
            tile_x = random.choice(range(0,grid_size))
            tile_y = random.choice(range(0,grid_size))
            tile_item = grid[tile_x][tile_y]

        grid[tile_x][tile_y] = 9

    for i in range(0, grid_size):
        for j in range(0,grid_size):
            if grid[i][j] == 9:
                continue
            else:
                mines_around = 0
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if k >= grid_size or k < 0 or l >= grid_size or l < 0:
                            continue

                        if grid[k][l] == 9:
                            mines_around += 1

                        

                grid[i][j] = mines_around

    return grid



def check_tile(mouse_pressed_position, grid):
    global grid_visible
    mouse_x = mouse_pressed_position[0]
    mouse_y = mouse_pressed_position[1]
    if grid_visible[mouse_x, mouse_y] == 0:
        grid_visible[mouse_x, mouse_y] = 1


    field = np.array([[mouse_x,mouse_y]])


    index = 0
    if grid[mouse_x][mouse_y] == 0:

        while field.size != 0:
            x = field[index,0]
            y = field[index,1]
            
            if grid[x][y] == 0:
                
                if x+1 < grid_size and grid_visible[x+1][y] == 0:
                    field = np.append(field, [[x+1,y]], 0)

                if x-1 >= 0 and grid_visible[x-1][y] == 0:
                    field = np.append(field, [[x-1,y]], 0)

                if y+1 < grid_size and grid_visible[x][y+1] == 0:
                    field = np.append(field, [[x,y+1]], 0)

                if y-1 >= 0 and grid_visible[x][y-1] == 0:
                    field = np.append(field, [[x,y-1]], 0)
        
                
            if grid_visible[x,y] == 0:
                grid_visible[x,y] = 1
            field = np.delete(field, index, 0)
            
        
def title_screen():
    running = True
    start_x = screen_width/4 + screen_width/12
    start_y = screen_height/8 + screen_height/2
    difficulty_label_x = screen_width/4 + screen_width/14
    difficulty_label_y = screen_height/8
    grid_size_x = screen_width/4 + screen_width/7
    grid_size_y = screen_height/8 + screen_height/4
    difficulty_buttons_x = difficulty_label_x
    difficulty_buttons_y = difficulty_label_y + 40
    grid_size_buttons_x = difficulty_buttons_x - 30
    grid_size_buttons_y = grid_size_y + 40

    global difficulty
    global grid_size
    global tile_size
    global grid_visible

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        mouse_pos = pygame.mouse.get_pos()

        difficulty_label = draw_text("Difficulty:", 30, "black")
        screen.blit(difficulty_label, (difficulty_label_x, difficulty_label_y))
        size_label = draw_text("Size:", 30, "black")
        screen.blit(size_label, (grid_size_x, grid_size_y))

        if difficulty == 1:
            text = draw_text("1", 40, "white")
            pygame.draw.rect(screen, "black", [difficulty_buttons_x,difficulty_buttons_y,50,50])
            screen.blit(text, (difficulty_buttons_x+15, difficulty_buttons_y+5))
        else:
            if (difficulty_buttons_x <= mouse_pos[0] <= difficulty_buttons_x +50 
                and difficulty_buttons_y <= mouse_pos[1] <= difficulty_buttons_y + 50
                and grid_size < 14):
                text = draw_text("1", 40, "black")
                pygame.draw.rect(screen, "lightgray", [difficulty_buttons_x,difficulty_buttons_y,50,50])
                screen.blit(text, (difficulty_buttons_x+15, difficulty_buttons_y+5))
                if mouse_pressed_left() == True:
                    difficulty = 1
            else:
                text = draw_text("1", 40, "black")
                screen.blit(text, (difficulty_buttons_x+15, difficulty_buttons_y+5))

        if difficulty == 2:
            text = draw_text("2", 40, "white")
            pygame.draw.rect(screen, "black", [difficulty_buttons_x + 60,difficulty_buttons_y,50,50])
            screen.blit(text, (difficulty_buttons_x + 60+15, difficulty_buttons_y+5))
        else:
            if (difficulty_buttons_x + 60 <= mouse_pos[0] <= difficulty_buttons_x + 60 +50 
                and difficulty_buttons_y <= mouse_pos[1] <= difficulty_buttons_y + 50
                and grid_size < 19):
                text = draw_text("2", 40, "black")
                pygame.draw.rect(screen, "lightgray", [difficulty_buttons_x + 60,difficulty_buttons_y,50,50])
                screen.blit(text, (difficulty_buttons_x + 60+15, difficulty_buttons_y+5))
                if mouse_pressed_left() == True:
                    difficulty = 2
            else:
                text = draw_text("2", 40, "black")
                screen.blit(text, (difficulty_buttons_x + 60+15, difficulty_buttons_y+5))

        if difficulty == 3:
            text = draw_text("3", 40, "white")
            pygame.draw.rect(screen, "black", [difficulty_buttons_x+120,difficulty_buttons_y,50,50])
            screen.blit(text, (difficulty_buttons_x+120+15, difficulty_buttons_y+5))
        else:
            if (difficulty_buttons_x+120 <= mouse_pos[0] <= difficulty_buttons_x+120 +50 
                and difficulty_buttons_y <= mouse_pos[1] <= difficulty_buttons_y + 50):
                text = draw_text("3", 40, "black")
                pygame.draw.rect(screen, "lightgray", [difficulty_buttons_x+120,difficulty_buttons_y,50,50])
                screen.blit(text, (difficulty_buttons_x+120+15, difficulty_buttons_y+5))
                if mouse_pressed_left() == True:
                    difficulty = 3
            else:
                text = draw_text("3", 40, "black")
                screen.blit(text, (difficulty_buttons_x+120+15, difficulty_buttons_y+5))

        #sizes: 7, 11, 14, 19
        if grid_size == 7:
            text = draw_text("7", 40, "white")
            pygame.draw.rect(screen, "black", [grid_size_buttons_x,grid_size_buttons_y,50,50])
            screen.blit(text, (grid_size_buttons_x+12, grid_size_buttons_y+5))
        else:
            if (grid_size_buttons_x <= mouse_pos[0] <= grid_size_buttons_x +50 
                and grid_size_buttons_y <= mouse_pos[1] <= grid_size_buttons_y + 50):
                text = draw_text("7", 40, "black")
                pygame.draw.rect(screen, "lightgray", [grid_size_buttons_x,grid_size_buttons_y,50,50])
                screen.blit(text, (grid_size_buttons_x+12, grid_size_buttons_y+5))
                if mouse_pressed_left() == True:
                    grid_size = 7
                    difficulty = 1
            else:
                text = draw_text("7", 40, "black")
                screen.blit(text, (grid_size_buttons_x+12, grid_size_buttons_y+5))

        if grid_size == 11:
            text = draw_text("11", 40, "white")
            pygame.draw.rect(screen, "black", [grid_size_buttons_x+60,grid_size_buttons_y,50,50])
            screen.blit(text, (grid_size_buttons_x+60+1, grid_size_buttons_y+5))
        else:
            if (grid_size_buttons_x+60 <= mouse_pos[0] <= grid_size_buttons_x+60 +50 
                and grid_size_buttons_y <= mouse_pos[1] <= grid_size_buttons_y + 50):
                text = draw_text("11", 40, "black")
                pygame.draw.rect(screen, "lightgray", [grid_size_buttons_x+60,grid_size_buttons_y,50,50])
                screen.blit(text, (grid_size_buttons_x+60+1, grid_size_buttons_y+5))
                if mouse_pressed_left() == True:
                    grid_size = 11
                    difficulty = 2
            else:
                text = draw_text("11", 40, "black")
                screen.blit(text, (grid_size_buttons_x+60+1, grid_size_buttons_y+5))

        if grid_size == 14:
            text = draw_text("14", 40, "white")
            pygame.draw.rect(screen, "black", [grid_size_buttons_x+120,grid_size_buttons_y,50,50])
            screen.blit(text, (grid_size_buttons_x+120+1, grid_size_buttons_y+5))
        else:
            if (grid_size_buttons_x+120 <= mouse_pos[0] <= grid_size_buttons_x+120 +50 
                and grid_size_buttons_y <= mouse_pos[1] <= grid_size_buttons_y + 50):
                text = draw_text("14", 40, "black")
                pygame.draw.rect(screen, "lightgray", [grid_size_buttons_x+120,grid_size_buttons_y,50,50])
                screen.blit(text, (grid_size_buttons_x+120+1, grid_size_buttons_y+5))
                if mouse_pressed_left() == True:
                    grid_size = 14
                    difficulty = 2
            else:
                text = draw_text("14", 40, "black")
                screen.blit(text, (grid_size_buttons_x+120+1, grid_size_buttons_y+5))

        if grid_size == 19:
            text = draw_text("19", 40, "white")
            pygame.draw.rect(screen, "black", [grid_size_buttons_x+180,grid_size_buttons_y,50,50])
            screen.blit(text, (grid_size_buttons_x+180+1, grid_size_buttons_y+5))
        else:
            if (grid_size_buttons_x+180 <= mouse_pos[0] <= grid_size_buttons_x+180 +50 
                and grid_size_buttons_y <= mouse_pos[1] <= grid_size_buttons_y + 50):
                text = draw_text("19", 40, "black")
                pygame.draw.rect(screen, "lightgray", [grid_size_buttons_x+180,grid_size_buttons_y,50,50])
                screen.blit(text, (grid_size_buttons_x+180+1, grid_size_buttons_y+5))
                if mouse_pressed_left() == True:
                    grid_size = 19
                    difficulty = 3
            else:
                text = draw_text("19", 40, "black")
                screen.blit(text, (grid_size_buttons_x+180+1, grid_size_buttons_y+5))


        if start_x <= mouse_pos[0] <= start_x +180 and start_y <= mouse_pos[1] <= start_y + 60:
            text = draw_text("START", 60, "white")
            pygame.draw.rect(screen, "black", [start_x,start_y,180,60])
            screen.blit(text, (start_x, start_y))
            if mouse_pressed_left() == True:
                tile_size = field_size/(grid_size + 1)
                grid_visible = np.full((grid_size,grid_size), 0)
                game()
                running = False
        else:
            text = draw_text("START", 60, "black")
            screen.blit(text, (start_x, start_y))

        pygame.display.flip()
        clock.tick(60)
    



def game():
    running = True
    grid = np.full((grid_size,grid_size), 0)
    
    first_guess_happend = False
    mouse_pressed_position = [0,0]
    timer = 0
    dt = 0

    flags_num = grid_size*difficulty
    flags_num_x = 25
    flags_num_y = 20
    timer_x = 175
    timer_y = 20
    start_x = 390
    start_y = 10
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # draw the control panel
        pygame.draw.line(screen,"black",
                         (flags_num_x, flags_num_y),
                         (flags_num_x, flags_num_y +60),
                         2)
        pygame.draw.polygon(screen, "red", 
                            ((flags_num_x, flags_num_y),
                             (flags_num_x, flags_num_y +30),
                             (flags_num_x +30, flags_num_y +15))
                            )
        flags_text = draw_text("=" + str(flags_num), 50, "black")
        screen.blit(flags_text, (flags_num_x+40, flags_num_y+5))

        
        pygame.draw.line(screen, "red", (timer_x +30, timer_y +10), (timer_x +30, timer_y +30), 4)
        pygame.draw.line(screen, "gray", (timer_x +30, timer_y +30), (timer_x +50, timer_y +30), 4)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 30, 6)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 6, 6)
        timer_text = draw_text("=" + str(timer), 50, "black")
        screen.blit(timer_text, (timer_x+70, timer_y+5))

        mouse_pos = pygame.mouse.get_pos()
        if start_x <= mouse_pos[0] <= start_x +190 and start_y+20 <= mouse_pos[1] <= start_y + 60:
            text = draw_text("NEW GAME", 40, "white")
            pygame.draw.rect(screen, "black", [start_x,start_y+20,190,40])
            screen.blit(text, (start_x, start_y+20))
            if mouse_pressed_left() == True:
                title_screen()
                running = False
        else:
            text = draw_text("NEW GAME", 40, "black")
            screen.blit(text, (start_x, start_y+20))

        # game loop
        if first_guess_happend == False:
            mouse_pos = pygame.mouse.get_pos()
            

            for i in range(0,grid_size):
                for j in range(0,grid_size):

                    pygame.draw.rect(screen, "lightgray", 
                                     pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                     0)

                    if (int((mouse_pos[0]-tile_size/2)/tile_size), int((mouse_pos[1]-control_panel_size-tile_size/2)/tile_size)) == (i,j):
                        pygame.draw.rect(screen, "gray", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        0)
                        
                        if mouse_pressed_left() == True:
                            mouse_pressed_position = [j,i]
                            grid = calculate_grid(mouse_pressed_position, grid)
                            first_guess_happend = True
                            #print(grid)
                            check_tile(mouse_pressed_position, grid)
                            
                                
                        
                    
                    pygame.draw.rect(screen, "black", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        1)
                    
        if first_guess_happend == True:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(0,grid_size):
                for j in range(0,grid_size):
                    
                    pygame.draw.rect(screen, "lightgray", 
                                     pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                     0)

                    if (int((mouse_pos[0]-tile_size/2)/tile_size), int((mouse_pos[1]-control_panel_size-tile_size/2)/tile_size)) == (i,j):
                        pygame.draw.rect(screen, "gray", 
                                            pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                            0)
                        

                        if mouse_pressed_left() == True:
                            mouse_pressed_position = [j,i]
                            #if bomb is pressed
                            if grid_visible[mouse_pressed_position[0],mouse_pressed_position[1]] != 2:
                                if grid[mouse_pressed_position[0],mouse_pressed_position[1]] == 9:
                                    end_screen(grid, grid_size, timer, flags_num)
                                    running = False

                                #if something other is pressed
                                if grid[mouse_pressed_position[0],mouse_pressed_position[1]] != 9:
                                    check_tile(mouse_pressed_position, grid)

                        elif mouse_pressed_right() == True:
                            mouse_pressed_position = [j,i]
                            
                            if (grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 0
                                and flags_num > 0):
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 2
                                flags_num -= 1
                                

                            elif grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 2:
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 0
                                flags_num += 1

                    if grid_visible[j][i] == 1:
                        pygame.draw.rect(screen, "white", 
                                         pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                         0)
                        if grid[j][i] != 0 and grid[j][i] != 9:
                            number = draw_text(str(grid[j][i]), tile_size, "black")
                            
                            screen.blit(number, (i*tile_size +tile_size/2 + tile_size/5, j*tile_size + control_panel_size +tile_size/2))
                    
                    if grid_visible[j][i] == 2:
                        pygame.draw.rect(screen, "gray", 
                                         pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                         0)
                        pygame.draw.line(screen,"black",
                                         (4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3),
                                         (4+i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + tile_size/2),
                                         2)
                        pygame.draw.polygon(screen, "red", 
                                            ((4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3),
                                             (4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + (tile_size/2)/2),
                                             (4+ i*tile_size +tile_size/2 +tile_size/3 + tile_size/4, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + (tile_size/2)/4))
                                             )
                    
                    pygame.draw.rect(screen, "black", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        1)
        if dt == 60:
            timer += 1
            dt = 0

        dt += 1      
        clock.tick(60)
        pygame.display.flip()



def end_screen(grid, grid_size, timer, flags_num):
    running = True

    flags_num_x = 25
    flags_num_y = 20
    timer_x = 175
    timer_y = 20
    start_x = 390
    start_y = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # draw the control panel
        pygame.draw.line(screen,"black",
                         (flags_num_x, flags_num_y),
                         (flags_num_x, flags_num_y +60),
                         2)
        pygame.draw.polygon(screen, "red", 
                            ((flags_num_x, flags_num_y),
                             (flags_num_x, flags_num_y +30),
                             (flags_num_x +30, flags_num_y +15))
                            )
        flags_text = draw_text("=" + str(flags_num), 50, "black")
        screen.blit(flags_text, (flags_num_x+40, flags_num_y+5))

        
        pygame.draw.line(screen, "red", (timer_x +30, timer_y +10), (timer_x +30, timer_y +30), 4)
        pygame.draw.line(screen, "gray", (timer_x +30, timer_y +30), (timer_x +50, timer_y +30), 4)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 30, 6)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 6, 6)
        timer_text = draw_text("=" + str(timer), 50, "black")
        screen.blit(timer_text, (timer_x+70, timer_y+5))

        mouse_pos = pygame.mouse.get_pos()
        if start_x <= mouse_pos[0] <= start_x +190 and start_y+20 <= mouse_pos[1] <= start_y + 60:
            text = draw_text("NEW GAME", 40, "white")
            pygame.draw.rect(screen, "black", [start_x,start_y+20,190,40])
            screen.blit(text, (start_x, start_y+20))
            if mouse_pressed_left() == True:
                title_screen()
                running = False
        else:
            text = draw_text("NEW GAME", 40, "black")
            screen.blit(text, (start_x, start_y+20))



        
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if grid[j][i] == 9:
                    pygame.draw.rect(screen, "red", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        0)    
                if grid[j][i] != 0 and grid[j][i] != 9:
                    number = draw_text(str(grid[j][i]), tile_size, "black")
                            
                    screen.blit(number, (i*tile_size +tile_size/2 + tile_size/5, j*tile_size + control_panel_size +tile_size/2))
                
                if grid_visible[j][i] == 2:
                        if grid[j][i] == 9:
                            pygame.draw.rect(screen, "green", 
                                            pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                            0)
                        else:
                            pygame.draw.rect(screen, "gray", 
                                            pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                            0)

                        pygame.draw.line(screen,"black",
                                         (4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3),
                                         (4+i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + tile_size/2),
                                         2)
                        pygame.draw.polygon(screen, "red", 
                                            ((4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3),
                                             (4+ i*tile_size +tile_size/2 +tile_size/3, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + (tile_size/2)/2),
                                             (4+ i*tile_size +tile_size/2 +tile_size/3 + tile_size/4, -4 + j*tile_size + control_panel_size +tile_size/2 +tile_size/3 + (tile_size/2)/4))
                                             )

                pygame.draw.rect(screen, "black", 
                                 pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                 1)
        
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    title_screen()


pygame.quit()