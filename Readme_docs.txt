Dados com informação sobre a área de estudo:
buildings.txt
roads.txt
trees_baseline.txt

Os ficheiros buildings e trees tem a seguinte estrutura:
ID- numero do edidicio ou árvore (cada edificio ou árvore é definido por 4 vertices/coordenadas)
x, y - coordenadas x, y do edificio ou árvore
z- altura do edificio

O ficheiro roads tem a seguinte estrutura:
ID- numero da estrada (cada estrada é definido por 4 vertices/coordenadas)
x, y - coordenadas x, y do estrada

Envio duas pastas com dados:
NOx - pasta com dados de concentração de NO2 para uma altura de 1.5m, para 1 dia, em base horária (cada ficheiro corresponde a uma hora diferente, 
variando entre 0 a 23. A hora em questão é apresentada no nome do ficheiro, e.g., B_NOx_0).

Os ficheiros desta pasta tem a seguinte estrutura:
x, y - representam as coordenadas do dominio do modelo CFD, com uma resolução de 3m, sendo que a primeira
coordernada corresponde ao canto inferior esquerdo do dominio de simulação.
conc - representa a concentração de NO2, em ug/m3
vel - representa a magnitude da velocidade do vento, em m/s.
dir - representa a direção do vento

Com estes dados pretende-se representar os valores de concentração, para as diferentes horas, para uma altura fixa.


VEL - pasta com dados de velocidade e direção do vento, para diferentes alturas, para uma determinada hora. 

Esta pasta tem 19 ficheiros, sendo que cada ficheiro apresenta dados para diferentes alturas (com  
uma resolução de 3m). 
O nome do ficheiro representa a altura do corte. 
O primeiro ficheiro apresenta dados para uma altura de 3m e o último ficheiro apresenta dados para 
uma altura de 57m.

Cada ficheiro é constituido por 4 colunas, x, y, vel, dir.
x,y representam as coordenadas do dominio do modelo CFD, com uma resolução de 3m, sendo que a primeira
coordernada corresponde ao canto inferior esquerdo do dominio de simulação. 
A coluna vel representa a magnitude da velocidade do vento, em m/s.
A coluna dir representa a direção do vento. 

As restantes colunas do ficheiro não são relevantes.

O objetivo com estes dados é representar a velocidade do vento nas diferentes alturas. 


