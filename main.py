import pygame
import sys
import config
from math import fabs, floor
from random import randint
pygame.init()

WIN = pygame.display.set_mode((config.WIDTH,config.HEIGHT))

SCORE_FONT = pygame.font.SysFont(config.SCORE_FONT_NAME, config.SCORE_FONT_SIZE)
WINNER_FONT = pygame.font.SysFont(config.WINNER_FONT_NAME, config.WINNER_FONT_SIZE)

P1_SCORE = pygame.USEREVENT + 1
P2_SCORE = pygame.USEREVENT + 2

class Ball:
    def __init__(self, p1, p2, moveright, firstime, angle=0,y_vel=0,x_vel=config.BALL_X_STRAIGHT_VEL):
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

        elif ball.rect.x <= ball.p1.x and ball.rect.colliderect(ball.p1):
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

def p1_movement(keys_pressed, p1):
    if keys_pressed[pygame.K_w] and p1.y - config.PLAYER_VEL >= 0:
        p1.y -= config.PLAYER_VEL
    if keys_pressed[pygame.K_s] and p1.y + p1.height + config.PLAYER_VEL <= config.HEIGHT:
        p1.y += config.PLAYER_VEL

def p2_movement(keys_pressed, p2):
    if keys_pressed[pygame.K_UP] and p2.y - config.PLAYER_VEL >= 0:
        p2.y -= config.PLAYER_VEL
    if keys_pressed[pygame.K_DOWN] and p2.y + p2.height + config.PLAYER_VEL <= config.HEIGHT:
        p2.y += config.PLAYER_VEL

def main():
    p1 = pygame.Rect(config.PLAYER_MARGIN, config.HEIGHT/2 - config.PLAYER_HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    p2 = pygame.Rect(config.WIDTH - config.PLAYER_MARGIN, config.HEIGHT/2 - config.PLAYER_HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    ball = Ball(p1,p2,True,True)
    
    clock = pygame.time.Clock()
    run = True

    p1_score = 0
    p2_score = 0
    win_text = ""

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
        
        if p1_score == 7:
            win_text = "P1 Wins!"
        if p2_score == 7:
            win_text = "P2 Wins!"

        keys_pressed = pygame.key.get_pressed()
        p1_movement(keys_pressed, p1)
        p2_movement(keys_pressed, p2)
        ball.movement()
        draw_screen(p1,p2,ball, p1_score, p2_score)


    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()