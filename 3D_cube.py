import pygame
import numpy
from numpy.linalg import inv

#to move the cube use numbers 1, 2, 3 to switch between axis and the left and right arrows to rotate

pygame.init()

screen_width = 600
screen_height = 600

# axes: x = 1,0,0 ; y = 0,1,0 ; z = 0,0,1
# here I use Least squares method (aka A(T)*A*x=A(T)*b, where A is the vector matrix of the screen, A(T) is the transponated metrix, x is a vector projected on the screen, and b is the original vector)
image_screen_matix = numpy.matrix([[1,0], [0,0], [0,1]]) # matrix of vectors of the screen
trasponated_image_matrix = numpy.matrix_transpose(image_screen_matix) # A(T)
transA_times_A = numpy.matmul(trasponated_image_matrix, image_screen_matix) # A(T)*A
inverse_matrix = inv(transA_times_A) # inverse matrix of A(T)*A to express x


side_a = 200 # size of the side of the cube
half_side_a = side_a/2

center_point = numpy.array([300,300,300])

xyz_switch = 1 # switch between axis used later

# axis of the cube, rotated along the cube
cube_axis_x = numpy.array([1,0,0])
cube_axis_y = numpy.array([0,1,0])
cube_axis_z = numpy.array([0,0,1])

rotation_speed_rad = 0.17
cos_sp_left = numpy.cos(rotation_speed_rad)
sin_sp_left = numpy.sin(rotation_speed_rad)

# rotation matrices around xyz axis
Rx_left_mat = numpy.matrix([[1,0,0],[0,cos_sp_left,-sin_sp_left],[0,sin_sp_left,cos_sp_left]])
Rx_right_mat = inv(Rx_left_mat)

Ry_left_mat = numpy.matrix([[cos_sp_left,0,sin_sp_left],[0,1,0],[-sin_sp_left, 0, cos_sp_left]])
Ry_right_mat = inv(Ry_left_mat)

Rz_left_mat = numpy.matrix([[cos_sp_left,-sin_sp_left,0],[sin_sp_left,cos_sp_left,0],[0,0,1]])
Rz_right_mat = inv(Rz_left_mat)


screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def calculate_point(cube_axis, def_point): # def_point = point from which is the new point calculated, cube_axis = the axis along which the point is moved
    cal = numpy.array([cube_axis.item(0)*side_a + def_point[0],cube_axis.item(1)*side_a + def_point[1],cube_axis.item(2)*side_a + def_point[2]])
    return cal

def move_point(cal_point): # the point is calculated with the center point in [0,0,0], so it has to be moved to the right position
    point = numpy.array([cal_point[0]+center_point[0], cal_point[1]+center_point[1], cal_point[2]+center_point[2]]) # it's moved by the distance of [0,0,0] and the center point
    return point

def least_square_cal(point, screen_points, color): # calculating least square method using precalculated equation done before
    point = numpy.matmul(numpy.matmul(trasponated_image_matrix, point), inverse_matrix) # point = A(T)*b*inv(A(T)*A)
    screen_points.append([point.item(0), point.item(1)])
    pygame.draw.circle(screen, color, (point.item(0), point.item(1)), 5)

def rotation(rotation_matrix): # rotating with given rotation matrix
    global cube_axis_x, cube_axis_y, cube_axis_z
    cube_axis_x = numpy.matmul(rotation_matrix, cube_axis_x)
    cube_axis_y = numpy.matmul(rotation_matrix, cube_axis_y)
    cube_axis_z = numpy.matmul(rotation_matrix, cube_axis_z)

def projection():

    global cube_axis_x, cube_axis_y, cube_axis_z, xyz_switch

    # text to explain controls
    font = pygame.font.SysFont("monospace", 15)
    controls_part1 = font.render("controls: to move the cube use numbers 1, 2, 3 to switch ", True, "white")
    controls_part2 = font.render("between axis and the left and right arrows to rotate", True, "white")


    running = True
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        
        
        #controls
        key = pygame.key.get_pressed()
        #cube axis switch
        if key[pygame.K_1]:
            xyz_switch = 1
        elif key[pygame.K_2]:
            xyz_switch = 2
        elif key[pygame.K_3]:
            xyz_switch = 3

        # not sure why it "changes formats" but when you multiply array by matrix, the array will get in some kind of matrix format, so here I change it back
        cube_axis_x = numpy.array([cube_axis_x.item(0), cube_axis_x.item(1), cube_axis_x.item(2)])
        cube_axis_y = numpy.array([cube_axis_y.item(0), cube_axis_y.item(1), cube_axis_y.item(2)])
        cube_axis_z = numpy.array([cube_axis_z.item(0), cube_axis_z.item(1), cube_axis_z.item(2)])

        # rotation around axis
        if xyz_switch == 1:
            if key[pygame.K_RIGHT]:
                rotation(Rx_left_mat)
            if key[pygame.K_LEFT]:
                rotation(Rx_right_mat)

        if xyz_switch == 2:
            if key[pygame.K_RIGHT]:
                rotation(Ry_left_mat)
            if key[pygame.K_LEFT]:
                rotation(Ry_right_mat)

        if xyz_switch == 3:
            if key[pygame.K_RIGHT]:
                rotation(Rz_left_mat)
            if key[pygame.K_LEFT]:
                rotation(Rz_right_mat)

        # cal for calculated, because it has center at [0,0,0] so it's not the final point position
        # calA is derived from the "center" (aka [0,0,0]) so it has to be moved along all three axis
        calA = numpy.array([-cube_axis_x.item(0)*half_side_a -cube_axis_y.item(0)*half_side_a -cube_axis_z.item(0)*half_side_a, 
                            -cube_axis_x.item(1)*half_side_a -cube_axis_y.item(1)*half_side_a -cube_axis_z.item(1)*half_side_a, 
                            -cube_axis_x.item(2)*half_side_a -cube_axis_y.item(2)*half_side_a -cube_axis_z.item(2)*half_side_a])
        
        # the rest of the cal points are derived one way or another from the calA
        calB = calculate_point(cube_axis_x, calA)
        calC = calculate_point(cube_axis_y, calB)
        calD = calculate_point(cube_axis_y, calA)
        calE = calculate_point(cube_axis_z, calA)
        calF = calculate_point(cube_axis_z, calB)
        calG = calculate_point(cube_axis_z, calC)
        calH = calculate_point(cube_axis_z, calD)

        # moving the points from the calculated area to the final destinantion, where the point should be
        A = move_point(calA)
        B = move_point(calB)
        C = move_point(calC)
        D = move_point(calD)
        E = move_point(calE)
        F = move_point(calF)
        G = move_point(calG)
        H = move_point(calH)
        
        points_arr = [A, B, C, D, E, F, G ,H] # array of the 3D locations of the points
        screen_points = [] # 2D array of the points projections on the screen


        screen.fill("black")

        # calculating least square method for each point
        for i in points_arr:
            least_square_cal(i, screen_points, "white")

        least_square_cal(center_point, screen_points, "red") # calculating and drawing of the center point

        # drawing the sides of the cube
        pygame.draw.polygon(screen, "blue", [screen_points[0], screen_points[1], screen_points[2], screen_points[3]], 1)
        pygame.draw.polygon(screen, "blue", [screen_points[0], screen_points[1], screen_points[5], screen_points[4]], 1)
        pygame.draw.polygon(screen, "blue", [screen_points[0], screen_points[3], screen_points[7], screen_points[4]], 1)
        pygame.draw.polygon(screen, "blue", [screen_points[1], screen_points[2], screen_points[6], screen_points[5]], 1)
        pygame.draw.polygon(screen, "blue", [screen_points[2], screen_points[3], screen_points[7], screen_points[6]], 1)
        pygame.draw.polygon(screen, "blue", [screen_points[4], screen_points[5], screen_points[6], screen_points[7]], 1)

        screen.blit(controls_part1, (5,10)) # rendering the label with controls
        screen.blit(controls_part2, (5,30))

        pygame.display.flip()
        clock.tick(24)

        


if __name__ == "__main__":
    projection()

pygame.quit()