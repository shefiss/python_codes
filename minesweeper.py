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
difficulty = 2
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
            
        
    
    



def game():
    running = True
    grid = np.full((grid_size,grid_size), 0)
    
    first_guess_happend = False
    mouse_pressed_position = [0,0]
    numbers_font = pygame.font.SysFont(default_font, int(tile_size))
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        

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
                                    end_screen(grid, grid_size, numbers_font)
                                    running = False

                                #if something other is pressed
                                if grid[mouse_pressed_position[0],mouse_pressed_position[1]] != 9:
                                    check_tile(mouse_pressed_position, grid)

                        elif mouse_pressed_right() == True:
                            mouse_pressed_position = [j,i]
                            
                            if grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 0:
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 2
                                

                            elif grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] == 2:
                                grid_visible[mouse_pressed_position[0]][mouse_pressed_position[1]] = 0

                    if grid_visible[j][i] == 1:
                        pygame.draw.rect(screen, "white", 
                                         pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                         0)
                        if grid[j][i] != 0 and grid[j][i] != 9:
                            number = numbers_font.render(str(grid[j][i]), True, "black")
                            
                            screen.blit(number, (i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2))
                    
                    if grid_visible[j][i] == 2:
                        pygame.draw.rect(screen, "green", 
                                         pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                         0)
                    
                    pygame.draw.rect(screen, "black", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        1)
                        
        clock.tick(60)
        pygame.display.flip()



def end_screen(grid, grid_size, numbers_font):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if grid[j][i] == 9:
                    pygame.draw.rect(screen, "red", 
                                        pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                        0)    
                if grid[j][i] != 0 and grid[j][i] != 9:
                    number = numbers_font.render(str(grid[j][i]), True, "black")
                    screen.blit(number, (i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2))

                pygame.draw.rect(screen, "black", 
                                 pygame.Rect(i*tile_size +tile_size/2, j*tile_size + control_panel_size +tile_size/2, tile_size, tile_size), 
                                 1)
            
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    game()


pygame.quit()