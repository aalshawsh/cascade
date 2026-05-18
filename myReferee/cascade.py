import pygame
from pygame.locals import *
import asyncio
from time import time
from typing import AsyncGenerator
from .log import LogStream
from .game import PlayerColor, Coord, Direction, \
    Action, PlaceAction, MoveAction, EatAction, CascadeAction
from .game.constants import BOARD_N
from .game.coord import CARDINAL_DIRECTIONS
from .game import Player, game, \
    GameUpdate, PlayerInitialising, GameBegin, TurnBegin, TurnEnd, \
    BoardUpdate, PlayerError, GameEnd, UnhandledError, PlayerColor
from .game.board import Board, GamePhase
from .game.coord import Coord
from time import sleep
import json
import sys



SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FRAME_RATE = 60
ANIMATION_SPEED = 14*2  # frame speed
DELAY = 0 # set delay for agents so we can get not flash speeds of movement on screen



class Cascade:

    def __init__(self, red_player, blue_player):
        
        # initialize game
        pygame.init()

        # initialize sounds
        pygame.mixer.init()

        # initialize font
        pygame.font.init()
        self.my_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 12)

        # initialize screen of size 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # animation
        self.volume_frames = [pygame.image.load(f"animation/volume{i+1}.png").convert() for i in range(2)]
        self.volume_off_frames = [pygame.image.load(f"animation/volumeoff{i+1}.png").convert() for i in range(2)]
        self.volume_rect = self.volume_frames[0].get_rect(topleft=(SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
        self.board_frames = [pygame.transform.scale(pygame.image.load(f"animation/square{i+1}.png").convert(), (SCREEN_HEIGHT, SCREEN_HEIGHT)) for i in range(2)]
        self.start_menu_frames =  [pygame.image.load(f"animation/startmenu{i+1}.png").convert() for i in range(2)]
        self.red = {}
        self.blue = {}
        for i in range(12):
            
            self.red[i+1] =[
            pygame.transform.scale(
                pygame.image.load(f"animation/players/{i+1}red{j+1}.png").convert_alpha(),(15 * 5, 12 * 5)
                )
                for j in range(2)
            ]
            self.blue[i+1] = [
            pygame.transform.scale(
                pygame.image.load(f"animation/players/{i+1}blue{j+1}.png").convert_alpha(),(15 * 5, 12 * 5)
                )
                for j in range(2)
            ]
        self.cascade_animation_off= [pygame.image.load(f"animation/cascadeoff{i+1}.png").convert_alpha() for i in range(2)]
        self.cascade_animation_off_rect = self.cascade_animation_off[0].get_rect(topleft=(730,510))

        self.cascade_animation_on= [pygame.image.load(f"animation/cascadeon{i+1}.png").convert_alpha() for i in range(2)]
        self.cascade_animation_on_rect = self.cascade_animation_on[0].get_rect(topleft=(730,440))
     

        self._board = Board()
        # maping of board coordinates to on screen board
        self.board_mapping: dict[Coord,tuple] = {Coord(0,0):(49,51),Coord(0,1):(143,54),Coord(0,2):(237,50),Coord(0,3):(327,49),Coord(0,4):(419,49),Coord(0,5):(510,54),Coord(0,6):(596,53),Coord(0,7):(675,50),
                                                 Coord(1,0):(53,145),Coord(1,1):(142, 141),Coord(1,2):(229, 143),Coord(1,3):(324, 139),Coord(1,4):(423, 139),Coord(1,5):(508, 137),Coord(1,6):(595, 139),Coord(1,7):(679, 140),
                                                 Coord(2,0):(54, 247),Coord(2,1):(145, 241),Coord(2,2):(229, 242),Coord(2,3):(327, 242),Coord(2,4):(420, 240),Coord(2,5):(506, 238),Coord(2,6):(590, 236),Coord(2,7):(678, 237),
                                                 Coord(3,0):(50, 336),Coord(3,1):(142, 335),Coord(3,2):(230, 335),Coord(3,3):(325, 333),Coord(3,4):(420, 332),Coord(3,5):(510, 329),Coord(3,6):(593, 334),Coord(3,7):(676, 333),
                                                 Coord(4,0):(54, 415),Coord(4,1):(150, 419),Coord(4,2):(238, 422),Coord(4,3):(336, 422),Coord(4,4):(422, 418),Coord(4,5):(504, 421),Coord(4,6):(598, 418),Coord(4,7):(675, 421),
                                                 Coord(5,0):(53, 497),Coord(5,1):(156, 505),Coord(5,2):(243, 506),Coord(5,3):(333, 509),Coord(5,4): (428, 509),Coord(5,5):(515, 504),Coord(5,6):(595, 507),Coord(5,7):(675, 511),
                                                 Coord(6,0):(47, 587),Coord(6,1):(154, 588),Coord(6,2):(250, 590),Coord(6,3):(343, 588),Coord(6,4): (438, 589),Coord(6,5):(521, 590),Coord(6,6):(602, 591),Coord(6,7):(681, 592),
                                                 Coord(7,0):(52, 674),Coord(7,1):(156, 671),Coord(7,2):(259, 669),Coord(7,3):(357, 668),Coord(7,4): (440, 670),Coord(7,5):(524, 668),Coord(7,6):(604, 671),Coord(7,7):(687, 670)}


        # draw squares on each of the on screen board for input detection
        self.board_input_mapping = {}
        for coord, board_centre in self.board_mapping.items():
            self.board_input_mapping[coord] = pygame.Rect(board_centre[0] - 35, board_centre[1] - 35, 70, 70)

        # music to be looped
        pygame.mixer.music.load("audio/omgthisissocweepy.wav")
        pygame.mixer.music.play(-1)

        # title of the game!
        pygame.display.set_caption("CASCADE")

        self.clock = pygame.time.Clock()

        # agent information, if we r against a human save that info
        self.red_player = red_player
        self.blue_player = blue_player
        self.playing_with_dumb_human = False
        self.human_agents = []
        if "myHumanAgent" in self.red_player:
            self.human_agents.append(PlayerColor.RED)
            self.playing_with_dumb_human = True
        if "myHumanAgent" in self.blue_player:
            self.human_agents.append(PlayerColor.BLUE)
            self.playing_with_dumb_human = True

        self.running = True
        self.frame_counter = 0
        self.animation_frame = 0
        self.volume_off = False
        self.game_end = False
        self.results = None
        self.cascade_on = False

    def _start_menu_loop(self):
        
        tmp = True

        # loop game start screen until space is pressed
        while(tmp):
            self.clock.tick(FRAME_RATE)
            for event in pygame.event.get():
                if(event.type == KEYDOWN):
                    if(event.key == K_SPACE):
                        tmp = False
                        break
            
            self._cycle_frames()
                
                    

            # draw start screen
            self.screen.blit(self.start_menu_frames[self.animation_frame], (0, 0))


            pygame.display.update()

        # erase screen
        self.screen.fill((0,0,0))

    def _cycle_frames(self):
         # update frame counter to cycle thru frames
        self.frame_counter = (self.frame_counter + 1) % ANIMATION_SPEED
        if self.frame_counter == 0:
            self.animation_frame = (self.animation_frame+1) % 2

    def _render_loop(self):

        selected_coord = None
        while(self.running):

            board_cell_pressed = None
            self.clock.tick(FRAME_RATE)
            for event in pygame.event.get():
                if(event.type == QUIT):
                    print("Game ending!")
                    self.running= False
                    break

                if(event.type == MOUSEBUTTONDOWN):
                    # turn off music
                    if(self.volume_rect.collidepoint(event.pos)):
                        self.volume_off= not self.volume_off
                        if(self.volume_off):pygame.mixer.music.pause()
                        else:pygame.mixer.music.unpause()
                        
                    # turn cascade on/off
                    if(self.cascade_animation_on_rect.collidepoint(event.pos) and self.cascade_on):
                        self.cascade_on=False
                    elif(self.cascade_animation_off_rect.collidepoint(event.pos) and not self.cascade_on):
                        self.cascade_on=True
                
                    # if player pressed on
                    if(self.playing_with_dumb_human):
                        for coord, board_centre in self.board_input_mapping.items():
                            if(board_centre.collidepoint(event.pos)):
                                board_cell_pressed = coord

                                if(self._board._state[coord].color == self._board.turn_color):
                                    if(selected_coord == None):
                                        selected_coord = coord
                                    elif coord == selected_coord:
                                        selected_coord = None



            self._cycle_frames()

            self.screen.fill((0,0,0))

            # display cascade animation
            if(self.cascade_on):
                self.screen.blit(self.cascade_animation_on[self.animation_frame],(730,440))
            else:
                self.screen.blit(self.cascade_animation_off[self.animation_frame],(730,510))


            # draw board
            self.screen.blit(self.board_frames[self.animation_frame], (0, 0))

            # display game info
            self._game_info()

            # draw towers
            for coord,tower in self._board._state.items():

                if(not self._board[coord].is_empty):
                    if(tower.color == PlayerColor.BLUE):
                        rect = self.blue[tower.height][self.animation_frame].get_rect(center=self.board_mapping[coord])
                        self.screen.blit(self.blue[tower.height][self.animation_frame], rect)
                    else:
                        rect = self.red[tower.height][self.animation_frame].get_rect(center=self.board_mapping[coord])
                        self.screen.blit(self.red[tower.height][self.animation_frame], rect)


            # draw volume on/off
            if(self.volume_off == False):
                self.screen.blit(self.volume_frames[self.animation_frame], (SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
            else:
                self.screen.blit(self.volume_off_frames[self.animation_frame], (SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
                
            # if playing against a human get input data:
            if(self.playing_with_dumb_human):

                for coord, rectangle in self.board_input_mapping.items():
                    pygame.draw.rect(self.screen, (255, 0, 0), rectangle, 1)

            # if human players turn draw list of possible moves
            if(self._board.turn_color in self.human_agents):
                
                if(self._board.phase == GamePhase.PLACEMENT):
                    legal_coords = {action.coord for action in self._legal_placements(self._board.turn_color)}
                    
                    for coord in legal_coords :
                        pygame.draw.rect(self.screen, (0, 255, 0), self.board_input_mapping[coord], 1)
                    if(board_cell_pressed in legal_coords):
                        self._write_move("place",board_cell_pressed,None)
                else:

                    # highlight pressed player
                    if(selected_coord is not None and self._board._state[selected_coord].color == self._board.turn_color):
                        pygame.draw.rect(self.screen, (255, 255, 0), self.board_input_mapping[selected_coord], 1)

                        # get possible action for this selected tower
                        actions = self._legal_play_actions(self._board.turn_color,selected_coord)
                        for action in actions:

                            try:
                                dest = action.coord+action.direction
                            except ValueError:
                                continue

                            if(isinstance(action,CascadeAction) and self.cascade_on):
                                pygame.draw.rect(self.screen, (128, 0, 128), self.board_input_mapping[dest], 1)
                            elif(isinstance(action,EatAction)and not self.cascade_on):
                                pygame.draw.rect(self.screen, (0, 255, 255), self.board_input_mapping[dest], 1)
                            elif(isinstance(action,MoveAction)and not self.cascade_on):
                                pygame.draw.rect(self.screen, (0, 255, 0), self.board_input_mapping[dest], 1)
                                
                
                            if(board_cell_pressed == (dest)):
                                if(isinstance(action,EatAction) and not self.cascade_on):
                                    self._write_move("eat",action.coord,action.direction)
                                    selected_coord = None
                                elif(isinstance(action,MoveAction) and not self.cascade_on):
                                    self._write_move("move",action.coord,action.direction)
                                    selected_coord = None
                                elif(isinstance(action,CascadeAction) and self.cascade_on):
                                    self._write_move("cascade",action.coord,action.direction)
                                    selected_coord = None

       

            pygame.display.update()
        
        quit()


    def _write_move(self,action:str,coord:Coord,direction: Direction):
        """
            write to json file 
        """

        move = {"action":action,"row":coord.r,"col":coord.c, "direction": direction.name if direction is not None else None}
        with open("gameInfo.json","w") as fp:
            json.dump(move,fp)



    def _game_info(self):

        # if its somebodies turn display their waiting 

        # if game ended display who won and possibly a rematch?
        if(self.game_end):
            text_surface = self.my_font.render(f'{self.results} WON!! HOORAY! kill me', False, (255,255,255)) 
            self.screen.blit(text_surface, (733,26))
        else:
            text_surface = self.my_font.render(f'{self._board.turn_color} turn! Move number: {self._board.turn_count}', False, (255,255,255)) 
            self.screen.blit(text_surface, (733,26))



    async def update_game(self)-> AsyncGenerator:
        while True:
            update: GameUpdate = yield
            match update:
                case BoardUpdate(board):
                   self._board = board
                   sleep(DELAY)
                   pass
                case GameEnd(None):
                    self.game_end = True
                    self.results = None
                case GameEnd(winner):
                    self.game_end = True
                    self.results = winner


    def _legal_placements(self,player_color: PlayerColor) -> list[PlaceAction]:
        """
        Returns a list of all legal placement actions for the current board state.
        """
        actions = []
        for r in range(BOARD_N):
            for c in range(BOARD_N):
                coord = Coord(r, c)
                
                # Skip occupied cells
                if not self._board[coord].is_empty:
                    continue

                # Skip cells adjacent to opponent's pieces if it's not the first placement
                if self._board._placement_count > 0 and self._adj_opponent(coord,player_color):
                    continue

                actions.append(PlaceAction(coord))
        return actions

    def _adj_opponent(self, coord: Coord, player_color: PlayerColor) -> bool:
        """
        Return True if the given coordinate is adjacent to an opponent's piece, False otherwise.
        """
        opp = player_color.opponent
        for d in CARDINAL_DIRECTIONS:
            try:
                if self._board[coord + d].color == opp:
                    return True
            except ValueError:
                pass
        return False
    

    def _legal_play_actions(self,player_color: PlayerColor, coord:Coord) -> list[Action]:
        """
        Returns a list of all legal play actions (MOVE, EAT, CASCADE) for the current a specific piece
        """
        state = self._board._state
        color = player_color
        opp = color.opponent

        eat_actions = []
        cascade_actions = []
        move_actions = []

        cell = self._board._state[coord]
        for d in CARDINAL_DIRECTIONS:
            try:
                des = coord + d
                if self._board[des].is_empty:
                    move_actions.append(MoveAction(coord, d))
                elif self._board[des].color == color:
                    move_actions.append(MoveAction(coord, d))
                elif self._board[des].color == opp:
                    if (cell.height >= self._board[des].height):
                        eat_actions.append(EatAction(coord, d))
            except ValueError:
                pass
            
        # Check for possible cascade actions
        if cell.height >= 2:
            for d in CARDINAL_DIRECTIONS:
                cascade_actions.append(CascadeAction(coord, d))
        
        return eat_actions + cascade_actions + move_actions


    def quit(self):
        pygame.quit()

