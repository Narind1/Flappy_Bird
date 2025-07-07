import pygame
import random
import pandas as pd
import matplotlib.pyplot as plt

# Flappy Bird Attributes Class
class FlappyBirdAttributes:
    #colours used in this code
    black = (0, 0, 0)
    blue = (135, 206, 235)
    green = (0, 200, 0)
    orange = (250, 175, 0)

    #dimensions of screen
    s_width = 600
    s_height = 600

    #attributes of bird
    bird_size = 30
    bird_x = 50
    bird_y = s_height // 2
    gravity = 0.25
    bird_jump = -4.5

    #attributes of pipe
    pipe_width = 50
    pipe_height = random.randint(200, 400)
    pipe_x = s_width
    pipe_speed = 6
    pip_gap = 150
    game_over = False  # Initialize game_over here
    
    def __init__(self):
        self.pipe_height = random.randint(200, 400)
        self.pipe_x = self.s_width
        self.bird_change_y = 0
        self.score = 0

# Setting up the menu for the user interface
print('''.
.
.
.
Hello I am the game spirit.
Before we start enter your name:''')
name = input("")
try:
    with open('high_scores.csv', 'x') as file:
        file.write("Name,Score\n")
except FileExistsError:
    pass
print(f"\nHello {name}")
#loop for program execution
while True:
    print("\nPlease select from the following functions:\n1.PLAY GAME\n2.HIGH SCORE\n3.QUIT\n")
    inp = input("")

    if inp == '1':
        pygame.init()
        attributes = FlappyBirdAttributes()

        scrn = pygame.display.set_mode((attributes.s_width, attributes.s_height))
        pygame.display.set_caption("FLAPPY_BIRD")
        #fps
        clock = pygame.time.Clock()
        #functions to manipulate the attributes
        def draw_bird(x, y):
            pygame.draw.rect(scrn, attributes.orange, (x, y, attributes.bird_size, attributes.bird_size))

        def draw_pipe(x, height):
            pygame.draw.rect(scrn, attributes.green, (x, 0, attributes.pipe_width, height))
            pygame.draw.rect(scrn, attributes.green, (x, height + attributes.pip_gap, attributes.pipe_width, attributes.s_height - height - attributes.pip_gap))

        def reset_pipe():
            attributes.pipe_height = random.randint(200, 400)
            attributes.pipe_x = attributes.s_width

        def display_score(score):
            font = pygame.font.SysFont(None, 50)
            text = font.render(" Score : " + str(score), True, attributes.black)
            scrn.blit(text, (10, 10))

        def check_collision():
            if attributes.bird_x + attributes.bird_size > attributes.pipe_x and attributes.bird_x < attributes.pipe_x + attributes.pipe_width:
                if attributes.bird_y < attributes.pipe_height or attributes.bird_y + attributes.bird_size > attributes.pipe_height + attributes.pip_gap:
                    return True
            return False

        def final_score():
            font = pygame.font.SysFont(None, 70)
            text = font.render("Final Score: " + str(attributes.score), True, attributes.black)
            text_rect = text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 2))
            scrn.blit(text, text_rect)

            font = pygame.font.SysFont(None, 30)
            restart_text = font.render("Click to restart", True, attributes.black)
            restart_text_rect = restart_text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 2 + 50))
            scrn.blit(restart_text, restart_text_rect)

        def restart():
            attributes.bird_y = attributes.s_height // 2
            attributes.bird_change_y = 0
            attributes.score = 0
            attributes.pipe_x = attributes.s_width
            reset_pipe()
            attributes.game_over = False
            attributes.pipe_speed = 6

        def menu(font):
            text = font.render("FLAPPY BIRD", True, attributes.black)
            start_text = text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 4))
            scrn.blit(text, start_text)

            text = font.render("1.Press space bar to fly. ", True, attributes.black)
            start_text = text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 2 + 50))
            scrn.blit(text, start_text)

            text = font.render("2.Avoid hitting the pipes", True, attributes.black)
            start_text = text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 2 + 100))
            scrn.blit(text, start_text)

            text = font.render("3.Fly as long as you can.", True, attributes.black)
            start_text = text.get_rect(center=(attributes.s_width // 2, attributes.s_height // 2 + 150))
            scrn.blit(text, start_text)

        running = True
        menu_display = True
        # game loop
        while running:
            scrn.fill(attributes.blue)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if menu_display:
                            menu_display = False
                        elif not attributes.game_over:
                            attributes.bird_change_y = attributes.bird_jump
                        elif attributes.game_over:
                            restart()

            if menu_display:
                menu(pygame.font.SysFont(None, 50))
                pygame.display.update()
                continue
            
            # to update bird position
            if not attributes.game_over:
                attributes.bird_y += attributes.bird_change_y
                attributes.bird_change_y += attributes.gravity

            draw_bird(attributes.bird_x, attributes.bird_y)

            #to update pipes position
            if not attributes.game_over:
                attributes.pipe_x -= attributes.pipe_speed
                draw_pipe(attributes.pipe_x, attributes.pipe_height)
                attributes.pipe_x -= attributes.pipe_speed

            # checking for collision
            if (attributes.bird_y > attributes.s_height or attributes.bird_y < 0 or check_collision()) and not attributes.game_over:
                attributes.game_over = True

            #to increment the score of player and speed of pipe
            if attributes.pipe_x < -attributes.pipe_width:
                attributes.pipe_x = attributes.s_width
                reset_pipe()
                if not attributes.game_over:
                    attributes.score += 1
                    attributes.pipe_speed += 0.2

            display_score(attributes.score)

            if attributes.game_over:
                final_score()
                
                # Save scores to CSV file after game ends
                with open('high_scores.csv', 'a') as file:
                    file.write(f"{name},{attributes.score}\n")
                    
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
    
    #if user chooses the second option
    elif inp == '2':
        #exception handling
        try:
            df = pd.read_csv('high_scores.csv')

            #using pandas to manipulate the dataframe and getting top 5 score.
            if 'Name' in df.columns and 'Score' in df.columns:
                df_highest_scores = df.groupby('Name')['Score'].max().reset_index()
                df_top5 = df_highest_scores.sort_values(by='Score', ascending=False).head(5)
                
                #plotting the bar plot
                plt.figure(figsize=(10, 6))
                plt.bar(df_top5['Name'], df_top5['Score'], color='blue')
                plt.xlabel('Player Name')
                plt.ylabel('Score')
                plt.title('Top High Scores')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("The CSV file does not have 'Name' or 'Score' columns.")
        except FileNotFoundError:
            print("No high scores yet!")
        except Exception as e:
            print("An error occurred:", e)
    elif inp == '3':
        print("\nThank You \n See yu next time.\n")
        break
    else:
        print("\nPlease Enter valid function from [1 - 2 - 3]\n")
        continue
