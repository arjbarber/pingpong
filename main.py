import pygame
import sys
import config
import os
import colors
import cv2
import mediapipe as mp
from button import Button
from random import randint
from time import time
pygame.init()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join('Assets','font.ttf'), size)


WIN = pygame.display.set_mode((config.WIDTH,config.HEIGHT))

if config.SCORE_FONT_NAME == 'Press-Start-2P':
    SCORE_FONT = get_font(config.SCORE_FONT_SIZE)
else:
    SCORE_FONT = pygame.font.SysFont(config.SCORE_FONT_NAME, config.SCORE_FONT_SIZE)
if config.WINNER_FONT_NAME == 'Press-Start-2P':
    WINNER_FONT = get_font(config.WINNER_FONT_SIZE)
else:
    WINNER_FONT = pygame.font.SysFont(config.WINNER_FONT_NAME, config.WINNER_FONT_SIZE)

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets','Background.png')
)
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(config.WIDTH,config.HEIGHT))


P1_SCORE = pygame.USEREVENT + 1
P2_SCORE = pygame.USEREVENT + 2

class Ball:
    def __init__(self, p1: pygame.Rect, p2: pygame.Rect, moveright: bool, firstime: bool, angle=0,y_vel=0,x_vel=config.BALL_X_STRAIGHT_VEL):
        self.p1 = p1
        self.p2 = p2
        self.rect = pygame.Rect(config.WIDTH/2 - config.BALL_RADIUS,config.HEIGHT/2 - config.BALL_RADIUS, config.BALL_RADIUS*2, config.BALL_RADIUS*2)
        self.moveright = moveright
        self.firsttime = firstime
        self.angle = angle
        self.y_vel = y_vel
        self.x_vel = x_vel

    def movement(ball):
        if ball.rect.x + ball.rect.width >= ball.p2.x and ball.rect.colliderect(ball.p2):
            ball.moveright = False
            if ball.rect.y + config.BALL_RADIUS >= ball.p2.y and ball.rect.y + config.BALL_RADIUS <= ball.p2.y + (ball.p2.height//3):
                ball.y_vel = config.BALL_Y_VEL * -1
                ball.x_vel = config.BALL_X_SLANT_VEL
            elif ball.rect.y + config.BALL_RADIUS > ball.p2.y + (ball.p2.height//3) and  ball.rect.y + config.BALL_RADIUS < ball.p2.y + (2*(ball.p2.height//3)):
                ball.y_vel = 0
                ball.x_vel = config.BALL_X_STRAIGHT_VEL
            elif ball.rect.y + config.BALL_RADIUS >= ball.p2.y + (2*(ball.p2.height//3)) and  ball.rect.y + config.BALL_RADIUS <= ball.p2.y + ball.p2.height:
                ball.y_vel = config.BALL_Y_VEL
                ball.x_vel = config.BALL_X_SLANT_VEL

            if ball.moveright == False:
                ball.x_vel *= -1

        elif ball.rect.x <= ball.p1.x + ball.p1.width and ball.rect.colliderect(ball.p1):
            ball.moveright = True
            if ball.rect.y + config.BALL_RADIUS >= ball.p1.y and ball.rect.y + config.BALL_RADIUS <= ball.p1.y + (ball.p1.height//3):
                ball.y_vel = config.BALL_Y_VEL * -1
                ball.x_vel = config.BALL_X_SLANT_VEL
            elif ball.rect.y + config.BALL_RADIUS > ball.p1.y + (ball.p1.height//3) and  ball.rect.y + config.BALL_RADIUS < ball.p1.y + (2*(ball.p1.height//3)):
                ball.y_vel = 0
                ball.x_vel = config.BALL_X_STRAIGHT_VEL
            elif ball.rect.y + config.BALL_RADIUS >= ball.p1.y + (2*(ball.p1.height//3)) and  ball.rect.y + config.BALL_RADIUS <= ball.p1.y + ball.p1.height:
                ball.y_vel = config.BALL_Y_VEL
                ball.x_vel = config.BALL_X_SLANT_VEL

            if ball.moveright == False:
                ball.x_vel *= -1
            

        if ball.rect.x + ball.rect.width >= config.WIDTH:
            pygame.event.post(pygame.event.Event(P1_SCORE))
        elif ball.rect.x <= 0:
            pygame.event.post(pygame.event.Event(P2_SCORE))

        if ball.firsttime:
            randnum = randint(0,1)
            if randnum == 1:
                randbool = True
            else:
                randbool = False
            ball.moveright = randbool

            ball.firsttime = False

        if ball.rect.y + ball.rect.height >= config.WIDTH or ball.rect.y <= 0:
            ball.y_vel *= -1

        ball.rect.x += ball.x_vel
        ball.rect.y += ball.y_vel
    
    def reset(ball):
        ball.rect.x = config.WIDTH/2 - config.BALL_RADIUS
        ball.rect.y = config.HEIGHT/2 - config.BALL_RADIUS
        ball.p1.x = config.PLAYER_MARGIN
        ball.p1.y = config.HEIGHT/2 - config.PLAYER_HEIGHT/2
        ball.p2.x = config.WIDTH - config.PLAYER_MARGIN
        ball.p2.y = config.HEIGHT/2 - config.PLAYER_HEIGHT/2
        ball.firsttime = True
        ball.x_vel = config.BALL_X_STRAIGHT_VEL
        ball.y_vel = 0

def draw_screen(p1,p2,ball,p1_score,p2_score):
    WIN.fill(config.COLOR)

    p1_score_text = SCORE_FONT.render("Score: " + str(p1_score), 1, config.SCORE_FONT_COLOR)
    p2_score_text = SCORE_FONT.render("Score: " + str(p2_score), 1, config.SCORE_FONT_COLOR)
    WIN.blit(p1_score_text, (config.SCORE_FONT_X_MARGIN, config.SCORE_FONT_Y_MARGIN))
    WIN.blit(p2_score_text, (config.WIDTH - config.SCORE_FONT_X_MARGIN - p2_score_text.get_width() , config.SCORE_FONT_Y_MARGIN))
    
    pygame.draw.rect(WIN, config.PLAYER_COLOR, p1)
    pygame.draw.rect(WIN, config.PLAYER_COLOR, p2)
    pygame.draw.circle(WIN, config.BALL_COLOR,(ball.rect.x + config.BALL_RADIUS,ball.rect.y + config.BALL_RADIUS),config.BALL_RADIUS,width=0)

    pygame.display.update()

def draw_winner(win_text, counter):
    win_text_render = WINNER_FONT.render(win_text, 1, config.WINNER_FONT_COLOR)
    WIN.blit(win_text_render, (config.WIDTH/2 - (win_text_render.get_width()/2), config.HEIGHT/2 - (win_text_render.get_height()/2)))
    
    if counter == 0:
        counter = time()
        pygame.display.update()
    elif time() >= counter + 5.0:
        menu()
    return counter
    

def p1_movement(p1, ball):
    if randint(1, 4) == 1:
        if ball.rect.y + config.BALL_RADIUS < p1.y:
            p1.y -= config.PLAYER_VEL
        elif ball.rect.y + config.BALL_RADIUS > p1.y + p1.height:
            p1.y += config.PLAYER_VEL

def p2_movement(average_y, p2):
    handstate = (average_y * config.HEIGHT) // 2
    if handstate > 0 and handstate + p2.height <= config.HEIGHT:
        p2.y = handstate
    else:
        if handstate <= 0:
            p2.y = 0
        else:
            p2.y = config.HEIGHT - p2.height

def main():
    pygame.display.set_caption("Ping Pong")
    p1 = pygame.Rect(config.PLAYER_MARGIN, config.HEIGHT/2 - config.PLAYER_HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    p2 = pygame.Rect(config.WIDTH - config.PLAYER_MARGIN, config.HEIGHT/2 - config.PLAYER_HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    ball = Ball(p1,p2,True,True)
    
    clock = pygame.time.Clock()
    run = True

    average_y = 0
    count = 0


    p1_score = 0
    p2_score = 0
    win_text = ""
    counter = 0
    isMoving = True

    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == P1_SCORE:
                p1_score += 1
                ball.reset()
            if event.type == P2_SCORE:
                p2_score += 1
                ball.reset()

        ret, frame = cap.read()
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)       
        
        print(count)
        print("y: ", average_y)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), config.LANDMARK_RADIUS, config.LANDMARK_COLOR, -1)
                    average_y += y
                    count += 1
        
        cv2.imshow("Webcam",frame)
        
        if count > 0:
            average_y =  average_y / count

        if isMoving:
            p1_movement(p1, ball)
            p2_movement(average_y, p2)
            ball.movement()
            draw_screen(p1,p2,ball, p1_score, p2_score)
        
        if p1_score >= 7:
            win_text = "P1 Wins!"
            counter = draw_winner(win_text,counter)
            isMoving = False

        if p2_score >= 7:
            win_text = "P2 Wins!"
            counter = draw_winner(win_text,counter)
            isMoving = False
        


    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()

def menu():

    pygame.display.set_caption("Main Menu")

    
    quit_button_surface = pygame.transform.scale(
        pygame.image.load(os.path.join('Assets', 'Play Rect.png')), (400,150)
    )
    play_button_surface = pygame.transform.scale(
        pygame.image.load(os.path.join('Assets', 'Play Rect.png')), (quit_button_surface.get_width(),quit_button_surface.get_height())
    )
    
    MENU_TEXT = get_font(config.MENU_FONT_SIZE).render("Ping Pong", True, config.MENU_FONT_COLOR)
    MENU_RECT = MENU_TEXT.get_rect(center=(config.WIDTH//2,config.HEIGHT//2 - 200))
    
    quitButton = Button(quit_button_surface, (config.WIDTH//2), (config.HEIGHT//2) + 150, "Quit",WIN)
    playButton = Button(play_button_surface, (config.WIDTH//2), (config.HEIGHT//2) - 50, "Play",WIN)
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(config.FPS)
        WIN.fill(colors.WHITE)
        WIN.blit(BACKGROUND, (0,0))
        WIN.blit(MENU_TEXT, MENU_RECT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(pygame.mouse.get_pos()):
                    main()
                if quitButton.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        
        playButton.update()
        playButton.changeColor(pygame.mouse.get_pos())
        quitButton.update()
        quitButton.changeColor(pygame.mouse.get_pos())
        pygame.display.update()

if __name__ == "__main__":
    menu()