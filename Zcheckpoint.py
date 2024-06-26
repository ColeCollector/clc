import time
import heatmap
import copy

class chess():
    #remember:
    #lowercase = black
    #upercase = white


    xaxis = ['a','b','c','d','e','f','g','h','i']
    yaxis = ['1','2','3','4','5','6','7','8']


    def fen2pos(self,fen):
        positions = []
        #castle = {"K":False,"Q":False,"k":False,"q":False}
        number = 8
        column = 1
        letters = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}


        for i in range(64):
            try:
                column+=int(fen[i]) 
            except:
                if fen[i] == " ":
                    break
                elif fen[i] == "/":
                    number-=1
                    column = 1
                else: 
                    positions.append(f"{fen[i]}{letters[column]}{number}")
                    column +=1
        


        #for i in fen.split(" ")[2]:
        #    castle[i]=True
            
        return positions

    def pos2fen(self,pos,turn):
        letters = ['a','b','c','d','e','f','g','h','i']
        x = ""
        row = 8
        collumn = -1
        pos.append({" i1":[]})

        for i in pos:
            switch = False
            if int(list(i.keys())[0][2]) != row:
                row-=1

                if collumn!=7:
                    if 0!=letters.index(list(i.keys())[0][1]):
                        x = f"{x}{-collumn+7}"
                    else:
                        switch = True
                        x = f"{x}{-collumn+7}"

                while int(list(i.keys())[0][2]) != row:
                    x = f"{x}/8"
                    row-=1

                if switch == True:
                    x = f"{x}/{list(i.keys())[0][0]}"

                if collumn !=7 and 0!=letters.index(list(i.keys())[0][1]):
                    x = f"{x}/{letters.index(list(i.keys())[0][1])}{list(i.keys())[0][0]}"

                if collumn==7:
                    if 0!=letters.index(list(i.keys())[0][1]):
                        x = f"{x}/{letters.index(list(i.keys())[0][1])}{list(i.keys())[0][0]}"
                    else:
                        x = f"{x}/{list(i.keys())[0][0]}"
                

            else:
                if collumn+1!=letters.index(list(i.keys())[0][1]):
                    x = f"{x}{letters.index(list(i.keys())[0][1])-collumn-1}{list(i.keys())[0][0]}"
                else:
                    x = f"{x}{list(i.keys())[0][0]}"
            
    
            collumn = letters.index(list(i.keys())[0][1])
        

        
        x += f"{self.turn[0]} KQkq - 0 1"
        return x

    def rook(self,square,board1,board2):

        first = square[:1]
        last = square[1:]
        
        available = []
        vertical = [True,True]
        horizontal = [True,True]


        for i in range(1,8):

            if vertical[0] == True and int(last[1])+i<=8:
                #up
                pos = f"{last[0]}{int(last[1])+i}"
                
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    vertical[0] = False
                else:
                    available.append(f"{first.upper()}{pos}")
            
            if vertical[1] == True and int(last[1])-i>0:
                #down
                pos = f"{last[0]}{int(last[1])-i}"
                
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    vertical[1] = False
                else:
                    available.append(f"{first.upper()}{pos}")

            if horizontal[0] == True and self.xaxis.index(last[0])+i<8:
                #left
                pos = f"{self.xaxis[self.xaxis.index(last[0])+i]}{last[1]}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    horizontal[0] = False
                else:
                    available.append(f"{first.upper()}{pos}")

            if horizontal[1] == True and self.xaxis.index(last[0])-i>=0:
                #right
                pos = f"{self.xaxis[self.xaxis.index(last[0])-i]}{last[1]}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    horizontal[1] = False
                else:
                    available.append(f"{first.upper()}{pos}")


        available.sort()
        return {square:available}

    def knight(self,square,board1,board2):

        available = []

        currentx = square[1:][0]
        currenty = square[1:][1]
        first = square[:1]
        
        xnum = self.xaxis.index(currentx)
        ynum = self.yaxis.index(currenty)

        for i in range(0,8):
            x = self.xaxis[i]
            differ = abs(xnum - self.xaxis.index(x))

            if differ == 2:

                if ynum + 2 < 9:
                    pos = f"{x}{ynum + 2}"

                    if pos in board2:
                        if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                                available.append(f"Nx{pos}")

                    else:
                        available.append(f"N{pos}")

                if ynum > 0: 
                    pos = f"{x}{ynum}"

                    if pos in board2:
                        if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                                available.append(f"Nx{pos}")

                    else:
                        available.append(f"N{pos}")

            if differ == 1:
                if ynum + 3 < 9:
                    pos = f"{x}{ynum + 3}"

                    if pos in board2:
                        if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                                available.append(f"Nx{pos}")

                    else:
                        available.append(f"N{pos}")

                if ynum - 1 > 0:
                    pos = f"{x}{ynum - 1}"

                    if pos in board2:
                        if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                                available.append(f"Nx{pos}")
                    else:
                        available.append(f"N{pos}")

        if str(square) in available:
            available.remove(str(square))
        
        available.sort()

        return {square:available}

    def bishop(self,square,board1,board2):

        available = []
        top = [True,True]
        bottom = [True, True]
        
        xnum = self.xaxis.index(square[1:][0])
        ynum = self.yaxis.index(square[1:][1])

        first = square[:1]

        for i in range(0,8):
            if ynum+2+i<=8 and xnum-i-1>=0 and top[0] == True:
                #top left
                pos = f"{self.xaxis[xnum-i-1]}{ynum+2+i}"
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    top[0] = False

                else:
                    available.append(f"{first.upper()}{pos}")

            if ynum+2+i<=8 and xnum+i+1<8 and top[1] == True:
                pos = f"{self.xaxis[xnum+i+1]}{ynum+2+i}"
                #top right
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    top[1] = False

                else:
                    available.append(f"{first.upper()}{pos}")

            if ynum-i>0 and xnum-i-1>=0 and bottom[0] == True:
                #bottom left
                pos = f"{self.xaxis[xnum-i-1]}{ynum-i}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    bottom[0] = False

                else:
                    available.append(f"{first.upper()}{pos}")
            

            if ynum-i>0 and xnum+i+1<8 and bottom[1] == True:
                #bottom right
                pos = f"{self.xaxis[xnum+i+1]}{ynum-i}"
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    bottom[1] = False

                else:
                    available.append(f"{first.upper()}{pos}")


        available.sort()

        return {square:available}

    def pawn(self,square,board1,board2):
        available = []
    
        xnum = self.xaxis.index(square[1:][0])+1
        ynum = self.yaxis.index(square[1:][1])+1


        #making pawns go different directions based on color
        if square[0] == "P":
            x = 1
            special = [2,8,5]
            
        else:
            x= -1
            special = [7,1,4]

        if f"{square[1]}{ynum+1*x}" not in board2:
            if ynum+1*x!=special[1]:
                available.append(f"{square[1]}{ynum+1*x}")

                #double pawn move
                if f"{square[1]}{ynum+2*x}" not in board2 and ynum==special[0]:
                    available.append(f"{square[1]}{ynum+2*x}")
            else:
                available.append(f"{square[1]}{ynum+1*x}=Q")


        if xnum<8:
            if f"{self.xaxis[xnum]}{ynum+1*x}" in board2:
                
                #pawn takes right
                if (board1[board2.index(f"{self.xaxis[xnum]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                    if ynum+1*x!= special[1]:
                        available.append(f"{square[1]}x{self.xaxis[xnum]}{ynum+1*x}")

                    else:
                        available.append(f"{square[1]}x{self.xaxis[xnum]}{ynum+1*x}=Q")


        if xnum-2>=0:
            if f"{self.xaxis[xnum-2]}{ynum+1*x}" in board2:

                #pawn takes left
                if (board1[board2.index(f"{self.xaxis[xnum-2]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                    if ynum+1*x!=special[1]:
                        available.append(f"{square[1]}x{self.xaxis[xnum-2]}{ynum+1*x}")
                    else:
                        available.append(f"{square[1]}x{self.xaxis[xnum-2]}{ynum+1*x}=Q")



        
        available.sort()
        return {square:available}

    def king(self,square,board1,board2):
        available = []

        xnum = self.xaxis.index(square[1:][0])
        ynum = self.yaxis.index(square[1:][1])

        def check(pos):
            if pos in board2:
                if (board1[board2.index(pos)])[:1].isupper() != square[:1].isupper():
                    available.append(f"Kx{pos}")
            else:
                available.append(f"K{pos}")

        if ynum+1 < 8:
            #up
            
            pos = f"{self.xaxis[xnum]}{self.yaxis[ynum+1]}"
            check(pos)
            if xnum+1 < 8:
                pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum+1]}"
                check(pos)

            if xnum-1 > 0:  
                pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum+1]}"  
                check(pos)
                
        if ynum-1 > 0:
            #down
            pos = f"{self.xaxis[xnum]}{self.yaxis[ynum-1]}"
            check(pos)

            if xnum+1 < 8:
                pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum-1]}"
                check(pos)

            if xnum-1 > 0:  
                pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum-1]}"  
                check(pos)

        if xnum+1 < 8:
            #right
            pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum]}"
            check(pos)

        if xnum-1 > 0:  
            #left
            pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum]}"
            check(pos)

            
        available.sort()
        return {square:available}

    def __init__(self,board):
        movecount = [0,0]
        pgn = []
        self.turn = "white"
        #lastmove = None
        while True:
            def findmoves(board):
                moves = []
                board2 = []

                #an homage to andrew
                tally = 0

                for i in board:
                    board2.append(i[1:])

                if self.turn == "white":
                    piece = ["B","R","N","Q","P","K"]

                elif self.turn == "black":
                    piece = ["b","r","n","q","p","k"]

                for i in board:

                    if i[:1] == piece[0]:
                        moves.append(self.bishop(board[tally],board,board2))

                    elif i[:1] == piece[1]:
                        moves.append(self.rook(board[tally],board,board2))

                    elif i[:1] == piece[2]:
                        moves.append(self.knight(board[tally],board,board2))
                    
                    elif i[:1] == piece[3]:
                        queen = self.bishop(board[tally],board,board2)[i]+self.rook(board[tally],board,board2)[i]
                        queen.sort()
                        moves.append({i:queen})

                    elif i[:1] == piece[4]:
                        moves.append(self.pawn(board[tally],board,board2)) 

                    elif i[:1] == piece[5]:
                        moves.append(self.king(board[tally],board,board2))

                    else:
                        moves.append({board[tally]:[]})

                    tally+=1
                return moves

            moves = findmoves(board)

                
            allmoves = []
            dupes = []

            if self.turn == "white":
                switch = True
            else:
                switch = False

            for j in moves:
                if list(j.keys())[0][0].isupper() == switch:
                    for k in (list(j.values())[0]):
                        if k in allmoves:
                            dupes.append(k)
                        else:
                            allmoves.append(k)

            allmoves = []

            for j in moves:
                if list(j.keys())[0][0].isupper() == switch:
                    for k in (list(j.values())[0]):
                        if k in dupes:
                            list(j.values())[0][list(j.values())[0].index(k)] = f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}"


            for i in moves:
                if (self.turn == "white" and list(i.keys())[0][0].isupper() == True) or (self.turn == "black" and list(i.keys())[0][0].isupper() == False):
                    for j in list(i.values())[0]:
                        allmoves.append(j)


            def evaluate(moves):
                evaluation = 0

                for i in moves:

                    temp = list(i.keys())[0] 
                    heatm = heatmap.PieceMap(temp)
                    heat = heatm[0]
                    evaluation += heatm[1]*10
                    evaluation += heat[8-int(temp[-1])][int(self.xaxis.index(temp[-2]))]


                return evaluation
            
            devaluation = []
            evaluation = []
            depth1 = []
            movecopy = copy.copy(moves)
            stop = [False,False]
            

            
            for move in allmoves:

                if move == allmoves[-1]:
                    stop[0] = True

                moves = copy.copy(movecopy)

                #if capture then 50 move rule resets
                #if "x" in move:
                #    movecount[1] = 0


                take = None
                for i in moves:
                    if move in list(i.values())[0]:
                        if list(i.keys())[0][0].isupper() == switch:
                            #if pawn promotion spawn a queen and get rid of pawn
                            if "=" in move:
                                if list(i.keys())[0][0].isupper():
                                    move = "Q" + move[-4] + move[-3]
                                else:
                                    move = "q" + move[-4] + move[-3]   
                            else:
                                move = list(i.keys())[0][0]+move[-2]+move[-1]
                            
                            original = i
                    

                    if list(i.keys())[0][1:] == move[-2]+move[-1]:
                        take = i
                

                #if pawn moves 50 move rule resets
                if take != None:
                    moves.remove(take)

                moves.remove(original)
                moves.append({move:""})

                
                def depth():
                    depthboard = []

                    for i in moves:
                        depthboard.append(list(i.keys())[0])
                    
                    #looking at the position from black's perspecifive
                    if self.turn == "white":
                        self.turn = "black"
                    else:
                        self.turn = "white"

                    newboard = findmoves(depthboard)
                    
                    if self.turn == "black":
                        self.turn = "white"
                    else:
                        self.turn = "black"


                    return newboard
                    

                depth1.append(depth())



            
            #worst code ever:
                
            if self.turn == "white":
                self.turn = "black"
            else:
                self.turn = "white"

            counter = 0

            for dmoves in depth1:

                
                dallmoves = []
                dupes = []
                for j in dmoves:
                    if list(j.keys())[0][0].isupper() != switch:
                        for k in (list(j.values())[0]):
                            if k in dallmoves:
                                dupes.append(k)
                            else:
                                dallmoves.append(k)

                dallmoves = []

                for j in dmoves:
                    if list(j.keys())[0][0].isupper() != switch:
                        for k in (list(j.values())[0]):
                            if k in dupes:
                                list(j.values())[0][list(j.values())[0].index(k)] = f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}"


                for i in dmoves:
                    if (self.turn == "white" and list(i.keys())[0][0].isupper() == True) or (self.turn == "black" and list(i.keys())[0][0].isupper() == False):
                        for j in list(i.values())[0]:
                            dallmoves.append(j)

                
                dmovecopy = copy.copy(dmoves)

                devaluation = []
                stop = [False,False]

                for move in dallmoves:
                    if move == dallmoves[-1]:
                        stop[0] = True

                    dmoves = copy.copy(dmovecopy)


                    take = None
                    for i in dmoves:
                        if move in list(i.values())[0]:
                            if list(i.keys())[0][0].isupper() != switch:
                                #if pawn promotion spawn a queen and get rid of pawn
                                if "=" in move:
                                    if list(i.keys())[0][0].isupper():
                                        move = "Q" + move[-4] + move[-3]
                                    else:
                                        move = "q" + move[-4] + move[-3]   
                                else:
                                    move = list(i.keys())[0][0]+move[-2]+move[-1]
                                
                                original = i
                        

                        if list(i.keys())[0][1:] == move[-2]+move[-1]:
                            take = i

                    if take != None:
                        dmoves.remove(take)

                    dmoves.remove(original)
                    dmoves.append({move:""})
                    


                    devaluation.append(evaluate(dmoves))

                    #at the end of the loop pick the best move
                    if stop[0] == True and stop[1] == False:
                        stop[1] = True
                        
                        #minmax algorithm
                        if self.turn == "white":
                            dallmoves.append(dallmoves[devaluation.index(max(devaluation))])

                        else:
                            dallmoves.append(dallmoves[devaluation.index(min(devaluation))])

                
                if self.turn == "white":
                    evaluation.append(max(devaluation))
                else:
                    evaluation.append(min(devaluation))


                #if self.turn == "white":
                    #print(allmoves[counter],move,max(devaluation))
                #else:
                    #print(allmoves[counter],move,min(devaluation))

                counter+=1

            if self.turn == "white":
                move = allmoves[evaluation.index(min(evaluation))]
            else:
                move = allmoves[evaluation.index(max(evaluation))]




            if move == allmoves[-1]:
                stop[0] = True

            moves = copy.copy(movecopy)

            #if capture then 50 move rule resets
            #if "x" in move:
            #    movecount[1] = 0

            take = None
            for i in moves:
                if move in list(i.values())[0]:
                    if list(i.keys())[0][0].isupper() == switch:
                        #if pawn promotion spawn a queen and get rid of pawn
                        if "=" in move:
                            if list(i.keys())[0][0].isupper():
                                move = "Q" + move[-4] + move[-3]
                            else:
                                move = "q" + move[-4] + move[-3]   
                        else:
                            move = list(i.keys())[0][0]+move[-2]+move[-1]
                        
                        original = i
                

                if list(i.keys())[0][1:] == move[-2]+move[-1]:
                    take = i

            #if pawn moves 50 move rule resets

            if take != None:
                moves.remove(take)

            moves.remove(original)
            moves.append({move:""})


            

            #print(f"\n\nchosen move:{allmoves[evaluation.index(max(evaluation))]}")


            if self.turn == "white":
                pgn.append(allmoves[evaluation.index(min(evaluation))])
                #print(f"chosen move:{pgn[-1]}")
                #lastmove = pgn[-1]

            else:
                pgn.append(allmoves[evaluation.index(max(evaluation))])
                #print(f"chosen move:{pgn[-1]}")
                #lastmove = pgn[-1]

            movecount[1] +=1
            movecount[0] +=1

            
            king = [False,False]



            #print("\n\n")
            for i in moves:
                if list(i.keys())[0][0] == "K":
                    king[0] = True
                elif list(i.keys())[0][0] == "k":
                    king[1] = True


            if king[1] == False:
                print("White won!")
                break

            elif king[0] == False:
                print("Black won!")
                break 
            
            #After 100 half moves the game ends by draw
            if movecount[1] == 50:
                print("Draw by 50 move rule")
                break
    

            board = []

            for i in range(len(moves)):
                board.append(list(moves[i].keys())[0])


        for i in range(len(pgn)):
            if i%2==0:
                print(f"{int((i+2)/2)}. {pgn[i]}",end=" ")
            else:
                print(pgn[i],end=" ")


        print("\n\n")
        
#Positions I used to test for bugs
#board = self.fen2pos("r1B1k2r/ppPp1p1n/n3p1p1/6Q1/qPq5/N1B5/1P2PPPP/R3K2R w KQkq - 0 1")
#board = self.fen2pos("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board = self.fen2pos("k7/8/8/8/3B4/8/8/7K w - - 0 1")
#board = self.fen2pos("r3k2r/pQpp1p1n/n1P1p1pN/8/qP3B2/N1B1b3/1PK1PPPP/R6R w HAkq - 0 1")
#board = self.fen2pos("2q5/4q3/8/1p2R1q1/q1R5/8/2q1p3/k6K w - - 0 1")
#board = self.fen2pos ("rnbqkbnr/pppp1ppp/8/8/4pP2/6PP/PPPPP3/RNBQKBNR b KQkq f3 0 3")
#board = self.fen2pos("7k/5Q2/4q3/4K3/8/8/8/8 w - - 0 1")


start = time.time()
for i in range(1):
    board = chess.fen2pos(None,"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR - 0 1")
    chess(board)

print(f"\n\nProgram ran for {round((time.time()-start),3)} seconds\n")