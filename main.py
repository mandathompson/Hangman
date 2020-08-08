import pygame
import math
# import random
from random_words import RandomWords

#set up display
pygame.init()
#choose width and height we want for game to be in pixels
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")


#Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
#every character is defined by a number:
A = 65
for i in range(26):
    #where should we draw the beginning buttons 
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    #i mod 13 is the remainder of i after dividing 13; up until 13 i will count normally and when we hit 13 it will start counting again going up to 13. The distance between each button drawn is (radius * 2 + gap). GAP * 2 keeps us offset from the edge of the screen
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    #put a bunch of pairs of x,y values inside list:
    letters.append([x, y, chr(A + i), True])

#fonts 
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT= pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#load images
images = []
for i in range(7):
    #loops up to but not including 7
    image = pygame.image.load("hangman" + str(i) + ".png") 
    images.append(image)



#game variables
hangman_status = 0
r = RandomWords()
# words = ["HELLO", "PYTHON", "PYGAME", "REPLIT"]
word = r.random_word()
# word = random.choice(words)
guessed = []


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


#game loop to constantly run the game  
#60 frames per second
FPS = 60
#clock object to ensure loop runs at this speed
clock = pygame.time.Clock()
run = True


def draw():
    win.fill(WHITE)
    text = TITLE_FONT.render("Hangman", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    #draw word
    display_word = " "
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else: 
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))


    #draw buttons
    for letter in letters:
        #since all letters are pairs we can split them into their x y values
        #this is called unpacking
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            # draw a circle on the window in black in the center, radius 3
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/ 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)    
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)




while run:
    clock.tick(FPS)


    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #this will get x,y position of mouse
            #0,0 is in the top left hand corner, which is where we begin to draw from
            m_x, m_y = pygame.mouse.get_pos()
            #check if mouse is further than radius of button
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        display_message("You won, hooray!")
        break

    if hangman_status == 6:
        display_message("You lost, boo.")
        text = WORD_FONT.render(word, 1, BLACK)    
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
        break


pygame.quit()



