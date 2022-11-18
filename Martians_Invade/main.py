# The Martians Invade! game
# Richard North 28/03/2021
import pygame
import math
import sys
from os import path
import some_basic_functions
import game_classes

pygame.init()


image_dir = path.join(path.dirname(__file__), "new images")
sound_dir = path.join(path.dirname(__file__), 'sounds')
'''
Loading the sound effects/ background music
'''
laser_fire = pygame.mixer.Sound(path.join(sound_dir, "laser_fire_2.wav"))
pygame.mixer.music.load(path.join(sound_dir, "music_1.mp3"))
pygame.mixer.music.play(-1)  # music will be played on a loop
pygame.mixer.music.set_volume(0.025)  # setting the volume of the music

# windowing
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Martians Invade")

# loading the image used for the icon  new images
icon = pygame.image.load(path.join(image_dir, "alien.png"))
pygame.display.set_icon(icon)  # setting the icon image

# setting the speed of the game
FPS = 60
CLOCK = pygame.time.Clock()

# changing the cursor to a crosshair
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

# importing the background image to the programme
background = pygame.image.load(path.join(image_dir, "Martian_background_3.png")).convert()

# scaling the image the size of the window
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background.get_rect()

# base amount of enemies
Base_amount_of_enemies = 18

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_YELLOW = (150, 150, 0)
LIGHT_YELLOW = (255, 255, 0)
LIGHT_BLUE = (200, 255, 255)


def main():
    # initialising variables
    # Boolean variables
    Game_on = True
    Spawning = True
    Level_complete = False
    Blast_back_active = False

    # Setting some basic attributes of the player
    PLAYER_WIDTH = 60
    PLAYER_HEIGHT = 90
    Player_x = SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2
    Player_y = SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2

    # setting some basic attributes of the aliens
    ALIEN_WIDTH = 50
    ALIEN_HEIGHT = 50
    ALIEN_HEALTH = 1
    ALIEN_POWER = 1

    # setting some basic attributes of boss aliens
    BOSS_ALIEN_HEIGHT = 100
    BOSS_ALIEN_WIDTH = 100
    BOSS_HEALTH = 30
    BOSS_POWER = 3
    A_BOSS = True

    # used as a base amount of enemies that will then be multiplied by the level
    Amount_to_spawn = Base_amount_of_enemies
    Amount_of_enemies_alive = Amount_to_spawn
    Level = 1

    # counters that will be used to delay certain aspects for a given length of time
    Level_delay_counter = 1
    spawn_delay = 0
    blast_back_counter = 1

    # creating groups for all of the sprites
    All_sprites = pygame.sprite.Group()
    Player_sprite = pygame.sprite.Group()
    Enemy_sprites = pygame.sprite.Group()
    Bullets = pygame.sprite.Group()


    '''
    loading the player images
    '''
    # loading the images used for the player
    player_assets = ["spaceman_1.png", "spaceman_2.png", "spaceman_3.png",\
        "spaceman_4.png", "spaceman_5.png", "spaceman_6.png",\
            "spaceman_7.png", "spaceman_8.png"]
    # creating a list of images for the player
    player_walking = []
    for name in player_assets:
        player_walking.append(pygame.image.load(path.join(image_dir, name)).convert())

    # loading the image used for the players bullets
    bullet_image = pygame.image.load(path.join(image_dir, "Bullet_1.png")).convert()
    bullet_image = pygame.transform.rotate(bullet_image, 90)

    # loading all the health bar images
    health_assets = ["health_0.png", "health_20.png", "health_40.png",\
        "health_60.png", "health_80.png", "health_100.png"]
    # creating a list of the health bar states
    health_bar = []
    for name in health_assets:
        health_bar.append(pygame.image.load(path.join(image_dir, name)).convert())

    '''
    loading the enemy alien images
    '''
    alien_assets = ["Alien_1.png", "Alien_2.png", "Alien_3.png", "Alien_4.png",\
        "Alien_5.png", "Alien_6.png", "Alien_7.png", "Alien_8.png", "Alien_9.png",\
            "Alien_10.png", "Alien_11.png", "Alien_12.png", "Alien_13.png",\
                 "Alien_14.png", "Alien_15.png", "Alien_16.png", "Alien_17.png",\
                      "Alien_18.png"]
    alien_images = []
    for name in alien_assets:
        alien_images.append(pygame.image.load(path.join(image_dir, name)).convert())

    boss_alien_images = []
    for alien in alien_images:
        boss_alien_images.append(pygame.transform.scale\
            (alien, (BOSS_ALIEN_WIDTH, BOSS_ALIEN_HEIGHT)))

    def paused():
        Pause = True
        while Pause:
            CLOCK.tick(FPS)
            for event in pygame.event.get():
                # checking to see if the player closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # if the player quits the Pause while loop is set false
                    Pause = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Pause = False

            WINDOW.fill(BLACK)
            WINDOW.blit(background, background_rect)
            some_basic_functions.display_text(WINDOW, SCREEN_WIDTH / 2 - 90,\
                100, 50, "PAUSED", BLACK)
            some_basic_functions.display_text(WINDOW, SCREEN_WIDTH / 2 - 340,\
                0, 80, "The Martians Invade!", BLACK)
            some_basic_functions.display_text(WINDOW, SCREEN_WIDTH - 220, 0,\
                28, "Current Score: {}".format(player.score), BLACK)
            
            resume_clicked = some_basic_functions.create_button(WINDOW, \
                SCREEN_WIDTH/2 - 125, 200, 200, 50, LIGHT_YELLOW, DARK_YELLOW,\
                    30, BLACK, "Resume")
            if resume_clicked:
                Pause = False
                
            restart_clicked = some_basic_functions.create_button(WINDOW, \
                SCREEN_WIDTH/2 - 125, 300, 200, 50, LIGHT_YELLOW, DARK_YELLOW,\
                    30, BLACK, "Restart")
            if restart_clicked:
                main()
            main_menu_clicked = some_basic_functions.create_button(WINDOW, \
                SCREEN_WIDTH/2 - 125, 400, 200, 50, LIGHT_YELLOW, DARK_YELLOW,\
                    30, BLACK, "Main menu")
            if main_menu_clicked:
                menu()

            pygame.display.update()
        

    player = game_classes.SpaceMan(Player_x, Player_y, PLAYER_WIDTH, PLAYER_HEIGHT,\
        SCREEN_WIDTH, SCREEN_HEIGHT, player_walking)
    All_sprites.add(player)
    Player_sprite.add(player)

    while Game_on:
        CLOCK.tick(FPS)
        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)

        if player.health <= 0:
            game_over(player.score)

        for event in pygame.event.get():
            # checking to see if the player closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the Game_on while loop is set false
                Game_on = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullet = player.fire(bullet_image)
                    All_sprites.add(bullet)
                    Bullets.add(bullet)
                    laser_fire.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused()

        '''
        spawning enemies
        '''

        if Spawning:
            if Amount_to_spawn > 0:
                spawn_delay += 1
                if spawn_delay % (FPS / 2) == 0:
                    if Level >= 7 and Amount_to_spawn % 40 == 0:
                        boss_enemy = game_classes.Aliens(BOSS_ALIEN_WIDTH, BOSS_ALIEN_HEIGHT,\
                            SCREEN_WIDTH, SCREEN_HEIGHT, boss_alien_images, Level, A_BOSS,\
                                BOSS_HEALTH, BOSS_POWER)

                        All_sprites.add(boss_enemy)
                        Enemy_sprites.add(boss_enemy)
                        Amount_to_spawn -= 1
                    else:
                        enemy = game_classes.Aliens(ALIEN_WIDTH, ALIEN_HEIGHT, SCREEN_WIDTH,\
                            SCREEN_HEIGHT, alien_images, Level, not A_BOSS, ALIEN_HEALTH,\
                                ALIEN_POWER)

                        All_sprites.add(enemy)
                        Enemy_sprites.add(enemy)
                        Amount_to_spawn -= 1
                    spawn_delay = 0
            else:
                Spawning = False


        '''
        collisions
        '''
        # checking if the enemies are hit
        hits = pygame.sprite.groupcollide(Enemy_sprites, Bullets, False, True)
        for hit in hits:
            hit.health -= 1
            if hit.health == 0:
                if hit.is_a_boss:
                    player.score += 10 * Level
                else:
                    player.score += 1 * Level
                player.enemies_killed += 1
                hit.kill()

        # dealing with collisions between the player and the enemies
        if not Blast_back_active:
            hits = pygame.sprite.spritecollide(player, Enemy_sprites, False,\
                pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= hit.power
                Blast_back_active = True
                blast_center = player.rect.center

        # the blast back variables are being used to knock the enemies back once the player has been hit
        if Blast_back_active:
            blast_back_counter += 1
            pygame.draw.circle(WINDOW, LIGHT_BLUE, blast_center, blast_back_counter * 4, 8)
            if blast_back_counter % 180 == 0:
                blast_back_counter = 0
                Blast_back_active = False

        '''
        updating the values once the player has killed all enemies
        '''

        if Amount_of_enemies_alive - player.enemies_killed == 0:
            Level_complete = True
            if Level_delay_counter % (FPS * 5) == 0:
                Level += 1
                Spawning = True
                player.enemies_killed = 0
                Amount_to_spawn = Base_amount_of_enemies * Level
                Amount_of_enemies_alive = Amount_to_spawn
                Level_complete = False
            Level_delay_counter += 1

        '''
        updating/drawing everything on screen
        '''

        Player_sprite.update()
        Enemy_sprites.update(player.rect.center, Blast_back_active)
        Bullets.update()
        Enemy_sprites.draw(WINDOW)
        Bullets.draw(WINDOW)

        if Blast_back_active:
            if blast_back_counter % (FPS / 6) == 0:
                Player_sprite.draw(WINDOW)
        else:
            Player_sprite.draw(WINDOW)

        if Level_complete:
            some_basic_functions.display_completion(WINDOW, Level, SCREEN_WIDTH, SCREEN_HEIGHT)

        some_basic_functions.display_score(WINDOW, player.score, SCREEN_WIDTH)
        some_basic_functions.display_level(WINDOW, Level, SCREEN_WIDTH)
        some_basic_functions.display_text(WINDOW, SCREEN_WIDTH / 2 + 150, 0, 36,\
            "Enemies left alive: {}".format(Amount_of_enemies_alive - player.enemies_killed), BLACK)
        # displaying the players health bar on screen for them to see
        WINDOW.blit(health_bar[player.health], (10, 0))
        pygame.display.update()


def menu():
    # Initialising variables
    running = True

    # importing the enemy image
    alien_image_1 = pygame.image.load(path.join(image_dir, "Alien_2.png")).convert()
    alien_image_1 = pygame.transform.scale(alien_image_1, (60, 60))
    alien_image_1.set_colorkey(BLACK)
    alien_image_2 = pygame.transform.rotate(alien_image_1, 30)
    alien_image_3 = pygame.transform.rotate(alien_image_1, -30)

    # importing the player image
    player_image_1 = pygame.image.load(path.join(image_dir, "spaceman_1.png")).convert()
    player_image_1.set_colorkey(BLACK)
    player_image_1 = pygame.transform.rotate(player_image_1, 90)

    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # checking to see if the player closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the running while loop is set false
                running = False
                sys.exit()

        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)

        new_game_clicked = some_basic_functions.create_button(WINDOW, 50,\
            SCREEN_HEIGHT / 2 - 50, 200, 50, LIGHT_YELLOW, DARK_YELLOW,\
                30, BLACK, "New Game")
        if new_game_clicked:
            main()

        how_to_clicked = some_basic_functions.create_button(WINDOW, 380,\
            SCREEN_HEIGHT/2 - 50, 200, 50, LIGHT_YELLOW, DARK_YELLOW,\
                30, BLACK, "How to play")
        if how_to_clicked:
            how_to_play()
            
        high_scores_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH - 580, SCREEN_HEIGHT/2 - 50, 200, 50, LIGHT_YELLOW,\
                DARK_YELLOW, 30, BLACK, "High Scores")
        if high_scores_clicked:
            leaderboeards()
        settings_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH - 250, SCREEN_HEIGHT/2 - 50, 200, 50, LIGHT_YELLOW,\
                DARK_YELLOW, 30, BLACK, "Settings")
        if settings_clicked:
            settings()

        some_basic_functions.display_text(WINDOW, 350, 5, 80, "The Martians Invade!", BLACK)
        WINDOW.blit(alien_image_1, (SCREEN_WIDTH/2, 100))#looking down
        WINDOW.blit(alien_image_2, (300, 100))#looking bottom right
        WINDOW.blit(alien_image_3, (1000,100))#looking bottom left
        WINDOW.blit(player_image_1, (500,500))
        pygame.display.update()



def how_to_play():
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # checking to see if the player closes the window 
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the running while loop is set false 
                running = False
                sys.exit()

        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)
        some_basic_functions.display_text(WINDOW, 350, 5, 80,\
            "The Martians Invade!", BLACK)
        some_basic_functions.display_text(WINDOW, 570, 100, 40,\
            "How to play", BLACK)
        some_basic_functions.display_text(WINDOW, 400, 150, 40,\
            "To move up select and hold the W key", BLACK)
        some_basic_functions.display_text(WINDOW, 380, 200, 40,\
            "To move down select and hold the S key", BLACK)
        some_basic_functions.display_text(WINDOW, 400, 250, 40,\
            "To go left select and hold the A key", BLACK)
        some_basic_functions.display_text(WINDOW, 400, 300, 40,\
            "To go right select and hold the D key", BLACK)
        some_basic_functions.display_text(WINDOW, 100, 350, 40,\
            "To shoot click your mouse and the bullet will go in the direction of your cursor", BLACK)
        some_basic_functions.display_text(WINDOW, 520, 400, 40,\
            "Objective of game", BLACK)
        some_basic_functions.display_text(WINDOW, 25, 450, 40,\
            "To shoot and kill as many aliens as possible without getting caught - Save the human race!", BLACK)

        #create_button(x, y, width, height, light_colour, dark_colour, font_size, font_colour, text)
        main_menu_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 150, 200, 50, LIGHT_YELLOW,\
                DARK_YELLOW, 30, BLACK, "Main menu")
        if main_menu_clicked:
            menu()

        #create_button(x, y, width, height, colour, font_size, font_colour)
        pygame.display.update()


def leaderboeards():
    running = True
    
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # checking to see if the player closes the window 
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the running while loop is set false 
                running = False
                sys.exit()

        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)
        some_basic_functions.draw_leaderboard(WINDOW, SCREEN_WIDTH, SCREEN_HEIGHT)
        some_basic_functions.display_text(WINDOW, 350, 5, 80, \
            "The Martians Invade!", BLACK)

        main_menu_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 150, 200, 50,\
                LIGHT_YELLOW, DARK_YELLOW, 30, BLACK, "Main menu")
        if main_menu_clicked:
            menu()

        pygame.display.update()

def settings():
    running = True
    
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # checking to see if the player closes the window 
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the running while loop is set false 
                running = False
                sys.exit()

        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)
        
        some_basic_functions.display_text(WINDOW, 350, 5, 80, \
            "The Martians Invade!", BLACK)

        some_basic_functions.display_text(WINDOW, 410, SCREEN_HEIGHT/2, 60, \
            "Sorry im not ready yet!", BLACK)

        main_menu_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 150, 200, 50,\
                LIGHT_YELLOW, DARK_YELLOW, 30, BLACK, "Main menu")
        if main_menu_clicked:
            menu()

        pygame.display.update()



def game_over(player_score):
    # Initialising variables
    running = True
    text_box_clicked = False
    data_submitted = False

    # importing the enemy image
    alien_image_1 = pygame.image.load(path.join(image_dir, "Alien_2.png")).convert()
    alien_image_1 = pygame.transform.scale(alien_image_1,(60,60))
    alien_image_1.set_colorkey(BLACK)
    alien_image_2 = pygame.transform.rotate(alien_image_1,30)
    alien_image_3 = pygame.transform.rotate(alien_image_1,-30)
    alien_image_4 = pygame.transform.rotate(alien_image_1,150)
    alien_image_5 = pygame.transform.rotate(alien_image_1,180)
    alien_image_6 = pygame.transform.rotate(alien_image_1,-150)
    alien_image_7 = pygame.transform.rotate(alien_image_1,90)
    alien_image_8 = pygame.transform.rotate(alien_image_1,-90)

    # importing the player image
    player_image_1 = pygame.image.load(path.join(image_dir, "spaceman_1.png")).convert()
    player_image_1.set_colorkey(BLACK)
    player_image_1 = pygame.transform.rotate(player_image_1,90)
    health_at_0 = pygame.image.load(path.join(image_dir, "health_0.png")).convert()

    excepted_values = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G",\
        "h","H","i","I","j","J","k","K","l","L","m","M","n","N","o","O","p","P",\
            "q","Q","r","R","s","S","t","T","u","U","v","V","w","W","x","X","y",\
                "Y","z","Z"," "]
    player_name = ""
    scores = some_basic_functions.read_and_convert_scores()

    while running:
        CLOCK.tick(FPS)        
        for event in pygame.event.get():
            # checking to see if the player closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                # if the player quits the running while loop is set false 
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    if  not data_submitted:
                        if (mouse_x >= text_box.left and mouse_x <= text_box.right)\
                            and (mouse_y >= text_box.top and mouse_y <= text_box.bottom):
                            text_box_clicked = True
                    else:
                        text_box_clicked = False

            if text_box_clicked:             
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15 and event.unicode in excepted_values:
                            player_name += event.unicode

        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)

        some_basic_functions.display_text(WINDOW, 350, 5, 80,\
            "The Martians Invade!", BLACK)
        some_basic_functions.display_text(WINDOW, 500, 100, 70,\
             "Game Over", BLACK)
        some_basic_functions.display_text(WINDOW, 380, SCREEN_HEIGHT - 70,\
             70, "Better Luck Next Time", BLACK)
        some_basic_functions.display_text(WINDOW, SCREEN_WIDTH/2 - 100, \
            200, 30, "Your Score: {}".format(player_score), BLACK)
        some_basic_functions.display_text(WINDOW, SCREEN_WIDTH/2 - 120, \
            240, 30, "Highest Score: {}".format(str(scores[0]["score"])), BLACK)
        some_basic_functions.display_text(WINDOW, SCREEN_WIDTH/2 - 470, 280, 30,\
            "Please select the text box and write your name and then click submit to add it to the leaderboard",\
                BLACK)

        restart_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 - 125, SCREEN_HEIGHT - 250, 200, 50,\
                LIGHT_YELLOW, DARK_YELLOW, 30, BLACK, "Restart")
        if restart_clicked:
            main()

        main_menu_clicked = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 - 125, SCREEN_HEIGHT - 150, 200, 50,\
                LIGHT_YELLOW, DARK_YELLOW, 30, BLACK, "Main menu")
        if main_menu_clicked:
            menu()

        text_box = some_basic_functions.create_text_box(WINDOW,\
            SCREEN_WIDTH/2 - 150, 350, 170, 30, 30, BLACK,\
                player_name, text_box_clicked)

        submit_name = some_basic_functions.create_button(WINDOW,\
            SCREEN_WIDTH/2 + 30, 350, 100, 30, LIGHT_YELLOW,\
                DARK_YELLOW, 30, BLACK, "submit")
        if submit_name:
            if  not data_submitted and len(player_name) > 0:
                some_basic_functions.write_to_scoreboard(player_name,\
                    player_score, scores)
                data_submitted = True
                text_box_clicked = False     

        WINDOW.blit(health_at_0, (0,0))
        WINDOW.blit(alien_image_1, (100, 500))#looking down
        WINDOW.blit(alien_image_2, (50, 500))#looking bottom right
        WINDOW.blit(alien_image_3, (130,500))#looking bottom left
        WINDOW.blit(alien_image_4, (50, 580))#looking top right
        WINDOW.blit(alien_image_5, (100, 600))#looking top
        WINDOW.blit(alien_image_6, (130,580))#looking top left
        WINDOW.blit(alien_image_7, (50,550))#looking right
        WINDOW.blit(alien_image_8, (170,550))#looking left
        WINDOW.blit(player_image_1, (100,550))
        pygame.display.update()
    
menu()