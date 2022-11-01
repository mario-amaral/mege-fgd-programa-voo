# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:22:18 2022
Programa plano de voo: modulo de cálculo
Guarda num dicionário de python as configurações dos modelos de câmaras predefinidos
@author: Mario Amaral
"""

# Configurações predefinidas das câmaras digitais usando dicionários em python:
# pixel_size: tamanha do pixel do sensor da câmara [micrometros]
# Número de pixels dado por s2 x s1, com:
#    s1: largura do sensor (medido na direção de voo) em px
#    s2: comprimento do sensor (medido na perpendicular à direção de voo) em px
# focal_distance: distancia focal [mm]

camera_model = {
         'DMC': {
             'pixel_size': 12.,
             's1': 7680,
             's2': 13824,
             'focal_distance': 120.,
             },

         'DMC_II_140': {
             'pixel_size': 7.2,
             's1': 11200,
             's2': 12096,
             'focal_distance': 92.,
             },

         'DMC_II_230' : {
             'pixel_size': 5.6,
             's1': 14144,
             's2': 15542,
             'focal_distance': 92.,
             },

         'DMC_II_250' : {
             'pixel_size': 5.6,
             's1': 17216,
             's2': 14656,
             'focal_distance': 112.,
             },
         
         'UltraCamD' : {
             'pixel_size': 9.,
             's1': 7500,
             's2': 11500,
             'focal_distance': 100.,
             },
         
         'UltraCamX' : {
             'pixel_size': 7.2,
             's1': 14430,
             's2': 9420,
             'focal_distance': 100.,
             },
         
         'UltraCamXp' : {
             'pixel_size': 6.,
             's1': 17310,
             's2': 11310,
             'focal_distance': 100.,
             },
         
         'UltraCamXp WA' : {
             'pixel_size': 6.,
             's1': 17310,
             's2': 11310,
             'focal_distance': 70.,
             },
         
         'Leica ADS' : {
             'pixel_size': 6.5,
             's1': 12000,
             's2': 12000,
             'focal_distance': 62.5,
             },
    }

def get_camera (model_name, parameter_name):
    """ Retorna valor do parametro e da camara.
        :model_name: nome da camara pre definida.
        :parameter_name: nome do parâmetro pretendido
    """
    return camera_model[model_name][parameter_name]

def get_camera_model_names ():
    """ Retorna lista de nomes dos modelos de câmaras predefinidos
    """
    return list(camera_model.keys())
