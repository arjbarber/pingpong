import pygame
import sys
import config
import colors
pygame.init()

WIN = pygame.display.set_mode((config.WIDTH,config.HEIGHT))

def draw_screen(p1,p2,ball):
    WIN.fill(colors.BLACK)

    pygame.draw.rect(WIN, colors.RED, p1)
    pygame.draw.rect(WIN, colors.RED, p2)
    pygame.draw.circle(WIN, colors.WHITE,(ball.x + config.BALL_RADIUS,ball.y + config.BALL_RADIUS),config.BALL_RADIUS,width=0)
    pygame.display.update()

def ball_movement(ball, p1, p2):
    if pygame.Rect.colliderect(ball):
        

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
    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        p1_movement(keys_pressed, p1)
        p2_movement(keys_pressed, p2)
        draw_screen(p1,p2,ball)

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()