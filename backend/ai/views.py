from django.shortcuts import render
from django.http import HttpResponse
from .ai import easyAI, State, minimax, minimaxHard
from django.http import JsonResponse
import json
MAX = float('inf')
MIN = float('-inf')


def brojSlobodnihCrtica(s):
    suma = 0
    for c in s.crtice:
        if c == "2":
            suma += 1
    return suma    

def index(request):
    # response_data = {}
    # response_data['result'] = '1235'
    # if request.method == 'POST':
    #     print(request.body)
    #     print(json.dumps(response_data))
    #     #return HttpResponse(json.dumps(response_data))
    #     return JsonResponse(response_data)
    #     #return HttpResponse(response_data)
        
    # elif request.method == 'GET':
    #     print(1000)

    #     return JsonResponse(response_data)
    # elif request.method == 'PUT':
    #     return JsonResponse(response_data)


    
    crtice = request.GET.get('crtice')
    polja = request.GET.get('polja')
    player = request.GET.get('player')
    tezina = request.GET.get('tezina')
    columns = int(request.GET.get("columns"))
    depth = int(request.GET.get("dubina"))

    s1 = State(crtice, polja)
    
    
    dubinaIgre = depth
    
      
    if tezina == "medium":
        print("Dubina: " + str(depth))
        value, potez = minimax(s1, depth, MIN, MAX, player, columns, dubinaIgre)
        print("Stanje crtica je: " + str(crtice))
        print("Stanje polja je: " + str(polja))
        print("Heuristika je: " + str(value))
        print("Potez je: " + str(potez))

        return HttpResponse(potez)

    elif tezina == "easy":
        potezAI = easyAI(s1, player, columns)
        return HttpResponse(potezAI)

    else: # HARD TEZINA
        brojCrtica = brojSlobodnihCrtica(s1)
        print("Broj slobodnih crtica", brojCrtica)

    
      #promena dubine u zavisnosti od broja slobodnih crtica 
      #ove vrednosti su pronadjene eksperimentalnim putem
        if brojCrtica < 20 and brojCrtica >= 15:
            depth = 8
        elif brojCrtica < 15 and brojCrtica >= 10:
            depth = 9
        elif brojCrtica < 10:
            depth = 10
        dubinaIgre = depth # OVO JE ZA ISPISIVANJE

        print("Dubina: " + str(depth))
        value, potez = minimaxHard(s1, depth, MIN, MAX, player, columns, dubinaIgre)
        print("Stanje crtica je: " + str(crtice))
        print("Stanje polja je: " + str(polja))
        print("Heuristika je: " + str(value))
        print("Potez je: " + str(potez))
        return HttpResponse(potez)


    

