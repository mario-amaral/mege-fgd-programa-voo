# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:56:42 2022

@author: mario
"""
import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import io
import simplekml
import utm

import cameras

predef_cameras_names = cameras.get_camera_model_names()

budget = 0.
flight_time = 0.
distance = 0.

def create_figure(area, fotos):
         
    area_to_plot = [area[0], area[1], area[2], area[3], area[0]] #formar polígono fechado da área a desenhar, com repetição do primeiro ponto na última posição da lista
    area_to_plot_xs, area_to_plot_ys = zip(*area_to_plot)
    
    fig = Figure(figsize=(9, 6))    
        
    ax = fig.add_subplot(111)
    
    ax.plot(area_to_plot_xs, area_to_plot_ys, color =(0.1, 0.2, 0.3, 0.2))
    
    for f in fotos:
        ax.plot(f[1], f[2], 'ro')
        ax.text(f[1], f[2], 'F' + str(f[0]), ha = "left")
        
    ax.set_xlabel("UTM Zone S 29: Easting [m]")
    ax.set_ylabel("UTM Zone S 29: Northing [m]")
        
    return fig

def draw_figure(element, figure):
    """
    Draws the previously created "figure" in the supplied Image Element
    :param element: an Image Element
    :param figure: a Matplotlib figure
    :return: The figure canvas
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
    if e_w: return -1 
    if w_e: return 1    

def write_txt_file(filename, fotos):
    filename_txt = filename + '.txt'
    with open(filename_txt, 'w') as file:
          
        for foto in fotos:
            row_to_write = str(foto) + "\n"
            file.write(row_to_write)
            
def write_kml_file(filename, fotos):
    
    #TO-DO: testar com pontos na zona de UTM 29 S
    
    kml = simplekml.Kml()
    
    for foto in fotos:
        
        point_name = 'F' + str(foto[0])
        pnt = kml.newpoint(name= point_name, altitudemode=('absolute'))
        
        point_coord = utm.to_latlon(foto[1], foto[2], 29, zone_letter="S") #é necessário definir a zona e a letra da projeção UTM
        lat = point_coord[0]
        lon = point_coord[1]
        height = foto[3]
                
        pnt.coords = [(lat,lon, height)]
        pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    
    kml.save(filename)

sg.theme('SystemDefault1')

column_cam_conf_manual = [
    [sg.Text('Dimensão do pixel [micro-m]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText('12', key='custom_pixel_size', size=(6,1),justification="right")],
    [sg.Text('Largura do sensor (s1) [px]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText('7680', key='custom_s1', size=(6,1),justification="right")],
    [sg.Text('Altura do sensor (s2) [px]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText('13824', key='custom_s2', size=(6,1),justification="right")],
    [sg.Text('Distância focal (c) [mm]', font=("Helvetica", 8), size=(30, 1)), 
     sg.InputText('120', key='custom_focal_distance', size=(6,1),justification="right")],
    ]

column_input = [
    [sg.Text('Configurador de plano de voo', size=(30, 1), font=("Helvetica", 14))],
    [sg.Text(' ')],
    
    [sg.Text('Area a levantar: Coordenadas dos vértices da área a levantar (em coordenadas UTM)', font=("Helvetica", 9, "bold"))],
    
    [sg.Text('P1x [m]', font=("Helvetica", 8)), sg.InputText('1000', key='P1_x', size=(9,1),justification="right"), 
     sg.Text('P2x [m]', font=("Helvetica", 8)), sg.InputText('5000', key='P2_x', size=(9,1),justification="right"), 
     sg.Text('P3x [m]', font=("Helvetica", 8)), sg.InputText('1000', key='P3_x', size=(9,1),justification="right"), 
     sg.Text('P4x [m]', font=("Helvetica", 8)), sg.InputText('5000', key='P4_x', size=(9,1),justification="right")], 
    
    [sg.Text('P1y [m]', font=("Helvetica", 8)),sg.InputText('10000', key='P1_y', size=(9,1),justification="right"), 
     sg.Text('P2y [m]', font=("Helvetica", 8)), sg.InputText('10000', key='P2_y', size=(9,1),justification="right"), 
     sg.Text('P3y [m]', font=("Helvetica", 8)), sg.InputText('13000', key='P3_y', size=(9,1),justification="right"), 
     sg.Text('P4y [m]', font=("Helvetica", 8)), sg.InputText('13000', key='P4_y', size=(9,1),justification="right")],
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
    [sg.Button('Submeter', button_color=("white")), sg.Button('Sair', button_color=("red"))],
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

layout = [
    [sg.Col(column_input),
     sg.Col(column_output, key=('-OUTPUT-'), visible=False)]
    ]
