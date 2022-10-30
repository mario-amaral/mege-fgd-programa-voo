# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:56:16 2022

@author: mario
"""

import calc
import io_elements

def main():
    window = io_elements.sg.Window('Plano de voo', io_elements.layout)
    image_element = window['-IMAGE-']
    
    while True:
        event, values = window.read()
        
        if event == 'Submeter':
            P1 = (float(values['P1_x']), float(values['P1_y']))
            P2 = (float(values['P2_x']), float(values['P2_y']))
            P3 = (float(values['P3_x']), float(values['P3_y']))
            P4 = (float(values['P4_x']), float(values['P4_y']))
            
            area = calc.get_area(P1, P2, P3, P4)
                            
            q = float(values['q'])
            l = float(values['l'])
            
            mf = float(values['mf'])
            
            cota_media = float(values['cota_media'])
            
            unit_cost_foto = float(values['unit_cost_foto'])
            unit_cost_flight_hour = float(values['unit_cost_flight_hour'])
            flight_speed = float(values['flight_speed'])
            
            cam_conf = io_elements.get_cam_conf(values['option_cam_predef'], values['option_cam_custom'], values['cam_conf_predef'], values['custom_s1'], values['custom_s2'], values['custom_pixel_size'], values['custom_focal_distance'])
            
            s1 = cam_conf[0]
            s2 = cam_conf[1]
            pixel_size = cam_conf[2]
            focal_distance = cam_conf[3]
    
            orientation = io_elements.get_orientation(values['E-W'], values['W-E'])
    
            fotos = calc.get_plan_fotos(area, orientation, cota_media, s1, s2, mf, pixel_size, focal_distance, l, q)
                    
            budget_values = calc.get_plan_budget(unit_cost_foto, unit_cost_flight_hour, flight_speed, s1, s2, pixel_size, mf, q, l, area, fotos)
            
            distance = round(budget_values[0], ndigits=1) # distancia total de voo na área a levantar em metros
            flight_time = round(budget_values[1] * 60, ndigits=1) # tempo de voo em minutos
            budget = round(budget_values[2], ndigits=1) # orçamento em Euro
        
            window['-OUTPUT-'].update(visible=True)
           
            window['distance'].update(distance)
            window['flight_time'].update(flight_time)
            window['budget'].update(budget)
            
            io_elements.draw_figure(image_element, io_elements.create_figure(area, fotos))
            
        elif event == 'SaveKML':
            pass
            #filename = sg.popup_get_file('Guardar KML', no_window=True)
            # load(form)
        elif event == 'SaveTXT':
            filename = values['filename']
            file_path = values['-USER_FOLDER-']
            chosen_file_name = file_path + "/" + filename
            io_elements.write_txt_file(chosen_file_name, fotos)
            
        elif event in ('Sair', None):
            break
    
    window.close()

if __name__ == "__main__":
    main()