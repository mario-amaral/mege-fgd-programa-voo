# Programa plano de voo (FCUL MEGE FGD 2023-24)

Programa plano de voo: define plano de voo para captura de fotografias numa área a levantar definida por pontos arbitrários.  

## Bibliotecas externas

Utiliza as seguintes bibliotecas Python:
+ PySimpleGUI: https://www.pysimplegui.org/
+ Matplotlib: https://matplotlib.org/
+ SimpleKML: https://simplekml.readthedocs.io/
+ UTM: https://pypi.org/project/utm/

## Arquitetura:

Módulos internos: main.py, io_elements.py; calc.py, cameras.py

+ Modulo principal (main.py): executa o loop da janela do User Interface (UI) e chama as funções de cálculo (no módulo calc.py), bem como as funções do módulo de input/output (io_elements.py).
+ Módulo de cálculo (calc.py): contém as funções que calculam as coordenadas dos pontos de captura de fotos, a área a levantar e os resultados do orçamento do plano de voo (orçamento, tempo de voo e distância). 
+ Módulo de input/output (io_elements.py): contém as referências para os objetos e funções das bibliotecas externas utilizadas para o UI e para a escrita dos ficheiros txt e kml.
+ Módulo de configurações das câmaras (cameras.py): contém implementação de um dicionário Python que armazena as configurações predefinidas de cãmaras. Pode ser editado, mas convém respeitar a sintaxe Python, pois não há nenhum mecanismo de verificação de erros implementado. 

## Notas:

+ Dadas as especificidades da biblioteca externa SimpleKML, é necessária a indicação da Zona UTM
+ Se não for indicada uma pasta para escrita dos ficheiros de output (.txt ou .kml), a pasta selecionada por defeito será aquela onde se encontra o executável
+ Esta versão do programa não contém uma implementação de exceções de execução face aos dados introduzidos pelo utilizador, para além do que possa existir nativo nas biblitocas Python standard ou externas utilizadas.

## Âmbito do projeto

Projeto executado por Mário Amaral em Python no âmbito da disciplina de fotogrametria digital do Mestrado de Eng. Geoespacial da FCUL (2022-23)

## Instalação e execução

Programado e testado em ambiente Python 3.10. Deverá ser compatível com versões anteriores do interpretador (pelo menos 3.8).

## Autor

Mário Amaral

## Licença

Aplicam-se as licenças das bibliotecas Python indicadas acima.

