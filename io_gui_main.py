# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:01:33 2022

@author: mario
"""
import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import io

import calc
import cameras

predef_cameras = cameras.get_camera_model_names()
budget = 0
flight_time = 0
distance = 0

def create_figure(area, fotos):
         
    area_to_plot = [area[0], area[1], area[2], area[3], area[0]] #formar polígono fechado da área a desenhar, com repetição do primeiro ponto na última posição da lista
    area_to_plot_xs, area_to_plot_ys = zip(*area_to_plot)
    
    fig = Figure(figsize=(9, 6))    
        
    ax = fig.add_subplot(111)
    
    ax.plot(area_to_plot_xs, area_to_plot_ys, color =(0.1, 0.2, 0.3, 0.2))
    
    for f in fotos:
        ax.plot(f[1], f[2], 'ro')
        ax.text(f[1], f[2], 'F' + str(f[0]), ha = "left")
        
    ax.set_xlabel("E [m]")
    ax.set_ylabel("N [m]")
        
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
    
    [sg.Text('P1x [m]', font=("Helvetica", 8)), sg.InputText('484775', key='P1_x', size=(9,1),justification="right"), 
     sg.Text('P2x [m]', font=("Helvetica", 8)), sg.InputText('488722', key='P2_x', size=(9,1),justification="right"), 
     sg.Text('P3x [m]', font=("Helvetica", 8)), sg.InputText('488722', key='P3_x', size=(9,1),justification="right"), 
     sg.Text('P4x [m]', font=("Helvetica", 8)), sg.InputText('484775', key='P4_x', size=(9,1),justification="right")], 
    
    [sg.Text('P1y [m]', font=("Helvetica", 8)),sg.InputText('4290518', key='P1_y', size=(9,1),justification="right"), 
     sg.Text('P2y [m]', font=("Helvetica", 8)), sg.InputText('4290518', key='P2_y', size=(9,1),justification="right"), 
     sg.Text('P3y [m]', font=("Helvetica", 8)), sg.InputText('4287616', key='P3_y', size=(9,1),justification="right"), 
     sg.Text('P4y [m]', font=("Helvetica", 8)), sg.InputText('4287616', key='P4_y', size=(9,1),justification="right")],
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
     sg.Combo(predef_cameras, key='cam_conf_predef', default_value = predef_cameras[0], size=(20, 1)),
     
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
    [sg.Button('SaveTXT'), sg.Button('SaveKML')],
    ]

layout = [
    [sg.Col(column_input),
     sg.Col(column_output, key=('-OUTPUT-'), visible=False)]
    ]

window = sg.Window('Plano de voo', layout)

image_element = window['-IMAGE-']       # type: sg.Image

while True:
    event, io_values = window.read()
    
    if event == 'SaveTXT':
        filename = sg.popup_get_file('Guardar KML', no_window=True)
        window.SaveToDisk(filename)
        # save(io_values)        
    elif event == 'SaveKML':
        filename = sg.popup_get_file('Guardar KML', no_window=True)
        window.SaveToDisk(filename)
        # load(form)
    elif event == 'Submeter':
        
        P1 = (float(io_values['P1_x']), float(io_values['P1_y']))
        P2 = (float(io_values['P2_x']), float(io_values['P2_y']))
        P3 = (float(io_values['P3_x']), float(io_values['P3_y']))
        P4 = (float(io_values['P4_x']), float(io_values['P4_y']))
        
        area = calc.get_area(P1, P2, P3, P4)
                        
        q = float(io_values['q'])
        l = float(io_values['l'])
        
        mf = float(io_values['mf'])
        
        cota_media = float(io_values['cota_media'])
        
        unit_cost_foto = float(io_values['unit_cost_foto'])
        unit_cost_flight_hour = float(io_values['unit_cost_flight_hour'])
        flight_speed = float(io_values['flight_speed'])
        
        if io_values['E-W']: orientation = -1 
        if io_values['W-E']: orientation = 1
        
        if io_values['option_cam_predef']: 
            s1 = cameras.get_camera(io_values['cam_conf_predef'],"s1")
            s2 = cameras.get_camera(io_values['cam_conf_predef'],'s2')
            pixel_size = cameras.get_camera(io_values['cam_conf_predef'],'pixel_size')
            focal_distance = cameras.get_camera(io_values['cam_conf_predef'],'focal_distance')            
            
        if io_values['option_cam_custom']:
            s1 = int(io_values['custom_s1'])
            s2 = int(io_values['custom_s2'])
            pixel_size = float(io_values['custom_pixel_size'])
            focal_distance = float(io_values['custom_focal_distance'])

        fotos = calc.get_plan_fotos(area, orientation, cota_media, s1, s2, mf, pixel_size, focal_distance, l, q)
                
        budget_values = calc.get_plan_budget(unit_cost_foto, unit_cost_flight_hour, flight_speed, s1, s2, pixel_size, mf, q, l, area, fotos)
        
        distance = round(budget_values[0], ndigits=1) # distancia total de voo na área a levantar em metros
        flight_time = round(budget_values[1] * 60, ndigits=1) # tempo de voo em minutos
        budget = round(budget_values[2], ndigits=1) # orçamento em Euro
    
        window['-OUTPUT-'].update(visible=True)
       
        window['distance'].update(distance)
        window['flight_time'].update(flight_time)
        window['budget'].update(budget)
        
        draw_figure(image_element, create_figure(area, fotos))
        
    elif event in ('Sair', None):
        break

window.close()
