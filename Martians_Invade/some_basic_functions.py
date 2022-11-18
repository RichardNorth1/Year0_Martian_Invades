import pygame
from os import path

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (200,200,200)

def read_and_convert_scores():
    '''This is a simple function to read a .txt file and return a list of dictionaries 
    note that the file it reads from needs the name and score to be seperated by a ":"
    '''
    allscores = []
    file_name = path.join(path.dirname(__file__), "scores.txt")
    with open(file_name, "r") as file:
        for line in file:
            line.strip("\n")
            data = line.split(":")
            allscores.append(data)

    scores_dictionary_list = []
    for element in allscores:
        score_dictionary = {"name":element[0], "score":int(element[1])}
        scores_dictionary_list.append(score_dictionary)

    return scores_dictionary_list


def write_to_scoreboard(new_name, new_score, scores_list):
    '''This function is used to write the players name and score to a .txt file
    once the new players name and score are passed through it is added to the list
    of dictionaries then sorted and written to the file'''
    scores_list.append({"name":new_name, "score":new_score})
    # sorting the list of dictionaries by the score
    scores_list.sort(key=lambda item: item.get("score"),reverse=True)
    # only keeping the top 5 scores
    scores_list = scores_list[:5]
    file_name = path.join(path.dirname(__file__), "scores.txt")
    with open(file_name, "w") as file:
        for element in scores_list:
            # formatting the the data ready to be written to the file
            player_data = element["name"] + ":" + str(element["score"]) + "\n"
            #writing the data to the file
            file.write(player_data)


def display_score(Surface, score, width):
    '''simple function to display the players score'''
    font = pygame.font.SysFont('ariel',36) # setting the font and the font size
    score = font.render("Score: " + str(score), True, BLACK)
    score_rect = score.get_rect()
    Surface.blit(score, (width - score_rect.width - 10, 0))# displaying the score in the window


def display_level(Surface, Level, width):
    '''simple function to display what level the player is currently on'''
    font = pygame.font.SysFont('ariel',36) # setting the font and the font size
    level = font.render("Level: " + str(Level), True, BLACK)
    level_rect = level.get_rect()
    level_x, level_y = (width/2 - level_rect.width/2- 100), 0 # setting the position the level will be displayed on screen
    Surface.blit(level, (level_x, level_y))# displaying the level in the window 


def display_completion(Surface, Level, width, height):
    '''simple function to display that the player has completed the level'''
    font = pygame.font.SysFont('ariel',66) # setting the font and the font size
    level = font.render("Level: {} Complete".format(str(Level)) , True, BLACK) 
    level_rect = level.get_rect()
    level_x, level_y = (width/2 - level_rect.width/2), (height/2 - level_rect.height / 2)
    Surface.blit(level, (level_x, level_y))# displaying the level in the window


def display_text(Surface, x, y, size, text, colour):
    '''simple to draw text to screen'''
    font = pygame.font.SysFont('ariel',size) # setting the font and the font size 
    writing = font.render(text , True, colour) 
    writing_rect = writing.get_rect
    writing_x, writing_y = x, y
    Surface.blit(writing, (writing_x, writing_y))


def create_button(Surface, x, y, width, height, light_colour, dark_colour, font_size, font_colour, text):
    button_clicked = False
    # setting the font and the font size
    font = pygame.font.SysFont('ariel',font_size)
    writing = font.render(text , True, font_colour)
    writting_rect = writing.get_rect()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if (mouse_x >= x and mouse_x <= x + width) and (mouse_y >= y and mouse_y <= y + height):
        button = pygame.draw.rect(Surface, dark_colour, [x, y, width, height])
        if clicked[0] == 1:
            button_clicked = True
    else:
        button = pygame.draw.rect(Surface, light_colour, [x, y, width, height])

    Surface.blit(writing, (button.x + button.width/2 - writting_rect.width/2,\
            button.y + button.height/2 - writting_rect.height / 2))

    return button_clicked


def create_text_box(Surface, x, y, width, height, font_size, font_colour, text, active):
    # setting the font and the font size
    font = pygame.font.SysFont('ariel',font_size)
    writing = font.render(text , True, font_colour)
    writting_rect = writing.get_rect()
    if active:   
        text_box = pygame.draw.rect(Surface, WHITE, [x, y, width, height])
    else:
        text_box = pygame.draw.rect(Surface, LIGHT_GREY, [x, y, width, height])
    Surface.blit(writing, (text_box.x + text_box.width/2 - writting_rect.width/2,\
            text_box.y + text_box.height/2 - writting_rect.height/2 ))
    return text_box


def draw_leaderboard(Surface, width, height):
    scores_list = read_and_convert_scores()
    pygame.draw.rect(Surface, WHITE, [width / 2 - 225, 150, 470, 350])
    pygame.draw.rect(Surface, BLACK, [width / 2 - 225, 150, 470, 350], 3)
    pygame.draw.line(Surface, BLACK, (width / 2 + 20, 200), (width / 2 + 20, 500), 3)#  vertical
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 200), (width / 2 + 245, 200), 3)#  horizontal
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 250), (width / 2 + 245, 250), 3)
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 300), (width / 2 + 245, 300), 3)
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 350), (width / 2 + 245, 350), 3)
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 400), (width / 2 + 245, 400), 3)
    pygame.draw.line(Surface, BLACK, (width / 2 - 225, 450), (width / 2 + 245, 450), 3)

    display_text(Surface, width / 2 - 125, 160, 40,"Top 5 highest scores", BLACK)
    display_text(Surface, width / 2 - 220, 220, 40,"Name", BLACK)
    display_text(Surface, width / 2 + 30, 220, 40,"Score", BLACK)

    display_text(Surface, width / 2 - 220, 270, 40,scores_list[0]["name"], BLACK)
    display_text(Surface, width / 2 + 30, 270, 40,str(scores_list[0]["score"]), BLACK)    

    display_text(Surface, width / 2 - 220, 320, 40,scores_list[1]["name"], BLACK)
    display_text(Surface, width / 2 + 30, 320, 40,str(scores_list[1]["score"]), BLACK)

    display_text(Surface, width / 2 - 220, 370, 40,scores_list[2]["name"], BLACK)
    display_text(Surface, width / 2 + 30, 370, 40,str(scores_list[2]["score"]), BLACK)

    display_text(Surface, width / 2 - 220, 420, 40,scores_list[3]["name"], BLACK)
    display_text(Surface, width / 2 + 30, 420, 40,str(scores_list[3]["score"]), BLACK)

    display_text(Surface, width / 2 - 220, 470, 40,scores_list[4]["name"], BLACK)
    display_text(Surface, width / 2 + 30, 470, 40,str(scores_list[4]["score"]), BLACK)
 
