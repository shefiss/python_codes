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
grid_visible = np.full((grid_size,grid_size), 0) # this grid carries on the information if given tile is visible (1) or not (0), or if the tile has a flag (2)

# methods for mouse press
def mouse_pressed_left():
    global mouse_hold_left
    if pygame.mouse.get_pressed()[0] == True and mouse_hold_left == False: # this checks if the mouse is pressed
        mouse_hold_left = True
        return True
    elif pygame.mouse.get_pressed()[0] == True and mouse_hold_left == True: # this checks if the mouse is pressed for more than one tick, if yes, it will turn statement False, so the game doesn't recognise more than one mouse press
        return False
    elif pygame.mouse.get_pressed()[0] == False and mouse_hold_left == True: # this checks if the mouse is not pressed
        mouse_hold_left = False
        return False
    else:
        return False

# the same method but for the right button
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

# unifying the text rendering
def draw_text(string, size, color):
    font = pygame.font.SysFont(default_font, int(size))
    return font.render(string, True, color)


def calculate_grid(mouse_pressed_position, grid):
    
    for i in range(0,grid_size*difficulty):
        tile_item = 9 # tile_item is set on 9 (the mine) so the while cycle will happend at least once
        tile_x = mouse_pressed_position[0] # tile_x and y is set on mouse position for the same reason as before
        tile_y = mouse_pressed_position[1]

        # this while cyclus makes sure that the mine wont spawn on the tile where the mouse is, and in 8 tiles around (i.e. the first click will always land on 0)
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

    # this cyclus sets up the numbers in the grid
    for i in range(0, grid_size):
        for j in range(0,grid_size):
            if grid[i][j] == 9: # if cyclus lands on mine
                continue
            else:
                mines_around = 0
                for k in range(i-1, i+2): # cyclus that checks 8 tiles around the i,j tile
                    for l in range(j-1, j+2):
                        if k >= grid_size or k < 0 or l >= grid_size or l < 0: #checks if the k,l tile is not out of bounds
                            continue

                        if grid[k][l] == 9:
                            mines_around += 1

                        

                grid[i][j] = mines_around # adds the number of mines around the i,j tile

    return grid


# method that checks tile that was clicked on
def check_tile(mouse_pressed_position, grid):
    global grid_visible
    mouse_x = mouse_pressed_position[0]
    mouse_y = mouse_pressed_position[1]
    if grid_visible[mouse_x, mouse_y] == 0:
        grid_visible[mouse_x, mouse_y] = 1


    

    # if player clicked on 0, it will reveal the whole island
    field = np.array([[mouse_x,mouse_y]]) # field work as a memory for the while cyclus of all unrevealed zero tiles
    index = 0
    if grid[mouse_x][mouse_y] == 0:
        while field.size != 0: # while cyclus revealing zero tiles and number tiles around the zero island
            x = field[index,0]
            y = field[index,1]
            
            if grid[x][y] == 0:
                
                # if prompts adding zero tiles into field (memory)
                if x+1 < grid_size and grid_visible[x+1][y] == 0: # checks if the next tile is not out of bounds and if it wasn't already revealed
                    field = np.append(field, [[x+1,y]], 0)

                if x-1 >= 0 and grid_visible[x-1][y] == 0:
                    field = np.append(field, [[x-1,y]], 0)

                if y+1 < grid_size and grid_visible[x][y+1] == 0:
                    field = np.append(field, [[x,y+1]], 0)

                if y-1 >= 0 and grid_visible[x][y-1] == 0:
                    field = np.append(field, [[x,y-1]], 0)
                """

                if x+1 < grid_size and y+1 < grid_size and grid_visible[x+1][y+1] == 0:
                    field = np.append(field, [[x+1,y+1]], 0)

                if x+1 < grid_size and y-1 >= 0 and grid_visible[x-1][y-1] == 0:
                    field = np.append(field, [[x-1,y-1]], 0)

                if x-1 >= 0 and y+1 < grid_size and grid_visible[x-1][y+1] == 0:
                    field = np.append(field, [[x-1,y+1]], 0)

                if x-1 >= 0 and y-1 >= 0 and grid_visible[x-1][y-1] == 0:
                    field = np.append(field, [[x-1,y-1]], 0)
                """      
                
            if grid_visible[x,y] == 0: # tile reveal
                grid_visible[x,y] = 1
            field = np.delete(field, index, 0) # deleting proccessed tile from field (memory)
            
        
def title_screen():
    running = True
    # start button pos
    start_x = screen_width/4 + screen_width/12
    start_y = screen_height/8 + screen_height/2
    # difficulty label pos
    difficulty_label_x = screen_width/4 + screen_width/14
    difficulty_label_y = screen_height/8
    # size label pos
    grid_size_x = screen_width/4 + screen_width/7
    grid_size_y = screen_height/8 + screen_height/4
    # position of set of difficulty buttons
    difficulty_buttons_x = difficulty_label_x+10
    difficulty_buttons_y = difficulty_label_y + 40
    # position of set of size buttons
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

        # setup of difficulty and size labels
        difficulty_label = draw_text("Difficulty:", 30, "black")
        screen.blit(difficulty_label, (difficulty_label_x, difficulty_label_y))
        size_label = draw_text("Size:", 30, "black")
        screen.blit(size_label, (grid_size_x, grid_size_y))

        # setup of buttons (all are the same, in both buttons sets)
        if difficulty == 1:
            text = draw_text("1", 40, "white") #if difficulty is set on 1, it will show as white text on black background
            pygame.draw.rect(screen, "black", [difficulty_buttons_x,difficulty_buttons_y,50,50]) # first button is drawn on the set coridnates, the rest are based on the first one
            screen.blit(text, (difficulty_buttons_x+15, difficulty_buttons_y+5))
        else:
            if (difficulty_buttons_x <= mouse_pos[0] <= difficulty_buttons_x +50 
                and difficulty_buttons_y <= mouse_pos[1] <= difficulty_buttons_y + 50
                and grid_size < 14): # if the difficulty is not set on 1 but the mouse is hovering, the background will turn gray
                text = draw_text("1", 40, "black")
                pygame.draw.rect(screen, "lightgray", [difficulty_buttons_x,difficulty_buttons_y,50,50])
                screen.blit(text, (difficulty_buttons_x+15, difficulty_buttons_y+5))
                if mouse_pressed_left() == True:
                    difficulty = 1
            else: # else it will be in idle state
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

        # sizes: 7, 11, 14, 19 (sizes might be wierd, but it is because the grid starts at 
        # x = tile_size/2 and ends tile_size/2 from the end, this way it has +1 tiles on screen,
        # so this means 7 actually makes tile's size screen_width/8)

        # because the number of mines is grid_size*difficulty, the number of tiles is grid_size*grid_size,
        # this way if you chosen grid size 19 and difficulty 1, it would place 19 mines on 361 tiles and the zero island
        # calculation would take very long, so when player chooses bigger grid it will force him into bigger difficulty level
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

        # start button set up
        if start_x <= mouse_pos[0] <= start_x +180 and start_y <= mouse_pos[1] <= start_y + 60:
            text = draw_text("START", 60, "white")
            pygame.draw.rect(screen, "black", [start_x,start_y,180,60])
            screen.blit(text, (start_x, start_y))
            if mouse_pressed_left() == True:
                tile_size = field_size/(grid_size + 1) # calculates tile size by given inputs
                grid_visible = np.full((grid_size,grid_size), 0) # calculates grid_visible size by given inputs
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

    flags_num = grid_size*difficulty # number of flags that you can use is the same as how many mines are in the game
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
        # drawing the flag icon
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
        

        # drawing the stop watch
        pygame.draw.line(screen, "red", (timer_x +30, timer_y +10), (timer_x +30, timer_y +30), 4)
        pygame.draw.line(screen, "gray", (timer_x +30, timer_y +30), (timer_x +50, timer_y +30), 4)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 30, 6)
        pygame.draw.circle(screen,"black",(timer_x +30, timer_y +30), 6, 6)
        timer_text = draw_text("=" + str(timer), 50, "black")
        screen.blit(timer_text, (timer_x+70, timer_y+5))

        # rendering the new game button
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
        if first_guess_happend == False: # the grid is rendered after the first guess happend, so the first click will never land on mine
            mouse_pos = pygame.mouse.get_pos()
            
            for i in range(0,grid_size):
                for j in range(0,grid_size):

                    pygame.draw.rect(screen, "lightgray", 
                                     pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                     0) # default color of the grid

                    if (int((mouse_pos[0]-tile_size/2)/tile_size), int((mouse_pos[1]-control_panel_size-tile_size/2)/tile_size)) == (i,j):
                        pygame.draw.rect(screen, "gray", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        0) # tile where is mouse hovering over will change color to gray
                        
                        if mouse_pressed_left() == True:
                            mouse_pressed_position = [j,i]
                            grid = calculate_grid(mouse_pressed_position, grid) # when the first guess happend the grid is calculated
                            first_guess_happend = True
                            check_tile(mouse_pressed_position, grid) # makes the first click reveal the first tiles
                            
                                
                        
                    
                    pygame.draw.rect(screen, "black", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        1) # drawing the edges of tiles
                    
        if first_guess_happend == True: # after the first guess happend the true game loop starts
            mouse_pos = pygame.mouse.get_pos()

            for i in range(0,grid_size): # for cycles i and j are scanning through all tiles of the grid
                for j in range(0,grid_size):
                    
                    pygame.draw.rect(screen, "lightgray", 
                                     pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                     0)

                    # if mouse is hovering over a tile, it will change color to gray
                    if (int((mouse_pos[0]-tile_size/2)/tile_size), int((mouse_pos[1]-control_panel_size-tile_size/2)/tile_size)) == (i,j):
                        pygame.draw.rect(screen, "gray", 
                                            pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                            0)
                        

                        if mouse_pressed_left() == True:
                            mouse_pressed_position = [j,i]
                            
                            if grid_visible[mouse_pressed_position[0],mouse_pressed_position[1]] != 2: # first it checks if the tile has a flag
                                if grid[mouse_pressed_position[0],mouse_pressed_position[1]] == 9: # if player clicks on a mine, it will end
                                    end_screen(grid, grid_size, timer, flags_num)
                                    running = False

                                #if something other is pressed
                                if grid[mouse_pressed_position[0],mouse_pressed_position[1]] != 9: # if player doesnt click on a mine it will run a tile check
                                    check_tile(mouse_pressed_position, grid)

                        # placing flags
                        elif mouse_pressed_right() == True:
                            mouse_pressed_position = [j,i]
                            
                            if (grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 0
                                and flags_num > 0): # checking if the tile has a flag, if not it will place one
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 2 # place flag means turning a visibility settings to 2
                                flags_num -= 1
                                

                            elif grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 2:
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 0 # if the tile already as a flag it wil remove it, changing from 2 to 0
                                flags_num += 1
                            # if the tile is already visible player cannot place a flag (understandably)
                            
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

        searched_tiles = 0
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if grid_visible[i][j] != 0:
                    searched_tiles += 1

        if searched_tiles == grid_size*grid_size:
            end_screen(grid, grid_size, timer, flags_num)

        if dt == 45:
            timer += 1
            dt = 0

        dt += 1      
        clock.tick(60)
        pygame.display.flip()



def end_screen(grid, grid_size, timer, flags_num): # whole end screen is 1 to 1 the same as the game, the only difference is that you cannot play
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