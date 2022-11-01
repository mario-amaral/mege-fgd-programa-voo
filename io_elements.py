# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:56:42 2022
Programa plano de voo: modulo de input/output utilizando a biblioteca PySimpleGUI para o interface de utilizador
Gera a janela para formulário de input e widgets de output. Gráfico é produzido através da biblioteca matplotlib.
Biblioteca SimplKML é usada para escrever no formato KML (em coordenadas elipsoidais lat/lon) e biblioteca UTM é usada
para converter coordenadas UTM em coordenadas lat/lon.
Bibliotecas externas:
    PySimpleGUI: https://www.pysimplegui.org/
    Matplotlib: https://matplotlib.org/
    SimpleKML: https://simplekml.readthedocs.io/
    UTM: https://pypi.org/project/utm/
@author: Mario Amaral
"""
import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import io
import simplekml
import utm

import cameras

# valores default apresentados no formulário de input:
P1_x_default = 484845
P2_x_default = 488710
P3_x_default = 484775
P4_x_default = 488722

P1_y_default = 4290518
P2_y_default = 4290502
P3_y_default = 4287816
P4_y_default = 4287616

s1_default = cameras.get_camera('DMC', 's1')
s2_default = cameras.get_camera('DMC', 's2')
pixel_size_default = cameras.get_camera('DMC', 'pixel_size')
focal_distance_default = cameras.get_camera('DMC', 'focal_distance')

predef_cameras_names = cameras.get_camera_model_names()

# inicialização das variáveis de output:
budget = 0.
flight_time = 0.
distance = 0.

# esquema de cores da biblioteca PySimpleGUI:
sg.theme('DarkTeal10')


def create_figure(area, fotos):
    """Função auxiliar de draw_figure(). Cria figura matplotlib para representação num elemento de imagem.
       :area: lista dos vértices da área a levantar
       :fotos: lista dos pontos de captura de fotos
    """
    # Forma polígono fechado da área a desenhar:
    area_to_plot = [area[0], area[1], area[2], area[3], area[0]]
    area_to_plot_xs, area_to_plot_ys = zip(*area_to_plot)

    # fig: Instância objeto Figure de matplotlib -- figsize determina o tamanho da janela do gráfico
    fig = Figure(figsize=(7, 4))

    # adiciona um sistema de eixos a fig e desenha os pontos da area
    ax = fig.add_subplot(111)
    ax.plot(area_to_plot_xs, area_to_plot_ys, color =(0.1, 0.2, 0.3, 0.2))

    # loop percorre todas a fotos da lista de fotos
    for f in fotos:
        # para cada foto f, desenha ponto no gráfico (ro representa ponto marcado por um circulo)
        ax.plot(f[1], f[2], 'ro')
        # atribui label com a identificação do ponto F1, F2, F3,...
        ax.text(f[1], f[2], 'F' + str(f[0]), ha = "left")

    # insere legendas dos eixos
    ax.set_xlabel("UTM Zone S 29: Easting [m]")
    ax.set_ylabel("UTM Zone S 29: Northing [m]")
        
    return fig


def draw_figure(element, figure):
    """Função auxiliar. Retorna canvas para representação da figura criada por create_figure() num elemento do GUI.
        utiliza objeto da biblioteca matplotlib.
       :element: elemento do GUI onde o canvas será apresentado
       :figure: figura gerada pela função create_figure(), apresentando a área e lista de pontos de captura de fotos
    """
    canv = FigureCanvasAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png',)
    if buf is None:
        return None
    buf.seek(0)
    element.update(data=buf.read())
    return canv 


def get_cam_conf(option_cam_predef, option_cam_custom, cam_conf_predef, custom_s1, custom_s2, custom_pixel_size, custom_focal_distance):
    """Função auxiliar. Retorna tuple com os parâmetros da configuração da camara conforme seleção do utilizador.
        :option_cam_predef: [user input] seleção de câmara predefinida (boolean)
        :option_cam_custom: [user input] seleção de câmara manual, usando formulário (boolean)
        :cam_conf_predef: nome da no modelo de camara predefinida
        :custom_s1, custom_s2, custom_pixel_size, custom_focal_distance: [user input] valores manuais
    """
    if option_cam_predef:
        s1 = cameras.get_camera(cam_conf_predef,"s1")
        s2 = cameras.get_camera(cam_conf_predef,'s2')
        pixel_size = cameras.get_camera(cam_conf_predef,'pixel_size')
        focal_distance = cameras.get_camera(cam_conf_predef,'focal_distance')            
        
    if option_cam_custom:
        s1 = int(custom_s1)
        s2 = int(custom_s2)
        pixel_size = float(custom_pixel_size)
        focal_distance = float(custom_focal_distance)
    
    return (s1, s2, pixel_size, focal_distance)


def get_orientation(e_w, w_e):
    """Função auxiliar. Retorna -1 se voo for na orientação E-W, retorna 1 se for na orientação W-E
        :e_w: [user input] seleção de orientação E-W (boolean)
        :w_e: [user input] seleção de orientação W-E (boolean)
    """
    if e_w: return -1 
    if w_e: return 1    


def write_txt_file(filename, fotos):
    """Escreve ficheiro txt com a lista de coordenadas dos pontos de captura de fotos, um em cada linha de texto.
        :filename: path do ficheiro para escrita em disco
        :fotos: lista dos pontos de captura de fotos
    """
    filename_txt = filename + '.txt'
    with open(filename_txt, 'w') as file:
          
        for foto in fotos:
            row_to_write = str(foto) + "\n"
            file.write(row_to_write)


def write_kml_file(filename, fotos):
    """Escreve ficheiro txt com a lista de coordenadas dos pontos de captura de fotos, um em cada linha de texto.
        :filename: path do ficheiro para escrita em disco
        :fotos: lista dos pontos de captura de fotos
    """
    filename = filename + '.kml'
    
    kml = simplekml.Kml()
    
    for foto in fotos:
        
        point_name = 'F' + str(foto[0])
        pnt = kml.newpoint(name= point_name, altitudemode=('absolute'))
        
        point_coord = utm.to_latlon(foto[1], foto[2], 29, zone_letter="S") #é necessário definir a zona e a letra da projeção UTM
        lon = point_coord[0]
        lat = point_coord[1]
        height = foto[3]
                
        pnt.coords = [(lat,lon, height)]
        pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    
    kml.save(filename)

# Configuração dos elementos do GUI usando o objeto sg da biblioteca PySimpleGUI:

column_cam_conf_manual = [
    [sg.Text('Dimensão do pixel [micro-m]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText(pixel_size_default, key='custom_pixel_size', size=(6,1),justification="right")],
    [sg.Text('Largura do sensor (s1) [px]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText(s1_default, key='custom_s1', size=(6,1),justification="right")],
    [sg.Text('Altura do sensor (s2) [px]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText(s2_default, key='custom_s2', size=(6,1),justification="right")],
    [sg.Text('Distância focal (c) [mm]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText(focal_distance_default, key='custom_focal_distance', size=(6,1),justification="right")],
    ]

column_input = [
    [sg.Text('Configurador de plano de voo', size=(30, 1), font=("Helvetica", 14))],
    [sg.Text(' ')],
    
    [sg.Text('Area a levantar: Coordenadas dos vértices da área a levantar (em coordenadas UTM)', font=("Helvetica", 9, "bold"))],
    
    [sg.Text('P1x [m]', font=("Helvetica", 8)), sg.InputText(P1_x_default, key='P1_x', size=(9,1),justification="right"), 
     sg.Text('P2x [m]', font=("Helvetica", 8)), sg.InputText(P2_x_default, key='P2_x', size=(9,1),justification="right"), 
     sg.Text('P3x [m]', font=("Helvetica", 8)), sg.InputText(P3_x_default, key='P3_x', size=(9,1),justification="right"), 
     sg.Text('P4x [m]', font=("Helvetica", 8)), sg.InputText(P4_x_default, key='P4_x', size=(9,1),justification="right")], 
    
    [sg.Text('P1y [m]', font=("Helvetica", 8)),sg.InputText(P1_y_default, key='P1_y', size=(9,1),justification="right"), 
     sg.Text('P2y [m]', font=("Helvetica", 8)), sg.InputText(P2_y_default, key='P2_y', size=(9,1),justification="right"), 
     sg.Text('P3y [m]', font=("Helvetica", 8)), sg.InputText(P3_y_default, key='P3_y', size=(9,1),justification="right"), 
     sg.Text('P4y [m]', font=("Helvetica", 8)), sg.InputText(P4_y_default, key='P4_y', size=(9,1),justification="right")],
    [sg.Text('Direção de voo:', font=("Helvetica", 8)), sg.Radio('E-W', "RADIO1", key='E-W', default=True), sg.Radio('W-E', "RADIO1", key='W-E')],
    
    [sg.Text('Cota média na área a levantar:', font=("Helvetica", 8)), sg.InputText('80', key='cota_media', size=(9,1),justification="right")],
    
    [sg.Text(' ')],
 
    [sg.Text('Variáveis de escala, velocidade de voo e sobreposição entre fotos:', font=("Helvetica", 9, "bold"))],
    [sg.Text('Escala 1:', font=("Helvetica", 8)), sg.InputText('8000', key='mf', size=(6,1),justification="right"),
     sg.Text('Velocidade de voo [km/h]', font=("Helvetica", 8)), sg.InputText('350', key='flight_speed', size=(3,1),justification="right")],
    [sg.Text('Sobreposição horizontal (l) [%]', font=("Helvetica", 8)), sg.Slider(range=(1, 100),
                orientation='h',
                size=(15, 10),
                default_value=60, key='l', ),
     sg.Text('Sobreposição vertical (q) [%]', font=("Helvetica", 8)), sg.Slider(range=(1, 100),
                orientation='h',
                size=(15, 10),
                default_value=20, key='q', )],
    
    [sg.Text(' ')],
    
    [sg.Text('Custos unitários:', font=("Helvetica", 9, "bold"))],
    [sg.Text('Foto [Euro/unid]:', font=("Helvetica", 8)), sg.InputText('100', key='unit_cost_foto', size=(6,1),justification="right"),
     sg.Text('Hora de voo [Euro/h]', font=("Helvetica", 8)), sg.InputText('2000', key='unit_cost_flight_hour', size=(3,1),justification="right")],
    
    [sg.Text(' ')],
    
    [sg.Text('Configuração da Camara:', font=("Helvetica", 9, "bold"))], 
     [sg.Radio('Modelo/configurações predefinidas', "RADIO2", key='option_cam_predef', default=True), 
     sg.Radio('Configuração manual', "RADIO2", key='option_cam_custom')],
    
    [sg.Text('Modelos/configurações predefinidas:', font=("Helvetica", 8)), 
     sg.Combo(predef_cameras_names, key='cam_conf_predef', default_value = predef_cameras_names[0], size=(20, 1)),
     
     sg.Col(column_cam_conf_manual, background_color='gray34')],
    [sg.Button('Submeter'), sg.Button('Sair', button_color=("red"))],
    ]

column_results_budget = [
    [sg.Text('Distância [m]', font=("Helvetica", 8), size=(15, 1)), 
     sg.Text(budget, key='distance', size=(6,1), justification="right")],
    [sg.Text('Tempo de voo [min]', font=("Helvetica", 8), size=(15, 1)), 
     sg.Text(flight_time, key='flight_time', size=(6,1),justification="right")],
    [sg.Text('Orçamento [Euro]', font=("Helvetica", 8, "bold"), size=(15, 1)), 
     sg.Text(budget, key='budget', size=(6,1),justification="right")],
    ]

column_output = [
    [sg.Image(key='-IMAGE-')],
    [sg.Col(column_results_budget)],
    
    [sg.Text(' ')],
    
    [sg.Text('Guardar plano de voo:', font=("Helvetica", 9, "bold") , size=(35, 1))],
    [sg.Text('Selectionar pasta:', font=("Helvetica", 8), size=(15, 1)),sg.Input(key='-USER_FOLDER-'), sg.FolderBrowse(target='-USER_FOLDER-')],
    [sg.Text('Nome do ficheiro:', font=("Helvetica", 8), size=(15, 1)),sg.InputText('plano_de_voo', key='filename')],
    [sg.Button('SaveTXT'), sg.Button('SaveKML')],
    ]

# layout é usado na criação da janela. Note-se que a coluna de output está inicialmente invisível até que o botão
# submeter seja pressionado (ver código no modulo main)
layout = [
    [sg.Col(column_input),
     sg.Col(column_output, key=('-OUTPUT-'), visible=False)]
    ]
