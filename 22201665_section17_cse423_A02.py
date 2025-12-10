from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


# window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500

# Timing
last_time = time.time()
delta_time = 0

# Button areas (for click detection)
exit_btn_area = {'x': 220, 'y': 220, 'size': 20}
restart_btn_area = {'x': -220, 'y': 220, 'size': 20}
pause_btn_area = {'x': 0, 'y': 220, 'size': 20}



# Diamond properties
dmnd_clor = (1, 0, 0)  # Initial color red
dmnd_x = 0
dmnd_y = 220
dmd_speed = 80 
dmd_size = 15
dmd_toron = 5  



# Catcher properties
chr_x = 0
chr_y = -200
chr_width = 60
chr_sped = 200  
chr_height = 20
chr_colr = (1, 1, 1)



# finding zone of the line
def find_zone_of_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy > 0:
            return 3
        elif dx < 0 and dy <= 0:
            return 4
        else:  
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx <= 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  
            return 6

#convering the line zone to zone-0
def convert_to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

# zone conversion form converted zone to zone-0 back to original zone
def convert_to_original_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y



#this function draws a single pixel
def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()





# function to draw line in zone-0 using midpoint algorithm
def midpoint_line_zone0(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    
    points = []
    for x in range(int(x1), int(x2) + 1):
        points.append((x, y))
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
    
    return points




# line drawing function that handles all zones
def draw_line(x1, y1, x2, y2):
    # Handle case where endpoints are same
    if x1 == x2 and y1 == y2:
        draw_point(x1, y1)
        return
    zone = find_zone_of_line(x1, y1, x2, y2)
    # Convert to zone 0
    x1_z0, y1_z0 = convert_to_zone_0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone_0(x2, y2, zone)
    # Ensure x1 < x2 for zone 0
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    # Get points in zone 0
    points = midpoint_line_zone0(x1_z0, y1_z0, x2_z0, y2_z0)
    # Convert back and draw
    for px, py in points:
        orig_x, orig_y = convert_to_original_zone(px, py, zone)
        draw_point(orig_x, orig_y)




#Game Objects drawing functions
#draw catcher bowl, using midpoint lines
def draw_catcher(x, y, width, height, color):
    glColor3f(*color)
    half_w = width // 2
    # Draw bowl shape
    draw_line(int(x - half_w), int(y + height), int(x - half_w), int(y))
    draw_line(int(x - half_w), int(y), int(x + half_w), int(y))
    draw_line(int(x + half_w), int(y), int(x + half_w), int(y + height))
    draw_line(int(x - half_w), int(y + height), int(x + half_w), int(y + height))


#drawing the exit button
def draw_exit_btn_area(x, y, size):
    glColor3f(1, 0, 0)  # Red
    # Draw X
    draw_line(int(x - size), int(y + size), int(x + size), int(y - size))
    draw_line(int(x - size), int(y - size), int(x + size), int(y + size))




#left restart button drawing
def draw_restart_btn_area(x, y, size):
    glColor3f(0, 0.8, 0.8)  # Bright teal
    # Arrow pointing left
    draw_line(int(x + size), int(y + size), int(x), int(y))
    draw_line(int(x), int(y), int(x + size), int(y - size))
    draw_line(int(x), int(y), int(x+size*2), int(y))



#play or pause button drawing
def draw_pause_btn_area(x, y, size, is_paused):
    glColor3f(1, 0.75, 0)  # Amber
    if is_paused:
        # Draw play triangle
        draw_line(int(x - size//2), int(y + size), int(x + size//2), int(y))
        draw_line(int(x + size//2), int(y), int(x - size//2), int(y - size))
        draw_line(int(x - size//2), int(y - size), int(x - size//2), int(y + size))
    else:
        # Draw pause bars
        draw_line(int(x - size//2), int(y + size), int(x - size//2), int(y - size))
        draw_line(int(x + size//4), int(y + size), int(x + size//4), int(y - size))



#drawing diamond shape
def draw_diamond(x, y, size, color):
    glColor3f(*color)
    # Top triangle
    draw_line(int(x), int(y + size), int(x - size), int(y))
    draw_line(int(x), int(y + size), int(x + size), int(y))
    # Bottom triangle
    draw_line(int(x - size), int(y), int(x), int(y - size))
    draw_line(int(x + size), int(y), int(x), int(y - size))














# Game state
game_over = False
paused = False
cheat_mode = False
score = 0



# Collision Detection
def find_colition_btn_diamond_catcr(dmnd_x, dmnd_y, dmd_size, chr_x, chr_y, catcher_w, catcher_h):
    # Diamond bounding box
    d_left = dmnd_x - dmd_size
    d_right = dmnd_x + dmd_size
    d_top = dmnd_y + dmd_size
    d_bottom = dmnd_y - dmd_size
    # Catcher bounding box
    c_left = chr_x - catcher_w // 2
    c_right = chr_x + catcher_w // 2
    c_top = chr_y + catcher_h
    c_bottom = chr_y
    return (d_left < c_right and
            d_right > c_left and
            d_bottom < c_top and
            d_top > c_bottom)




# Input Handlers 
# mouse click handler
def mouse_listener(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert screen coordinates to OpenGL coordinates
        gl_x = x - WINDOW_WIDTH // 2
        gl_y = WINDOW_HEIGHT // 2 - y
        
        # Check restart button
        # Arrow spans from x to x+size*2 horizontally, and y-size to y+size vertically
        if (restart_btn_area['x'] <= gl_x <= restart_btn_area['x'] + restart_btn_area['size']*2) and \
        abs(gl_y - restart_btn_area['y']) < restart_btn_area['size']:
            reset_game()
                
        # Check pause button
        elif abs(gl_x - pause_btn_area['x']) < pause_btn_area['size'] and \
             abs(gl_y - pause_btn_area['y']) < pause_btn_area['size']:
            paused = not paused
            print(f"Game {'Paused' if paused else 'Resumed'}")
        
        # Check exit button
        elif abs(gl_x - exit_btn_area['x']) < exit_btn_area['size'] and \
             abs(gl_y - exit_btn_area['y']) < exit_btn_area['size']:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

# cheating mode toggle
def keyboard_listener(key, x, y):
    global cheat_mode
    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        print(f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")
    glutPostRedisplay()


#arrow key input handler
def special_key_listener(key, x, y):
    global chr_x
    if not game_over and not paused:
        move_amount = 10
        if key == GLUT_KEY_LEFT:
            chr_x -= move_amount
            # Keep catcher in bounds
            chr_x = max(-250 + chr_width//2, chr_x)
        elif key == GLUT_KEY_RIGHT:
            chr_x += move_amount
            chr_x = min(250 - chr_width//2, chr_x)
    glutPostRedisplay()




# Game Logic
# creating new diamond at random horizontal point
def creating_new_d_at_random_hr_point():
    global dmnd_x, dmnd_y, dmnd_clor
    dmnd_x = random.randint(-200, 200)
    dmnd_y = 220
    # Random bright color
    dmnd_clor = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

#resetign game to initial satate
def reset_game():
    global game_over, score, dmd_speed, chr_x, chr_colr, paused, cheat_mode
    game_over = False
    paused = False
    cheat_mode = False
    score = 0
    dmd_speed = 80
    chr_x = 0
    chr_colr = (1, 1, 1)
    creating_new_d_at_random_hr_point()
    print("Starting Over")


# Animation function
def animate():
    global dmnd_y, dmd_speed, score, game_over, chr_colr, last_time, delta_time, chr_x
    # Calculate delta time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    if not game_over and not paused:
        # Move diamond down
        dmnd_y -= dmd_speed * delta_time
        # Cheat mode: auto-move catcher
        if cheat_mode:
            if chr_x < dmnd_x:
                chr_x += chr_sped * delta_time
                if chr_x > dmnd_x:
                    chr_x = dmnd_x
            elif chr_x > dmnd_x:
                chr_x -= chr_sped * delta_time
                if chr_x < dmnd_x:
                    chr_x = dmnd_x
            # Keep in bounds
            chr_x = max(-250 + chr_width//2, min(250 - chr_width//2, chr_x))
        # Check collision
        if find_colition_btn_diamond_catcr(dmnd_x, dmnd_y, dmd_size, chr_x, chr_y, 
                          chr_width, chr_height):
            score += 1
            dmd_speed += dmd_toron
            print(f"Score: {score}")
            creating_new_d_at_random_hr_point()
        # Check if diamond missed (fell below catcher)
        elif dmnd_y < chr_y - dmd_size - 10:
            game_over = True
            chr_colr = (1, 0, 0)  # Turn red
            print(f"Game Over! Final Score: {score}")
    glutPostRedisplay()



# Display & Animation
#maing display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Draw buttons
    draw_restart_btn_area(restart_btn_area['x'], restart_btn_area['y'], restart_btn_area['size'])
    draw_pause_btn_area(pause_btn_area['x'], pause_btn_area['y'], pause_btn_area['size'], paused)
    draw_exit_btn_area(exit_btn_area['x'], exit_btn_area['y'], exit_btn_area['size'])
    
    # Draw game objects
    if not game_over:
        draw_diamond(dmnd_x, dmnd_y, dmd_size, dmnd_clor)
    
    draw_catcher(chr_x, chr_y, chr_width, chr_height, chr_colr)
    glutSwapBuffers()



# Projection setup
def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)

# Initialization the oppenGL settings
def init():
    glClearColor(0, 0, 0, 1)  # Black background
    glPointSize(2)
    setup_projection()
    creating_new_d_at_random_hr_point()


# Main Function
def main():
    global last_time
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    init()
    # Register callbacks
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    last_time = time.time()
    print("====== Catch the Diamonds ======")
    print("Welcome to the game!")
    print("How to Play:")
    print(" - Use LEFT and RIGHT arrow keys to move the catcher.")
    print(" - Press 'C' to turn Cheat Mode ON or OFF.")
    print(" - Click the buttons at the top to Restart, Pause/Play, or Exit.")
    print(" - Catch the falling diamonds to earn points.")
    print(" - If you miss a diamond, the game will end.")
    print("=================================")
    glutMainLoop()


if __name__ == "__main__":
    main()