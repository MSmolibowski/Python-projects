from decimal import Subnormal
import math
import random
from unicodedata import decimal

import numpy as np
import time
from datetime import timedelta, datetime

#----------------Parameters to build graph-------------------------------



#------------------Generowanie grafu------------------------------------

def create_graph():
    basic_graph = np.zeros((verticle_number, verticle_number), dtype = int)     #tworzenie macierzy reprezentujacej graf wypełniony 0       

    for i in range(1, verticle_number):
        edge_weight = random.randint(min_weight, max_weight)    #wylosowanie wagi kosztu przejscia z jednego wierzcholka do drugiego
        basic_graph[i-1][i] = edge_weight                       #przypisanie wagi przejscia z X -> Y
        basic_graph[i][i-1] = edge_weight                       #przypisanie wagi przejscia z Y -> X
    
    return basic_graph



def check_and_fill(check_graph):                                            #sprawdzenie poprawności min i max krawędzi

    temp1 = check_graph

    for i in range(verticle_number):
        fill = edge_min_numb - len(temp1[i].nonzero()[0])               # tworzenie polaczen miedzy wierzcholkami (warunek)

        if fill > 0:
            rest = set(range(verticle_number)) - set(temp1[i].nonzero()[0]) - {i}
            while rest:
                j = random.choice(tuple(rest))              
                if len(temp1[:,j].nonzero()[0]) < max_weight:
                    fill_verticle = random.randint(min_weight, max_weight)
                    temp1[i][j] = fill_verticle
                    temp1[j][i] = fill_verticle
                    break
                rest.remove(j)
            else:
                raise Exception('Unnable to create graph')

    return temp1



#generator rozwiazan losowych:  pierwsze mrówki START!
#-----------------------Generator rozw losowych--------------------------
def scouting_ants():
    help_index = verticle_number - 1
    start_vertex = random.randint(0, help_index) #wybrac miejsce startu mrowki
    scouting_path = []                                  #sciezka jaka bedzie przechodzic zwiadowca (pierwsza mrowka)

    add_to_scouting_path = start_vertex
    scouting_path.append(add_to_scouting_path) #dodanie poczatkowego wierzchołka do rozwiązania (ścieżki)

    not_visited = set(range(verticle_number))         #lista nieodwiedzonych wierzchołków
    not_visited.remove(add_to_scouting_path)            #usuniecie wierzcholka startowego z listy wierzcholkow

    #print(f'start: {start_vertex}=> nieodwiedzeni {not_visited}')


    
    while not_visited:                        #szukaj sciezki dpokóki doputy nieużyto wszystkich wierzchołków
        
        neighbour_vertex = full_graph[add_to_scouting_path].nonzero()[0] #wyciagniecie sasiadow danego wierzcholka       
        missed_neigbours = tuple(not_visited & set(neighbour_vertex)) #nieodwiedzeni sasiedzi wierzcholka
        
        #print(f'{iter} NOT VISITED LIST: {not_visited}')
        #print(f'{iter} Wierzcholek w jakim jest mrowka: {add_to_scouting_path}')
        #print(f'{iter} Sasiedzi: {neighbour_vertex}')
        #print(f'{iter} Nieodwiedzeni sasiedz: {missed_neigbours}')
        
        if missed_neigbours:

            selected__neighbour = random.choice(missed_neigbours)      #wybieramy nieodwiedzony odcinek
            #print(f'{iter} nieodwiedzony => {selected__neighbour}')
        else:        
            selected__neighbour = random.choice(neighbour_vertex)       #losowanie sasiada do przejscia
            #print(f'{iter} odwiedzony sasiad => {selected__neighbour}')
                         
        #print("-------------------------------")
        #print(" ")
        
        if(selected__neighbour in not_visited):
            not_visited.remove(selected__neighbour)
        
        scouting_path.append(selected__neighbour)                               #dodanie wybranego wierzcholka do rozwiazania
        add_to_scouting_path = selected__neighbour                              #przejscie do wybranego wierzcholka
            
        
    return scouting_path



#--------------------------Metaheurystyka - Following ants-------------------

def meta_ants(chance):

    following_path = []                         #tworzone rozwiazanie
    help_index = verticle_number - 1

    start_vertex = random.randint(0, help_index) #wybrac miejsce startu mrowki
    add_to_following_path = start_vertex

    following_path.append(add_to_following_path) #dodanie poczatkowego wierzchołka do rozwiązania (ścieżki)

    following_not_visited = set(range(verticle_number))  #stworzenie  wierzch nieodwiedzonych
    following_not_visited.remove(add_to_following_path)
    
    while following_not_visited:                    #jedziemy dopóki doputy sa nieodwiedzone wierzch.
        
        roll = random.randint(0, 100)           #losowanie czy uzyc feromonow

        following_neighbour_vertex = full_graph[add_to_following_path].nonzero()[0] #wyciagniecie sasiadow danego wierzcholka (sasiadow nie wartosci feromonow)
        following_missed_neighbours = tuple(following_not_visited & set(following_neighbour_vertex))

        if following_missed_neighbours:
            
            if roll < chance:                       #uzycie feromonow dla NIEODWIEDZONYCH wierzch
                #---------------------wyciagniecie wart feromonow dla NIEODWIEDZONYCH wierzch i wyliczenie dla nich prawdopodobienstwa
                vertex_value = {}
                vertex_value = pheromone_matrix[add_to_following_path, following_missed_neighbours] #wartosci feromonow NIEODWIEDZONYCH wierz
                vertex_value_sum = sum(vertex_value)
                vertex_prob = np.round(vertex_value/vertex_value_sum * 100, decimals = 2)
                
                random_next_vertex = random.choices(following_missed_neighbours, weights=vertex_prob)   #losowanie nieodwiedzonego wierzch
                add_to_following_path = random_next_vertex[0] # [0] bo choiceS ! zwraca tablice
              
                #print(f'Nieodwiedzone wierzcholki: {following_missed_neighbours}')
                #print(f'wartosci feromonow: {vertex_value}')
                #print(f'prawdopodobienstwo: {vertex_prob}')
                #print(vertex_value[0])
                #print(f'suma wart: {vertex_value_sum}')
                #print(f'wylosowany {random_next_vertex}')

            else:                             #nieuzycie feromon dla NIEODWIEDZONYCH wierzch
                random_next_vertex = random.choice(following_missed_neighbours)
                add_to_following_path = random_next_vertex
                #print("Odwiedzony - bez feromonow")

        else:
   
            if roll < chance:                       #uzycie feromonow dla ODWIEDZONYCH wierzch
                
                vertex_value = {}
                vertex_value = pheromone_matrix[add_to_following_path, following_neighbour_vertex] #wartosci feromonow ODWIEDZONYCH wierz
                vertex_value_sum = sum(vertex_value)
                vertex_prob = np.round(vertex_value/vertex_value_sum * 100, decimals = 2)
                
                random_next_vertex = random.choices(following_neighbour_vertex, weights=vertex_prob)   #losowanie nieodwiedzonego wierzch
                add_to_following_path = random_next_vertex[0]
                
                #print(f'Odwiedzone wierzcholk: {following_neighbour_vertex}')
                #print(f'wartosci feromonow: {vertex_value}')
                #print(f'prawdopodobienstwo: {vertex_prob}')
                #print(vertex_value[0])
                #print(f'suma wart: {vertex_value_sum}')
                #print(f'wylosowany {random_next_vertex}')
            else:                                   #nieuzycie feromon dla nieodwiedzonych wierzch
                random_next_vertex = random.choice(following_neighbour_vertex)
                add_to_following_path = random_next_vertex
                #print("Nieodwiedzony - bez feromonow")



        if (add_to_following_path in following_not_visited):
            following_not_visited.remove(add_to_following_path)

        
        following_path.append(add_to_following_path)                              #i dodanie do rozwiazania
         
        #print('----------------------------------------------------------------------------------')        

    return following_path




#---------------------------Sumowanie kosztów----------------------------------
def count_cost(path):
    numb = np.empty(len(path) - 1, dtype = int)
    for i in range(0, len(path)-1):
        x = path[i]
        y = path[i+1]

        numb[i] = full_graph[x,y]

        if(i+1) % X_value == 0:
            back = math.ceil(X_value/2)
            v_lvl = len(full_graph[path[i+1]].nonzero()[0])

            numb[i] = numb[i] + 2 * numb[i+1 - back: i+1].sum() * v_lvl
    
    return numb.sum()



#--------------------------------------------nanoszenie feromonów----------------- #zmienic wartosci  nanoszone na macierz feromonow
def mark_pheromone(path, power):
    for i in range(0, len(path)-1):
        #increse = 1 * alfa
        pheromone_matrix[path[i]][path[i+1]] +=  power
        #j = i+1
        #print(f'v1: {path[i]} ===> {path[j]}')
    

    #sprawdzamy czy jakis wiersz nie potrzebuje wygladzenia

#-------------------------------------------Wygładzanie feromonow---------------------
def smoothie():
    for i in range(0, verticle_number-1):

        suma = sum(pheromone_matrix[i])
        search = suma * 0.1

        lovest = set(list(pheromone_matrix[i]))
        lovest.remove(0)
        lovest = min(lovest)

        if lovest < search:
            for j in range(0, verticle_number-1):
                if pheromone_matrix[i][j] > 0:
                    
                    pheromone_matrix[i][j] = lovest * (1 + math.log(pheromone_matrix[i][j] / lovest, go_smooth))


#-----------------------------------------------MAIN----------------------------------------------------
#------------------------------Generowanie instancji--------------------------------------------------------


#arg_to_change = input("Wpisz wartosc dla: czas  ")
#if  arg_to_change == '':
#    czas = czas
#else: 
#    czas = int(arg_to_change)

ants = 100               #liczba mrowek
verticle_number = 50    #liczba wierzcholkow w grafie

min_weight = 1          #minim waga przejścia daną krawędzią
max_weight = 100        #max waga przejścia daną krawędzią

X_value = 5                   # po ilu wierzcholkach jest wykonywana operacja na sumowanej sciezce

edge_min_numb = 6  #minimalna liczba krawędzi
edge_max_numb = 30     #max liczba krawędzi

pheromon_increase = 1     #wzmacnianie feromonów

pheromon_evaporate = 0.3    #wartosc parowania feromonów

go_smooth = 20              #wartosc wygladzania



#for G in range(0, 10): #generuj 10 grafow
graph = create_graph()
full_graph = check_and_fill(graph)
#czas = 30
juz = 0


Ilość_przelotów = 4
while juz < 9:              #ustawianie zmiennej

    if juz == 0:
        czas = 15
    if juz == 1:
        czas = 30
    if juz == 2:
        czas = 60
    if juz == 3:
       czas = 120
    if juz == 4:
        czas = 180
    #if juz == 5:
    #    czas = 300
    #if juz == 6:
    #    ants = 150
    #    czas = 300
    #if juz == 7:
    #    ants = 200
    #    czas = 300
    #if juz == 8:
    #    ants = 300
    #    czas = 300

    print(f'--------------------Badanie czasu :{czas}-------------------')
    calculate_data = []

    for G in range(0, Ilość_przelotów):      #10 przeszukiwan na tym samym grafie
        #------------------ZWIADOWCY------------

        scout_paths = []
        scout_counted = []
        for i in range(0, ants):
            temp_scout_path = scouting_ants()
            temp_scout_count = count_cost(temp_scout_path)

            scout_paths.append(temp_scout_path)
            scout_counted.append(temp_scout_count)

            #print(f'path {i} : cost: {scout_counted[i]} :: path {scout_paths[i]}')

        #----------sortowanie wyników---------------------------------

        scout_counted, scout_paths = zip(*sorted(zip(scout_counted, scout_paths )))  #sortowanie z neta

        #------------wybranie najlepszych 20%----------------       Poprawione

        best_twenty = math.ceil(ants * 0.2)
        scout_counted = scout_counted[0 : best_twenty]
        scout_paths = scout_paths[0 : best_twenty]
        best_scout = scout_counted[0]                       # najlepszy wynik zwiadowcow

        #---------------Pheromon matrix create------------------                    #do poprawy ??

        pheromone_matrix = np.zeros((verticle_number, verticle_number), dtype=float)
        pheromone_matrix[full_graph.nonzero()] = 1

        #------------Naniesienie feromonów na macierz--------------

        for i in range(0, len(scout_paths)):

            mark_pheromone(scout_paths[i], pheromon_increase)             #podaj sciezke i sile zwiekszania feromonow
            #print('pheromone map:')

        #print("Macierz feromonw (oznaczona)")
        #print(pheromone_matrix)

        #---------------------------Metaheurystyka start------------------------

        stop = datetime.now() + timedelta(seconds=czas)
        count = 1
        best_result = []
        best_ants_path = []
        best_cost_path = []
        best_result.append(best_scout)


        #wzrost szansy na feromony w czasie:

        while datetime.now() < stop:
            pheromonce_chance = ants * 0.1    #kiedy zwiekszyc szanse na uzycie feromonów

            meta_paths = []                 #tablice do zbierania rozwiazan
            meta_counted = []

            chance = 1
            yes = 1
            for i in range(0, ants):            #puszczamy mrowki szukajace rozwiazania

                if i > pheromonce_chance and yes == 1:
                    chance = 5
                    pheromonce_chance += ants * 0.3
                    yes += 1
                if i > pheromonce_chance and yes == 2:
                    chance = 15
                    pheromonce_chance += ants * 0.5  
                    yes += 1  

                if i > pheromonce_chance and yes == 3:
                    chance = 20
                    pheromonce_chance = ants * 0.7
                    yes += 1                 

                temp_meta_path = meta_ants(chance)
                temp_metha_cost = count_cost(temp_meta_path)
                
                meta_paths.append(temp_meta_path)
                meta_counted.append(temp_metha_cost)
                                          
            #----------------------sortowanie i wybranie najlepszej sciezki-----------

            meta_counted, meta_paths = zip(*sorted(zip(meta_counted, meta_paths )))  #sortowanie z neta

            best_twenty = math.ceil(ants * 0.2)
            meta_counted = meta_counted[0 : best_twenty]
            meta_paths = meta_paths[0 : best_twenty]

            for i in range(0, len(meta_paths)):
    
                mark_pheromone(meta_paths[i], pheromon_increase)             #podaj sciezke i sile zwiekszania feromonow
                #print('pheromone map:')

            if meta_counted[0] < best_result[0]:                #dodanie najlepszej sciezki do rozwiazania
                best_result.append(meta_counted[0])
                best_result.sort(reverse=False)
                #print(f'Ilosc mrowisk: {count} => Najlepsze rozwiazania: {best_result}')

            #-----------------poprawa feromonow na podstawie najlepszego wyniku z przelotu mrowek

            

            pheromone_matrix = pheromone_matrix - (pheromone_matrix * pheromon_evaporate).round(decimals=2)               #parowanie feromonow
            smoothie() 
            pheromone_matrix = pheromone_matrix.round(decimals=2)
            
            count += 1
        calculate_data.append(best_result[0])
        print(f'Próba {juz} : Bestresult for {czas} przejscie {G} ===> {best_result[0]}')
        print(f'Best results:{calculate_data}')
        #print(f'szanse: {chance}')
    srednia_wynikow = sum(calculate_data)/Ilość_przelotów
    print(' ')

    print("PODSUMOWANIE")
    print("-------------------------------")
    print(f'Szansa: {chance}: Sredni koszt sciezki dla ants: {czas}, mrowki {ants}, l.wierzch: {verticle_number}')
    print(srednia_wynikow)
    print("-------------------------------")
    
    fh = open(f'1111111111111.BadanieCzasu_{czas}_Mrowki_{ants}.txt', 'w')
    fh.write(f'Czas: {czas}, Mrowki {ants}, evaporate {pheromon_evaporate}, L.wierzch: {verticle_number}\n')
    fh.write(f'Sredni koszt: {srednia_wynikow}\n')
    
    for cost in calculate_data:
        line = str(cost)
        fh.write(line)
        fh.write('\n')
    fh.close
    juz +=1  





