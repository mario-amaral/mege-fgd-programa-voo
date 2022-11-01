# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:53:52 2022
Programa plano de voo: modulo de cálculo
Contem as funções de cálculo do plano de voo com base nos dados de input do utilizador
@author: Mario Amaral
"""


def get_area(P1, P2, P3, P4):
    """Retorna lista com as coordenadas dos vértices da área a levantar.
       :P1...P4: pontos que devem ser abrangidos pela área a levantar Pi = (Pi_x, Pi_y)
    """
    # Área a levantar (rectangular) definida por uma lista das coordenadas extremas dos quatro pontos (P1...P4) de
    # modo a conter todos eles:
    #  
    #  area[0] .............. area[1]
    #  |                            |
    #  |                            |
    #  area[2] .............. area[3]
    #
    area = [[min(P1[0], P2[0], P3[0], P4[0]), max(P1[1], P2[1], P3[1], P4[1])],
            [max(P1[0], P2[0], P3[0], P4[0]), max(P1[1], P2[1], P3[1], P4[1])],
            [max(P1[0], P2[0], P3[0], P4[0]), min(P1[1], P2[1], P3[1], P4[1])],
            [min(P1[0], P2[0], P3[0], P4[0]), min(P1[1], P2[1], P3[1], P4[1])]]

    return area


def get_first_foto(area, orientation, H, S2, q, B):
    """ Função auxiliar de get_plan_fotos. Retorna primeiro ponto de tomada de foto conforme a orientação de voo.
        :area: lista dos vértices da área a levantar
        :orientation: valor negativo para voo E-W e valor zero ou positivo para voo W-E
        :H: altura do primeiro ponto
        :S2: comprimento da projeção da foto no solo (para determinação de F1_delta_y)
        :q: sobreposição vertical entre faixas (para determinação de F1_delta_y)
    """
    # F1_delta_y dá-nos a distância entre a coordenada y da primeira foto e lado superior da area a levantar de modo
    # a garantir uma margem de segurança de 20% de S2
    F1_delta_y = S2 * 0.3

    # F1_starting_x dá-nos a coordenada x de partida da primeira foto de modo a garantir é capturada uma foto a uma
    # distância B do limite lateral da área a levantar
    F1_starting_x = B

    if orientation < 0: return (1, area[1][0] + F1_starting_x, area[1][1] - F1_delta_y,
                                H)  # caso orientação seja <0 (E-W), F1 toma a posição do vértice superior direito
    return (1, area[0][0] - F1_starting_x, area[0][1] - F1_delta_y,
            H)  # caso orientação seja qualquer valor positivo (W-E), F1 toma a posição do vértice superior esquerdo


def get_next_foto_faixa(foto, A, B):
    """Função auxiliar de get_plan_fotos. Retorna coordenadas da próxima foto numa fiada.
       :foto: foto de partida.
       :A: distância entre faixas (incremento na coordenada y)
       :B: distânmcia entre pontos de captura de foto na mesma faixa (incremento na coordenada x)
    """
    next_foto = (foto[0] + 1, foto[1] + B, foto[2] + A, foto[3])
    return next_foto


def get_plan_fotos(area, orientation, cota_media, s1, s2, pixel_size, focal_distance, mf, l, q):
    """ Retorna lista de pontos de captura de fotografias (F1, F2, F3, ...).
        :area: area a levantar [a calcular através de get_area()]
        :orientation: [user input] deverá ser -1 para voo E-W e qualquer outro valor para voo W-E
        :s1: [user input] largura do sensor (medido na horizontal) em px
        :s2: [user input] comprimento do sensor (medido na vertical) em px
        :pixel_size: [user input] tamanha do pixel do sensor da câmara [micrometros]
        :focal_distance: [user input] distancia focal
        :mf: [user input] modulo da escala da foto
        :l: [user input] sobreposição horizontal entre fotos do mesmo modelo
        :q: [user input] sobreposição vertical entre fotos em faixas adjacentes
    """
    # S1: dimensão de s1 à escala no terreno [m]:
    S1 = s1 * mf * pixel_size * 10 ** (-6)

    # S2: dimensão de s2 à escala no terreno [m]:
    S2 = s2 * mf * pixel_size * 10 ** (-6)

    # H: altura de voo tendo em conta a distância focal, modulo da escala da fotografia pretendida e cota média [m]:
    H = focal_distance * 10 ** (-3) * mf + cota_media

    # A: distância entre pontos de captura de fotos entre fiadas [m]:
    A = S2 * (1. - (q / 100.))

    # B: distância entre pontos de captura de fotos na mesma fiada [m]:
    B = S1 * (1. - (l / 100.))

    # Diferença entre coordenadas y dos vértices opostos da área a levantar
    Q = abs(area[0][1] - area[2][1])
    nfx = int((Q / A) + 1)  # número de fiadas

    # Diferença entre coordenadas y dos vértices opostos da área a levantar
    L = abs(area[0][0] - area[1][0])
    nm = int((L / B) + 1)  # número de fotos na mesma fiada

    # Inicialização da lista de fotos usando função auxiliar, tendo a primeira foto calculada em função da
    # área, orientação e altura. Nota: Altura será igual para todas as fotos no bloco

    fotos = [get_first_foto(area, orientation, H, S2, q, B)]

    # loop para inserir pontos de captura de fotos em cada fiada, contando com duas fotos extra de
    # segurança: uma antes do limite da área; uma após o limite da área:
    for i in range(nfx):
        # loop para inserir pontos de captura de fotos entre fiadas:
        for j in range(nm + 1):
            if i % 2 == 0: fotos.append(get_next_foto_faixa(fotos[-1], 0, orientation * B))
            if i % 2 == 1: fotos.append(
                get_next_foto_faixa(fotos[-1], 0, - orientation * B))  # nas fiadas pares a orientação é invertida

        fotos.append(get_next_foto_faixa(fotos[-1], -A, 0))

    # ISSUE TO FIX: hack para remover último ponto introduzido de forma não intencional (aspeto a melhorar...)
    fotos.pop(-1)

    return fotos


def get_plan_budget(unit_cost_foto, unit_cost_flight_hour, flight_speed, s1, s2, pixel_size, mf, q, l, area):
    """ Retorna tuple (distancia, tempo, budget) valores aproximados de distancia percorrida[m] duração de voo no plano
        definido [h] e orçamento [Euro].
        :unit_cost_foto: custo unitário por foto [Euro]
        :unit_cost_flight_hour: custo unitário por hora de voo [Euro]
        :flight_speed: [user input] velocidade de voo [km/h]
        :s1: [user input] largura do sensor (medido na direção de voo) [px]
        :s2: [user input] comprimento do sensor (medido na perpendicular à direção de voo) [px]
        :pixel_size: [user input] tamanha do pixel do sensor da câmara [micrometros]
        :mf: [user input] modulo da escala da foto
        :l: [user input] sobreposição horizontal entre fotos do mesmo modelo
        :q: [user input] sobreposição vertical entre fotos em faixas adjacentes
    """
    # S1: dimensão de s1 à escala no terreno [m]:
    S1 = s1 * mf * pixel_size * 10 ** (-6)

    # S2: dimensão de s2 à escala no terreno [m]:
    S2 = s2 * mf * pixel_size * 10 ** (-6)

    A = S2 * (1. - (q / 100.))  # distância entre pontos de captura de fotos entre fiadas
    B = S1 * (1. - (l / 100.))  # distância entre pontos de captura de fotos na mesma fiada

    Q = abs(area[0][1] - area[2][1])  # Diferença entre coordenadas y dos vértices laterais da área a levantar
    nfx = int((Q / A) + 1)  # número de fiadas

    L = abs(area[0][0] - area[1][0])  # Diferença entre coordenadas x dos vértices superiores da área a levantar
    nm = int((L / B) + 1)  # número de fotos na mesma fiada

    # Distância de voo: somamos as (nm + 1) distâncias de B percorridas entre pontos de tomada de foto em cada fiada +
    # distância aproximada de mudança de faixa (dada pela semi-circunferência pi*A/2) para nfx-1 mudanças de faixa
    # (valor em m):
    distance = (nm+1) * B * (nfx) + (3.141 / 2.) * A * (nfx - 1)

    # Tempo de voo é dado em função da distância e velocidade de voo
    time = distance / (flight_speed * 1000)

    # Orçamento total aproximado considerando os custos unitários
    budget = (nm + 1) * (nfx) * unit_cost_foto + time * unit_cost_flight_hour

    return (distance, time, budget)
