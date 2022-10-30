# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:53:52 2022

@author: mario
"""

import numpy as np

def get_area(P1, P2, P3, P4):
    """ Retorna lista com as coordenadas dos vértices da área a levantar. 
        Recebe: P1...P4 - pontos que devem ser abrangidos pela área a levantar. 
    """
    #  Área a levantar (rectangular) definida por uma lista das coordenadas extremas dos quatro pontos (P1...P4) de modo a conter todos eles:
    #  
    #  area[0] .............. area[1]
    #  |                            |
    #  |                            |
    #  area[2] .............. area[3]
    #
    area = []
    area.append([min(P1[0], P2[0], P3[0], P4[0]), max(P1[1], P2[1], P3[1], P4[1])])
    area.append([max(P1[0], P2[0], P3[0], P4[0]), max(P1[1], P2[1], P3[1], P4[1])])
    area.append([max(P1[0], P2[0], P3[0], P4[0]), min(P1[1], P2[1], P3[1], P4[1])])
    area.append([min(P1[0], P2[0], P3[0], P4[0]), min(P1[1], P2[1], P3[1], P4[1])])
    
    return area    

# calculate flight plan

def get_first_foto (area, orientation, h, S2, q):
    """ Retorna: primeiro ponto de tomada de foto conforme a orientação de voo. 
        Recebe: area: foto de partida.
                Orientation - deverá ser negativo para voo E-W e qualquer outro valor para voo W-E
                h - altura do primeiro ponto
                S2 - comprimento da projeção da foto no solo (para determinação de F1_delta_y)
                q - sobreposição vertical entre faixas (para determinação de F1_delta_y)
    """
    F1_delta_y = S2 * (50. - q)/100. # distância entre a coordenada y da primeira foto e lado superior da area a levantar de modo a garantir uma margem de segurança de 50%-q
    if orientation <0: return (1, area[1][0], area[1][1] - F1_delta_y, h) #caso orientação seja <0 (E-W), F1 toma a posição do vértice superior direito
    return (1, area[0][0], area[0][1] - F1_delta_y, h) #caso orientação seja qualquer valor positivo (W-E), F1 toma a posição do vértice superior esquerdo
    
def get_next_foto_faixa (foto, A, B):
    """ Retorna: coordenadas da próxima foto numa fiada. 
        Recebe: foto: foto de partida. 
                A: incremento na coordenada y
                B: incremento na x
    """
    next_foto = (foto[0] + 1, foto[1] + B, foto[2] + A, foto[3])
    return next_foto

def get_plan_fotos (area, orientation, cota_media, s1, s2, mf, pixel_size, focal_distance, l, q):
    """ Retorna: lista de pontos de captura de fotografias (F1, F2, F3, ...). 
        Recebe: area - area a levantar [a calcular através de get_area()] 
                Orientation: [user input] deverá ser -1 para voo E-W e qualquer outro valor para voo W-E
                cota_media: [user input] cota média da área a levantar
                s1: [user input] largura do sensor (medido na horizontal) em px
                s2: [user input] comprimento do sensor (medido na vertical) em px
                focal_distance: [user input] distancia focal
                pixel_size: [user input] em micro-metros
    """
    S1 = s1 * mf * pixel_size * 10**(-6) # largura do elemento da imagem (horizontal) medido no terreno. Valor em metros
    S2 = s2 * mf * pixel_size * 10**(-6) # comprimento do elemento da imagem (vertical) medido no terreno. Valor em metros
    
    h = focal_distance * 10**(-3) * mf + cota_media # altura de voo tendo em conta a distância focal, modulo da escala da fotografia pretendida e cota média
    
    A = S2 * ( 1. - (q / 100.)) # distância entre pontos de captura de fotos entre fiadas
    B = S1 * ( 1. - (l / 100.)) # distância entre pontos de captura de fotos na mesma fiada
    
    Q = abs(area[0][1] - area[2][1]) # Diferença entre coordenadas y dos vértices laterais da área a levantar
    nfx = int((Q / A) + 1) # número de fiadas
    
    L = abs(area[0][0] - area[1][0]) # Diferença entre coordenadas x dos vértices superiores da área a levantar  
    nm = int((L / B) + 1) # número de fotos na mesma fiada
    
    fotos = [get_first_foto(area, orientation, h, S2, q)] #inicialização da lista de fotos, tendo a primeira foto calculada em função da área, orientação e altura. 
    # Nota: Altura será igual para todas as fotos no bloco
    
    for i in range(nfx): # loop para inserir pontos de captura de fotos em cada fiada 
        for j in range(nm - 1): # loop para inserir pontos de captura de fotos entre fiadas 
            if i%2 == 0: fotos.append(get_next_foto_faixa(fotos[-1], 0, orientation * B)) 
            if i%2 == 1: fotos.append(get_next_foto_faixa(fotos[-1], 0, - orientation * B)) #nas fiadas pares a orientação é invertida
        fotos.append(get_next_foto_faixa(fotos[-1], -A, 0))
    
    fotos.pop(-1) # hack para remover último ponto introduzido de forma não intencional (aspeto a melhorar...)
    
    return fotos

#calculate budget

def get_plan_budget(unit_cost_foto, unit_cost_flight_hour, flight_speed, s1, s2, pixel_size, mf, q, l, area, fotos):
    """ Retorna: (distancia, tempo, budget) distancia percorrida/duranção de voo no plano definido [km, h] e orçamento. 
        Recebe: flight_speed - velocidade de voo [km/h]
                A - distância entre faixas
                B - distancia entre fotos numa faixa
                nfx - número de fiadas
                nm - numero de modelos por fiada
    """
    S1 = s1 * mf * pixel_size * 10**(-6) # largura do elemento da imagem (horizontal) medido no terreno. Valor em metros
    S2 = s2 * mf * pixel_size * 10**(-6) # comprimento do elemento da imagem (vertical) medido no terreno. Valor em metros
    
    A = S2 * ( 1. - (q / 100.)) # distância entre pontos de captura de fotos entre fiadas
    B = S1 * ( 1. - (l / 100.)) # distância entre pontos de captura de fotos na mesma fiada
    
    Q = abs(area[0][1] - area[2][1]) # Diferença entre coordenadas y dos vértices laterais da área a levantar
    nfx = int((Q / A) + 1) # número de fiadas
    
    L = abs(area[0][0] - area[1][0]) # Diferença entre coordenadas x dos vértices superiores da área a levantar  
    nm = int((L / B) + 1) # número de fotos na mesma fiada
    
    # somamos: as nfx distâncias de B percorridas entre pontos de tomada de foto em cada fiada + 
    # distância aproximada de mudança de faixa (dada pela semi-circunferência pi*A/2) para nfx-1 mudanças de faixa (valor em m) 
    distance = nm * B * nfx + (np.pi/2.) * A * (nfx - 1)
    
    time = distance / (flight_speed * 1000)
    budget = nm * nfx * unit_cost_foto + time * unit_cost_flight_hour
    return (distance, time, budget)
