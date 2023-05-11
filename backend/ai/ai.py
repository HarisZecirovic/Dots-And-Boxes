import math
import random
import time


class State:
    """
    Stanje igre 
    """
    def __init__(self, crtice, polja):
        self.crtice = crtice
        self.polja = polja

    def __str__(self):
        return self.crtice + " " + self.polja

# Vraca listu svih mogucih poteza jednog stanja


def actions(s):
    """
    Svi moguci potezi koji mogu da se odigraju
    """
    moves = []
    for i in range(len(s.crtice)):
        if s.crtice[i] == "2":
            moves.append(i)
    return moves

# def actions2(s):
#     moves = []
    
#     #columns = 3
#     for polje in range(len(s.polja)):
#         if s.polja[polje] == "2":
#             crte_oko_polja =  math.floor(polje / columns) * (columns + 1) + polje
#             broj_slobodnih = 0
#             indeksi = [crte_oko_polja, crte_oko_polja + columns,
#                 crte_oko_polja + columns + 1, crte_oko_polja + 2 * columns + 1]
#             for i in indeksi:
#                 if s.crtice[i] == "2":
#                     broj_slobodnih += 1

#             if broj_slobodnih != 2:
#                 for i in indeksi:
#                     if s.crtice[i] == "2":
#                         moves.append(i)
#     if len(moves) == 0:
#         return actions(s)
#     else:
#         return moves                    

def moveOrdering(s, player, columns):
    list1 = []
    list2 = []
    pravaLista = []
    moves = actions(s)
    for move in moves:
        stanje, polje = result(s, move, player, columns )
        if polje:
            list1.append(move)
        else:
            list2.append(move)
    pravaLista = list1 + list2
    return pravaLista           

def osvojenaTrecaCrtica(s, potez, columns):
    for polje in range(len(s.polja)):
        crta_iznad = math.floor(polje / columns) * (columns + 1) + polje
        broj_slobodnih = 0
        indeksi = [crta_iznad, crta_iznad + columns,
                    crta_iznad + columns + 1, crta_iznad + 2 * columns + 1] 

        if potez in indeksi:
            for i in indeksi:
                if s.crtice[i] == "2":
                    broj_slobodnih += 1
            if broj_slobodnih == 2:
                return True                    
    return False

def actions2(s, columns):
    potezi_koji_prave_trecu_crticu = []
    potezi_koji_ne_prave_trecu_crticu = []
    moves = actions(s)
    for move in moves:
        if osvojenaTrecaCrtica(s, move, columns):
            potezi_koji_prave_trecu_crticu.append(move)
        else:
            potezi_koji_ne_prave_trecu_crticu.append(move)

    if len(potezi_koji_ne_prave_trecu_crticu) > 0:
        return potezi_koji_ne_prave_trecu_crticu
    else:
        return potezi_koji_prave_trecu_crticu                



def result(s, a, player, columns):
    """
    Proveravamo da li smo osvojili neko polje
    """
   
    crtice = s.crtice[:a] + player + s.crtice[a + 1:]
    #  pOLJA TREBA DA SE MENJAJU ISTO AKO JE OSVOJIO NEKO POLJE
    polja = s.polja
    s2 = State(crtice, polja)
    osvojenoPolje = False  # pamtimo da li smo osvojili neko polje kad smo izvrsili ovaj potez
    for i in range(len(polja)):
        if s2.polja[i] == "2" and osvojenoPoljeSaIndeksom(s2, i, columns):
            polja = polja[:i] + player + polja[i + 1:]
            osvojenoPolje = True
    s2.polja = polja
    return s2, osvojenoPolje


def osvojenoPoljeSaIndeksom(s, indeks, columns):
    
    idCrticeIznad = math.floor(indeks / columns) * (columns + 1) + indeks
    indeksi = [idCrticeIznad, idCrticeIznad + columns,
               idCrticeIznad + columns + 1, idCrticeIznad + 2 * columns + 1]
    for i in indeksi:
        if s.crtice[i] == "2":
            return False
    return True


def terminalTest(s, depth):
    if depth == 0:  
        return True
    for polje in s.polja:
        if polje == "2":
            return False
    return True

#vraca suma mojih polja - suma protivnikovih polja
#bolji je od utility2 po tome sto tacnije opisuje vrednost nekog stanja
#npr utility2 bi za neka stanja vratio 0, dok utility za hard bi vratio -1,2,3.
#i lako bismo znali sta je bolje
def utility(s, player):  # TODO
    suma = 0 
    for polje in s.polja:
        if polje == player:
            suma += 1
        elif polje != "2":
            suma -= 1
    return suma

#utility2- Ukoliko je neko stanje S dovelo do pobede igraca player onda vraca 1
#ako je pobedio njegov protivnik vraca -1
#u svim ostalim slucajevima vraca 0
def utility2(s, player):
    suma1 = 0
    suma2 = 0
    for polje in s.polja:
        if polje == player:
            suma1 +=1
        elif polje != "2":
             suma2 += 1
    broj_polja = len(s.polja)
    if suma1 > broj_polja/2:
        return 1
    elif suma2 > broj_polja/2:
        return -1 
    else:
        return 0        


def easyAI(s, player, columns):
    moves = actions(s)
    for move in moves:
        newState, osvojenoPolje = result(s, move, player, columns)
        if osvojenoPolje:
            return move
    return moves[random.randint(0, len(moves) - 1)]

counter = 0
def minimax(s,depth,alpha, beta, player, columns,dubina):
    potezi = actions(s)

    for i in potezi:
        newState, osvojenoPolje = result(s, i, player, columns)
        if osvojenoPolje:
            return utility2(newState,"1"),i
        
    global counter
    counter += 1
    dubinaIgre = dubina
    value = potez = 0
    if terminalTest(s, depth): 
        return utility2(s, "1"), 0
    if player == "1":
        maxEval = float('-inf')
        bestMove = None
        moves = actions2(s, columns)
        igrac = 1 - int(player)
        for move in moves:
            rezultat, osvojenoPolje = result(s,move,player, columns)
            if osvojenoPolje:
                value, potez = minimax(rezultat, depth - 1, alpha, beta, player, columns, dubina)
            else:
                value, potez = minimax(rezultat, depth - 1,alpha, beta, str(igrac), columns,dubina)    
            maxEval = max(maxEval, value)
            alpa = max(alpha, value)
            if beta <= alpa:
                break
            if maxEval == value:
                bestMove = move
            if depth == dubinaIgre:
                print("Potez je: " + str(move) + " ,a heuristika je: " + str(value) + ", novo stanje je: " + str(rezultat))
        return maxEval, bestMove            
    else:
        minEval = float('inf')
        bestMove = None
        moves = actions2(s, columns)
        igrac = 1 - int(player)
        for move in moves:
            rezultat, osvojenoPolje = result(s,move,player, columns)
            if osvojenoPolje:
                value, potez = minimax(rezultat,depth - 1,alpha, beta, player, columns, dubinaIgre)
            else:    
                value, potez = minimax(rezultat, depth - 1,alpha, beta, str(igrac), columns, dubinaIgre)
            minEval = min(minEval, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
            if minEval == value:
                bestMove = move

        return minEval, bestMove 

def minimaxHard(s,depth,alpha, beta, player, columns, dubina):
    
    global counter
    counter += 1
    dubinaIgre = dubina
    value = potez = 0
    if terminalTest(s, depth): 
        return utility(s, "1"), 0
    if player == "1":
        maxEval = float('-inf')
        bestMove = None  
        if depth > 2:
            moves = moveOrdering(s, player, columns) 
        else:
            moves = actions(s)       
        igrac = 1 - int(player)
        for move in moves:
            rezultat, osvojenoPolje = result(s,move,player, columns)
            if osvojenoPolje:
                value, potez = minimaxHard(rezultat, depth - 1, alpha, beta, player, columns, dubinaIgre)
            else:
                value, potez = minimaxHard(rezultat, depth - 1,alpha, beta, str(igrac), columns, dubinaIgre)    
            maxEval = max(maxEval, value)
            alpa = max(alpha, value)
            if beta <= alpa:
                break
            if maxEval == value:
                bestMove = move
            if depth == dubinaIgre:
                print("Potez je: " + str(move) + " ,a heuristika je: " + str(value) + ", novo stanje je: " + str(rezultat))
        return maxEval, bestMove            
    else:
        minEval = float('inf')
        bestMove = None   
        if depth > 2:
            moves = moveOrdering(s, player, columns) 
        else:
            moves = actions(s)  
        igrac = 1 - int(player)
        for move in moves:
            rezultat, osvojenoPolje = result(s,move,player, columns)
            if osvojenoPolje:
                value, potez = minimaxHard(rezultat,depth - 1,alpha, beta, player, columns, dubinaIgre)
            else:    
                value, potez = minimaxHard(rezultat, depth - 1,alpha, beta, str(igrac), columns, dubinaIgre)
            minEval = min(minEval, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
            if minEval == value:
                bestMove = move

        return minEval, bestMove 



if __name__ == "__main__":
    test_crtice = "021200122210"
    test_polja = "2222"

    s1 = State(test_crtice, test_polja)
    print(str(s1))
    moves = moveOrdering(s1, "1" , 3)
    print(moves)
    moves = actions(s1)

    for move in moves:
        newState, osvojenoPolje = result(s1, move, "0",2)
        print(str(move) + " a rezultat je: " + str(newState) +
              " a heuristika je: " + str(utility(newState, "0")))
        print(terminalTest(newState, 1))

    # test za easyAI
    print(f'Potez koji ce AI da odigra {easyAI(s1, "0", 3)}')

    #test za Medium
    start_time = time.time()
    AI = minimaxHard(s1, 3,-100,100, "1", 2,3)
    t = time.time() - start_time
    print(AI)
    print(  f"Broj cvorova: {counter}, vreme: {t}, brzina {counter / t} cvorova u sekundi")
    print("Counter: "+ str(counter))

    # da isprobam f-ju terminaTest
    s1.polja = "000000000"
    print(terminalTest(s1, 1))
    print(utility2(s1,"1"))
    value,potez= minimax(s1,1,-100,100,"1",2,1)
    print(value,potez)