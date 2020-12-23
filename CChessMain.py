import pygame as pygame
import CChessEngine
import os

pygame.init()

WIDTH = 576
HEIGHT = 640
SQ_SIZE = 64
MAX_FPS = 15
ROWS = 10
COLUMNS = 9
IMAGES = {}
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


def loadImages():
    pieces = ["bR", "bH", "bE", "bG", "bK", "bC", "bP",
              "rP", "rC", "rK", "rG", "rE", "rH", "rR", ]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.smoothscale(
            pygame.image.load("chinese\\" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    IMAGES['board'] = pygame.transform.smoothscale(
        pygame.image.load(r"chinese\board.png"), (WIDTH, HEIGHT))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = CChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = ()  # tuple: row,col
    playerClicks = []  # list of 2 tuples max
    validMoves = gs.getValidMoves()
    moveMade = False
    drawGameState(screen, gs)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                    drawGameState(screen, gs)
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    if gs.redToMove:
                        drawBorder(screen, sqSelected, RED)
                    if not gs.redToMove:
                        drawBorder(screen, sqSelected, BLACK)
                    for movement in validMoves:
                        if movement[0] == sqSelected:
                            drawBorder(screen, movement[1], BLUE)
                    if len(playerClicks) == 2:
                        move = CChessEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board)
#                        print(move.moveID[0])
#                        print(move.moveID[1])
                        if move.moveID in validMoves:
                            gs.makeMove(move)
                            sqSelected = ()
                            playerClicks = []
                            drawGameState(screen, gs)
                            moveMade = True
                        else:
                            sqSelected = ()
                            playerClicks = []
                            drawGameState(screen, gs)
            # keyboard presses(
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()
                    drawGameState(screen, gs)
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            if len(validMoves) == 0:
                #                if gs.redToMove:
                #                    print("checkmate! black won!")
                #                else:
                #                    print("checkmate! red won!")
                declareWinner(screen)
            moveMade = False

        clock.tick(MAX_FPS)
        pygame.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    pygame.display.update()


def drawBoard(screen):
    screen.fill(pygame.Color("white"))
    screen.blit(IMAGES['board'], pygame.Rect(
        0, 0, WIDTH, HEIGHT))


def drawPieces(screen, board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(
                    c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    pygame.display.update()


def drawBorder(screen, position, color):
    # position -> (row,col)
    row = position[0]
    col = position[1]
    # topleft
    pygame.draw.rect(screen, color, (col * SQ_SIZE +
                                     4, row * SQ_SIZE + 4, 4, 4))
    # topright
    pygame.draw.rect(screen, color, ((col + 1) *
                                     SQ_SIZE - 4 - 4, row * SQ_SIZE + 4, 4, 4))
    # btmleft
    pygame.draw.rect(screen, color, (col * SQ_SIZE + 4,
                                     (row + 1) * SQ_SIZE - 4 - 4, 4, 4))
    # btmright
    pygame.draw.rect(screen, color, ((col + 1) * SQ_SIZE -
                                     4 - 4, (row + 1) * SQ_SIZE - 4 - 4, 4, 4))


def declareWinner(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('checkmate!', True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, textRect)


main()
