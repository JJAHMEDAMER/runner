import pygame as pg
from sys import exit

def player_animation():
    global player, player_index
    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player = player_walk[int(player_index)]

WIDTH = 800
HEIGHT = 400
GAME_ACTIVE = False


pg.init()  # Initialize pygame 

# Clock 
clock = pg.time.Clock()

#Sound
jump_sound = pg.mixer.Sound("audio/jump.mp3")
jump_sound.set_volume(0.2)

# Setting Font
font = pg.font.Font("font/Pixeltype.ttf", 50) # Font Name, Font Size

# Create Window 
# Take a tuple as an argument for Width and height
screen = pg.display.set_mode((WIDTH, HEIGHT))  
pg.display.set_caption("Runner")

# Creating Surfaces
sky = pg.image.load("graphics/Sky.png").convert()  # Covert works with no transparent pixels
ground = pg.image.load("graphics/ground.png").convert()

end_screen_fill = pg.Surface((1000,750), pg.SRCALPHA)   # per-pixel alpha
end_screen_fill.fill((94,129,162,225))                         # notice the alpha value in the color


game_name = font.render("RUNNER", False, (111,196,169))  # Text, Aliasing, Color
game_name_rect = game_name.get_rect(midtop = (WIDTH/2,50))

press_space = font.render("Press Space to Start!", False, (111,196,169))
press_space_rect = press_space.get_rect(midbottom = (WIDTH/2 , HEIGHT-50))

# Snail
snail_1 = pg.image.load("graphics\snail\snail1.png").convert_alpha()  # Covert_alpha works with transparent pixels
snail_2 = pg.image.load("graphics\snail\snail2.png").convert_alpha()
snail_walk = [snail_1, snail_2]
snail_index = 0
snail = snail_walk[snail_index]
snail_rect = snail.get_rect(midbottom = (750, 300))


# Player
player_stand = pg.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand = pg.transform.rotozoom(player_stand,0,2)  # Surface, rotation, zoom
player_stand_rect = player_stand.get_rect(center = (WIDTH/2,HEIGHT/2))

player_walk_1 = pg.image.load("graphics\player\player_walk_1.png").convert_alpha()
player_walk_2 = pg.image.load("graphics\player\player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0

player_jump = pg.image.load("graphics\player\player_jump.png")

player = player_walk[player_index]
player_rect = player.get_rect(midbottom = (80,300))

# Timers

snail_timer = pg.USEREVENT + 1
pg.time.set_timer(snail_timer, 500)


gravity = 0

start_time = 0
time = 0

while True:    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()   
        
        if GAME_ACTIVE == False:
             # End Screen
            if event.type == pg.KEYDOWN:
                snail_rect.left = 800
                GAME_ACTIVE = True
                start_time = time
                
        else: 
            # Check For Space Key Down
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player_rect.bottom == 300:
                    gravity = -20
                    jump_sound.play()

            if event.type == snail_timer:
                if snail_index == 1 : snail_index = 0
                else: snail_index = 1
                snail = snail_walk[snail_index]

        
               

    if GAME_ACTIVE:
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        #screen.blit(game_name, game_name_rect)

        # Score
        time = int(pg.time.get_ticks()/1000) - start_time# gets time from start of pygame 
        score_surf = font.render( f"Score: {time}" , False, (64,64,64) )
        score_rect = score_surf.get_rect(midtop = (WIDTH/2,50))
        screen.blit(score_surf,score_rect)


        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300

        player_animation()
        screen.blit(player,player_rect)


        snail_rect.x -= 6  # Get X position
        if snail_rect.right <= 0 : snail_rect.left = WIDTH
        screen.blit(snail, snail_rect)

        if player_rect.colliderect(snail_rect):
            GAME_ACTIVE = False

        
    else:
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        screen.blit(end_screen_fill,(0,0))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(press_space,press_space_rect)
        if time == 0: screen.blit(game_name, game_name_rect)
        else: screen.blit(score_surf,score_rect)
        

    pg.display.update()
    clock.tick(60) # frame rate 