import pygame
from pygame.locals import *

"""
Huge help from https://pygame.readthedocs.io/en/latest/1_intro/intro.html
"""

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FRAME_RATE = 60
ANIMATION_SPEED = 14*2  #12 frames per seconds for animation
def main():

    # initialize game
    pygame.init()

    # initialize sounds
    pygame.mixer.init()

    # initialize screen of size 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # animation
    volume_frames = [pygame.image.load(f"animation/volume{i+1}.png").convert() for i in range(2)]
    volume_off_frames = [pygame.image.load(f"animation/volumeoff{i+1}.png").convert() for i in range(2)]
    volume_rect = volume_frames[0].get_rect(topleft=(SCREEN_WIDTH-50, SCREEN_HEIGHT-50))

    board_frames = [pygame.transform.scale(pygame.image.load(f"animation/square{i+1}.png").convert(), (SCREEN_HEIGHT, SCREEN_HEIGHT)) for i in range(2)]
    
    # music to be looped
    pygame.mixer.music.load("audio/omgthisissocweepy.wav")
    pygame.mixer.music.play(-1)

    # set background color
    background = BLACK
    screen.fill(BLACK)

    # title of the game!
    pygame.display.set_caption("CASCADE")


    clock = pygame.time.Clock()


    # main game loop
    running = True
    frame_counter = 0
    animation_frame = 0
    volume_off = False
    while(running):

        clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            print(event)
            if(event.type == QUIT):
                print("Game ending!")
                running= False
                break

            if(event.type == MOUSEBUTTONDOWN):
                # turn off music
                if(volume_rect.collidepoint(event.pos)):
                    volume_off= not volume_off
                    if(volume_off):pygame.mixer.music.pause()
                    else:pygame.mixer.music.unpause()
        

        # update frame counter to cycle thru frames
        frame_counter = (frame_counter + 1) % ANIMATION_SPEED
        if frame_counter == 0:
            animation_frame = (animation_frame+1) % 2

        # draw board
        screen.blit(board_frames[animation_frame], (0, 0))

        # draw volume on/off
        if(volume_off == False):
            screen.blit(volume_frames[animation_frame], (SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
        else:
            screen.blit(volume_off_frames[animation_frame], (SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
            
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
    


