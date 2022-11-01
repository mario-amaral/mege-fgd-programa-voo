# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:56:16 2022
Programa plano de voo: modulo main para execução do programa recorrendo aos modulos internos calc e io_elements.
@author: Mario Amaral
"""

import calc
import io_elements


def main():
    """Corre o programa: contém loop de execução da janela PySimpleGUI
    """

    # Cria a janela do programa conforme elementos configurados no layout (modulo io_elements). Este objeto é usado
    # nesta função para atualizar os elementos de output
    window = io_elements.sg.Window('Plano de voo', io_elements.layout)

    # O elemento de imagem (widget do gráfico) é criado, mas só será apresentado quando o butão submeter for pressionado
    image_element = window['-IMAGE-']

    # loop de escuta de eventos de input:

    while True:
        # values guarda todos os elementos do GUI, incluindo valores dos parâmetros introduzidos pelo utilizador. Cada
        # elemento é identificado por uma key do tipo values['key'], conforme associação feita no modulo io_elements
        event, values = window.read()

        if event == 'Submeter':

            # Quando botão 'Submeter' é pressionado, as variáveis para cálculo são guardadas e passadas às diferentes
            # funções do modulo de cálculo:

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

            cam_conf = io_elements.get_cam_conf(values['option_cam_predef'], values['option_cam_custom'],
                                                values['cam_conf_predef'], values['custom_s1'], values['custom_s2'],
                                                values['custom_pixel_size'], values['custom_focal_distance'])

            s1 = cam_conf[0]
            s2 = cam_conf[1]
            pixel_size = cam_conf[2]
            focal_distance = cam_conf[3]

            orientation = io_elements.get_orientation(values['E-W'], values['W-E'])

            fotos = calc.get_plan_fotos(area, orientation, cota_media, s1, s2, mf, pixel_size, focal_distance, l, q)

            budget_values = calc.get_plan_budget(unit_cost_foto, unit_cost_flight_hour, flight_speed, s1, s2,
                                                 pixel_size, mf, q, l, area, fotos)

            # Valores da distância total, tempo de voo e orçamento são arredondados a uma casa decimal:

            distance = round(budget_values[0], ndigits=1)
            flight_time = round(budget_values[1] * 60, ndigits=1)  # tempo de voo em minutos
            budget = round(budget_values[2], ndigits=1)  # orçamento em Euro

            # Widget de output é tornada visivel no momento em que os elementos de output sao atualizados:
            window['-OUTPUT-'].update(visible=True)
            window['distance'].update(distance)
            window['flight_time'].update(flight_time)
            window['budget'].update(budget)

            io_elements.draw_figure(image_element, io_elements.create_figure(area, fotos))

        elif event == 'SaveKML':

            # ISSUE TO FIX: caso o programa corra a partir de executável .exe é necessário selecionar a pasta para
            # poder escrever o ficheiro. Caso o programa corra no interpretador python, o ficheiro é escrito por defeito
            # na mesma pasta do ficheiro main.py

            # Guarda ficheiro KML

            filename = values['filename']
            file_path = values['-USER_FOLDER-']
            chosen_file_name = file_path + '/' + filename
            io_elements.write_kml_file(chosen_file_name, fotos)

        elif event == 'SaveTXT':

            # Guarda ficheiro TXT

            filename = values['filename']
            file_path = values['-USER_FOLDER-']
            chosen_file_name = file_path + '/' + filename
            io_elements.write_txt_file(chosen_file_name, fotos)

        elif event in ('Sair', None):
            break

    window.close()


if __name__ == "__main__":
    main()
