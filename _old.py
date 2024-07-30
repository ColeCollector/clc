import pygame
import chess
import chess.engine
import openingtree

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Initialize variables
running = True
holding = False
bonded = None
movemade = False
compmove = None
hint = None
original = None
eval_toggle = True

eval = 0
drop_counter = 0

pgn = []

sounds = [pygame.mixer.Sound('sounds/mate.mp3'),pygame.mixer.Sound('sounds/move.mp3'),pygame.mixer.Sound('sounds/sparkle.mp3'),pygame.mixer.Sound('sounds/takes.mp3')]
sounds[2].set_volume(0.05)

# Initialize chess board
board = chess.Board()
board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')                                                                        

# Define the path to the Stockfish executable
stockfish_path = "stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Define square coordinates and image mappings
xaxis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
images = {"K": "Wking", "Q": "Wqueen", "R": "Wrook", "B": "Wbishop", "N": "Wknight", "P": "Wpawn",
          "k": "Bking", "q": "Bqueen", "r": "Brook", "b": "Bbishop", "n": "Bknight", "p": "Bpawn"}

# Display text on the screen
def show_text(text,size,location,color):
    a1 = pygame.font.Font(None, size).render(text, True, color)
    a2 = a1.get_rect(center=location) 
    screen.blit(a1, a2)

def piece_with_square(piece, square):
    piece_symbol = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol().lower()
    return f"{piece_symbol}{chess.square_name(square)}"

# Resets board visuals
def board_reset():
    global circle_squares, moves, board_pieces, piece_images, pos, og_pos, movepos, sorted_pieces, sorted_moves
    piece_images = []
    pos = []
    og_pos = []
    movepos = []
    sorted_pieces = []
    sorted_moves = []

    board_pieces = []
    moves = {}
    circle_squares = []

    # Initialize board piece_images
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            board_pieces.append(piece_with_square(piece, square))

    # Initialize moves
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        piece_square = piece_with_square(piece, move.from_square)
        san_move = board.san(move).replace('+', '').replace('#', '')
        if piece_square not in moves:
            moves[piece_square] = []
        moves[piece_square].append(san_move)
        circle_squares.append(san_move)

    # Initialize board rendering
    for j in range(8):
        for i in range(8):
            for piece in board_pieces:
                if xaxis.index(piece[1]) == i and 8 - int(piece[2]) == j:
                    piece_images.append(pygame.image.load(f"images/{images[piece[0]]}.png"))
                    sorted_pieces.append(piece)
                    pos.append(pygame.Vector2(340 + 75 * i + 37.5, 60 + 75 * j + 37.5))
                    og_pos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])

            for move in circle_squares:
                if move == 'O-O':
                    if 6 == i and 7 == j:
                        movepos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])
                        sorted_moves.append(move)

                elif move == 'O-O-O':
                    if 2 == i and 7 == j:
                        movepos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])
                        sorted_moves.append(move)

                elif xaxis.index(move[-2]) == i and 8 - int(move[-1]) == j:
                    movepos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])
                    sorted_moves.append(move)

board_reset()

transparent_surface = pygame.Surface((1280, 200), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 128))  # Fill with semi-transparent red (RGBA)

while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            holding = True
            for j in range(4):
                if pygame.Rect(1000,265+50*j,150,40).collidepoint(mouse):
                    if button_text[j] == "Resign":
                        if original != None:
                            pgn = []
                            original = None
                            compmove = None
                            eval = 0
                            board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')       
                            board_reset()

                    elif button_text[j] == "Hint":
                        result = engine.play(board, chess.engine.Limit(time=1))
                        hint = f"{board.piece_at(result.move.from_square)}{chess.square_name(result.move.from_square)}"
                        hint_end = board.san(result.move).replace('+','').replace('#', '')

                    elif button_text[j] == "Eval":
                        if eval_toggle:
                            eval_toggle = False
                        else:
                            eval_toggle = True

                    elif button_text[j] == "Flip":
                        pass
            
            # Switching to a new piece if you click on another piece while holding a piece
            for i in og_pos:
                if sorted_pieces[og_pos.index(i)][0].isupper():
                    if (mouse[0] > i[0] - 50 and mouse[0] < i[0] + 50) and (mouse[1] > i[1] - 50 and mouse[1] < i[1] + 50):
                        bonded = og_pos.index(i)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if bonded is not None:
                if sorted_pieces[bonded] in moves:
                    for l, i in enumerate(movepos):
                        if (mouse[0] > i[0] - 50 and mouse[0] < i[0] + 50) and (mouse[1] > i[1] - 50 and mouse[1] < i[1] + 50):
                            if sorted_pieces[bonded] in moves and sorted_moves[l] in moves[sorted_pieces[bonded]]:
                                hint = None
                                hint_end = None

                                #play moving sound
                                if "x" not in sorted_moves[l]:
                                    sounds[1].play()

                                #play different sound for capture
                                else:
                                    sounds[3].play()

                                pos[bonded] = pygame.Vector2(i[0], i[1])
                                movemade = True

                                # Drawing the chess board
                                for j in range(8):
                                    for i in range(8):
                                        color = "white" if (i + j) % 2 == 0 else "#D684FF"
                                        
                                        if compmove != None:
                                            if compmove == 'O-O':
                                                if 6 == i and 7 == j:
                                                    color = "#FFFFC6" if color == "white" else "#FFE884"

                                            elif compmove == 'O-O-O':
                                                if 2 == i and 7 == j:
                                                    color = "#FFFFC6" if color == "white" else "#FFE884"

                                            elif "=" in compmove:
                                                if xaxis.index(compmove[-4]) == i and 8 - int(compmove[-3]) == j:
                                                    color = "#FFFFC6" if color == "white" else "#FFE884"

                                            elif i == xaxis.index(compmove[-2]) and j==8-int(compmove[-1]):
                                                color = "#FFFFC6" if color == "white" else "#FFE884"

                                            if i == xaxis.index(original[-2]) and j==8-int(original[-1]):
                                                color = "#FFFFC6" if color == "white" else "#FFE884"

                                        pygame.draw.rect(screen, color, pygame.Rect(340 + 75 * i, 60 + 75 * j, 75, 75))

                                # Drawing piece_images
                                for i in range(len(piece_images)):
                                    piece_images[i].convert()
                                    rect = piece_images[i].get_rect(center=(pos[i].x, pos[i].y))
                                    screen.blit(piece_images[i], rect)

                                pygame.display.flip()
                                san_move = sorted_moves[l]
                                pgn.append(san_move)
                                move = board.parse_san(san_move)
                                board.push(move)
                                treemove = openingtree.based_move(pgn)

                                if treemove != None: 
                                    compmove = treemove
                                    treemove = board.parse_san(treemove)
                                    original = f"{board.piece_at(treemove.from_square)}{chess.square_name(treemove.from_square)}"
                                    pgn.append(compmove)
                                    board.push(treemove)

                                else:
                                    # Get the best move from Stockfish
                                    result = engine.play(board, chess.engine.Limit(time=1))
                                    original = f"{board.piece_at(result.move.from_square)}{chess.square_name(result.move.from_square)}"
                                    compmove = board.san(result.move).replace('+','').replace('#', '')
                                    pgn.append(compmove)
                                    board.push(result.move)

                                info = engine.analyse(board, chess.engine.Limit(time=2))
                                eval = info["score"]
                                eval = eval.pov(chess.WHITE).score()


                                # Opening Tree Sound effect
                                if treemove != None: 
                                    sounds[2].play()

                                # Mate sound
                                if len(moves) == 0:
                                    sounds[0].play()

                                # Moving sound
                                elif "x" not in compmove:
                                    sounds[1].play()

                                # Play different sound for capture
                                else:
                                    sounds[3].play()

                                board_reset()
                                break

                if not movemade:
                    if (mouse[0] > og_pos[bonded][0] - 50 and mouse[0] < og_pos[bonded][0] + 50) and (mouse[1] > og_pos[bonded][1] - 50 and mouse[1] < og_pos[bonded][1] + 50):
                        
                        drop_counter += 1
                        pos[bonded] = pygame.Vector2(og_pos[bonded][0], og_pos[bonded][1])

                        if drop_counter == 2:
                            drop_counter = 0
                            bonded = None
                        

                            

                    else:
                        pos[bonded] = pygame.Vector2(og_pos[bonded][0], og_pos[bonded][1])
                        bonded = None
                        
                else:
                    movemade = False
                    bonded = None

            holding = False

    screen.fill("white")

    button_text = ["Resign","Hint","Eval","Flip"]

    for j in range(4):
        if pygame.Rect(1000,265+50*j,150,40).collidepoint(mouse):
            pygame.draw.rect(screen, '#E9BFFF', (1000,265+50*j,150,40))
            show_text(button_text[j],40,(1075,285+50*j),'white')

        else:
            pygame.draw.rect(screen, '#AE4ADB', (1000,265+50*j,150,40))
            show_text(button_text[j],40,(1075,285+50*j),'white')


    #print(movemade,bonded,holding)

    # Drawing the chess board
    for j in range(8):
        for i in range(8):
            color = "white" if (i + j) % 2 == 0 else "#D684FF"
            
            if compmove != None:
                if compmove == 'O-O':
                    if 6 == i and 7 == j:
                        color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"

                elif compmove == 'O-O-O':
                    if 2 == i and 7 == j:
                        color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"
                
                elif "=" in compmove:
                    if xaxis.index(compmove[-4]) == i and 8 - int(compmove[-3]) == j:
                        color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"

                elif i == xaxis.index(compmove[-2]) and j==8-int(compmove[-1]):
                    color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"
        
                if i == xaxis.index(original[-2]) and j==8-int(original[-1]):
                    color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"

            if hint != None:
                if hint_end == 'O-O':
                    if 6 == i and 7 == j:
                        color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

                elif hint_end == 'O-O-O':
                    if 2 == i and 7 == j:
                        color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"
                
                elif "=" in hint_end:
                    if xaxis.index(hint_end[-4]) == i and 8 - int(hint_end[-3]) == j:
                        color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

                elif i == xaxis.index(hint_end[-2]) and j==8-int(hint_end[-1]):
                    color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

                if i == xaxis.index(hint[-2]) and j==8-int(hint[-1]):
                    color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

            pygame.draw.rect(screen, color, pygame.Rect(340 + 75 * i, 60 + 75 * j, 75, 75))

            if bonded is not None and sorted_pieces[bonded] in moves:
                for move in moves[sorted_pieces[bonded]]:
                    if "=" in move:
                        if xaxis.index(move[-4]) == i and 8 - int(move[-3]) == j:
                            color = "#EBCCFF" if (i + j) % 2 == 0 else "#945CB2"
                        pygame.draw.circle(screen, color, [377.5 + 75 * i, 97.5 + 75 * j], 15)
                        
                    elif move == 'O-O':
                        if 6 == i and 7 == j:
                            color = "#EBCCFF" if (i + j) % 2 == 0 else "#945CB2"
                        pygame.draw.circle(screen, color, [377.5 + 75 * i, 97.5 + 75 * j], 15)

                    elif move == 'O-O-O':
                        if 2 == i and 7 == j:
                            color = "#EBCCFF" if (i + j) % 2 == 0 else "#945CB2"
                        pygame.draw.circle(screen, color, [377.5 + 75 * i, 97.5 + 75 * j], 15)

                    elif xaxis.index(move[-2]) == i and 8 - int(move[-1]) == j:
                        color = "#EBCCFF" if (i + j) % 2 == 0 else "#945CB2"
                        pygame.draw.circle(screen, color, [377.5 + 75 * i, 97.5 + 75 * j], 15)

    # Drawing piece_images
    for i in range(len(piece_images)):
        piece_images[i].convert()
        rect = piece_images[i].get_rect(center=(pos[i].x, pos[i].y))
        screen.blit(piece_images[i], rect)

    if holding:
        if bonded is None:
            for i in range(len(pos)):
                if sorted_pieces[i][0].isupper():
                    if (pos[i].x - 50 < mouse[0] < pos[i].x + 50) and (pos[i].y - 50 < mouse[1] < pos[i].y + 50):
                        bonded = i
                        break
        else:
            pos[bonded] = pygame.Vector2(mouse[0], mouse[1])

    if eval_toggle:
        pygame.draw.rect(screen,'#AE4ADB',(250,60,20,600))

        if eval != None:
            pygame.draw.rect(screen,'white',(252,62,16,298+eval/3))
            show_text(str(round(eval/60,2)),40,(200,720/2),'#AE4ADB')

    if len(moves) == 0:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("You Lost", True, 'red')
        textRect = text.get_rect()
        textRect.center = (1280 // 2, 720 // 2)

        screen.blit(transparent_surface, (0,720/2-100,600,100))
        screen.blit(text, textRect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
engine.quit()