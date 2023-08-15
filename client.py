import connection as cn
import random
import time

s = cn.connect(2037)

def initialize_table(q_table):
    for i in range(96):
        linha = []
        for j in range(3):
            linha.append(0)

        q_table.append(linha)

def q_table_update(q_value, coluna, alfa, gama, reward, max_value):
    # Atualiza q_table
    q_value = (1 - alfa) * q_value + (alfa * (reward + (gama * max_value)))
    return q_value

# Linhas 0 à 3 -> plataforma 0 nas direções Norte, Leste, Sul, Oeste
# Linhas 4 à 7 -> plataforma 1 nas direções Norte, Leste, Sul, Oeste ...

# As colunas de 0 a 2 representam, nessa ordem, LEFT, RIGHT, JUMP

jogadas = ["left", "right", "jump"] # Define as possíveis jogadas

q_table = []
initialize_table(q_table) # Inicializa a Q-Table

alfa = 0.2 # Taxa de aprendizagem
gama = 0.5 # Taxa de desconto

# Modelando o estado inicial
current_state = 0 # Platform = 0  /  Direction = North

#Atualiza a tabela para o próximo teste
with open('resultado.txt', 'r') as arquivo:
   linhas = arquivo.readlines()
    

for i in range(96):
    linha = linhas[i].split(" ")
    for j in range(3):
        q_table[i][j] = float(linha[j])

# O usuário escolhe o tipo de ação do personagem
action_type = int(input())

i = 1000
while i > 0:

    # Escolha de ação inteligente
    if action_type == 0:
        action_value = q_table[current_state][0]
        action_idx = 0
        for j in range(3):
            if q_table[current_state][j] > action_value:
                    action_value = q_table[current_state][j]
                    action_idx = j 

    # Escolha de ação burra
    else:      
        action_idx = random.randint(0, 2)

    action = jogadas[action_idx]

    current_value = q_table[current_state][action_idx] # Atribui ao CURRENT VALUE o valor da tabela para o estado CURRENT STATE com a ação escolhida
    
    state_str, reward = cn.get_state_reward(s, action)  # Recebe o estado e a recompensa resultantes da ação

    # Ajusta o valor de para diminuir o impacto da queda no valor da q_table
    if reward == -100:
        alfa = 0.02
        
    platform = int(str(state_str)[2:7], 2) # Converting platform number to integer
    direction = int(str(state_str)[7:9], 2) # North = 0 / East = 1 / South = 2 / West= 3
    
    state = (platform * 4) + (direction % 4) # Nova variável STATE como inteiro para ser usada nos acessos à q_table

    max_value = max(q_table[state][0], q_table[state][1], q_table[state][2]) # Define o maior reforço futuro possível

    q_value = q_table_update(current_value, action_idx, alfa, gama, reward, max_value) # Recebe o valor atualizado da q_table

    q_table[current_state][action_idx] = q_value

    current_state = state # Atualiza o current state antes da próxima jogada

    i = i - 1

# Escreve a tabela em um arquivo .txt
with open('resultado.txt', 'w') as f:
    for i in range(96):
        for j in range(3):
            f.write((str(q_table[i][j]) + " "))
        f.write("\n")






