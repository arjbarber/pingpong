import pygame
import sys
import config
import colors
from random import randint
pygame.init()

WIN = pygame.display.set_mode((config.WIDTH,config.HEIGHT))

P1_SCORE = pygame.USEREVENT + 1
P2_SCORE = pygame.USEREVENT + 2

def draw_screen(p1,p2,ball):
    WIN.fill(colors.BLACK)

    pygame.draw.rect(WIN, colors.RED, p1)
    pygame.draw.rect(WIN, colors.RED, p2)
    pygame.draw.circle(WIN, colors.WHITE,(ball.x + config.BALL_RADIUS,ball.y + config.BALL_RADIUS),config.BALL_RADIUS,width=0)

    pygame.display.update()

def ball_movement(ball, p1, p2, firsttime,moveright):
    if firsttime:
        randnum = randint(0,1)
        if randnum == 1:
            randbool = True
        else:
            randbool = False
        
        moveright = randbool
    
    if ball.x + ball.width >= p2.x and pygame.Rect.colliderect(ball):
        moveright = not(moveright)
    if ball.x <= p1.x and pygame.Rect.colliderect(ball):
        moveright = not(moveright)
    if ball.x + ball.width >= config.WIDTH:
        pygame.event.post(pygame.event.Event(P1_SCORE))
    if ball.x <= 0:
        pygame.event.post(pygame.event.Event(P2_SCORE))
    
    if moveright:
        ball.x += config.BALL_VEL
    if moveright == False:
        ball.x -= config.BALL_VEL

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
    p1 = pygame.Rect(20, config.HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    p2 = pygame.Rect(config.WIDTH-20, config.HEIGHT/2, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
    ball = pygame.Rect(config.WIDTH/2,config.HEIGHT/2, config.BALL_RADIUS*2, config.BALL_RADIUS*2)

    clock = pygame.time.Clock()
    run = True
    firsttime = True
    moveright = True

    p1_score = 0
    p2_score = 0

    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == P1_SCORE:
                p1_score += 1
            if event.type == P2_SCORE:
                p2_score += 1
        
        keys_pressed = pygame.key.get_pressed()
        p1_movement(keys_pressed, p1)
        p2_movement(keys_pressed, p2)
        ball_movement(ball, p1, p2, firsttime,moveright)
        draw_screen(p1,p2,ball)

        firsttime = False

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()