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

# As colunas de 0 a 2 representam, nessa ordem, as ações LEFT, RIGHT, JUMP

jogadas = ["left", "right", "jump"] # Define as possíveis jogadas

q_table = []
initialize_table(q_table) # Inicializa a Q-Table

alfa = 0.25 # Taxa de aprendizagem
gama = 0.50 # Taxa de desconto

# Modelando o estado inicial
current_state = 0 # Platforma = 0  /  Direcão = Norte


# Recupera a tabela resultante do teste anterior
with open('qtable.txt', 'r') as arquivo:
   linhas = arquivo.readlines()

for i in range(96):
    linha = linhas[i].split(" ")
    for j in range(3):
                q_table[i][j] = float(linha[j])



i = 1000
while i > 0:

    # Uso de uma combinação de escolhas aleatórias com escolhas "inteligentes" nos testes
    action_type = random.randint(1, 2) # Proporção variável durante os testes

    alfa = 0.25

    # Escolha de ação inteligente
    if action_type != 0:
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
    
    current_value = q_table[current_state][action_idx] # Atribui ao current_value o valor da tabela para o estado current_state com a ação escolhida
    
    state_str, reward = cn.get_state_reward(s, action)  # Recebe o estado e a recompensa resultantes da ação

    # Reduz o impacto de uma ação JUMP que sai errada, devido ao não determinismo, e impacta na morte do personagem
    if reward == -100:
        alfa = 0.05 # Valor de alfa variável de acordo com os testes

    platform = int(str(state_str)[2:7], 2) # Converte número da plataforma para inteiro
    direction = int(str(state_str)[7:9], 2) # Norte = 0 / Leste = 1 / Sul = 2 / Oeste = 3
    
    state = (platform * 4) + (direction % 4) # Nova variável STATE como inteiro para ser usada nos acessos à q_table

    max_value = max(q_table[state][0], q_table[state][1], q_table[state][2]) # Define o maior reforço futuro possível

    q_value = q_table_update(current_value, action_idx, alfa, gama, reward, max_value) # Recebe o novo valor a ser inserido na q_table

    # Só atualiza a q_table para a plataforma treinada, nesse caso a plataforma 17 
    if(6800 <= current_state <= 7100):
        q_table[current_state][action_idx] = q_value

    current_state = state # Atualiza o current state antes da próxima jogada

    i = i - 1

# Escreve a tabela em um arquivo .txt
with open('resultado.txt', 'w') as f:
    for i in range(96):
        for j in range(3):
            f.write((str(q_table[i][j]) + " "))
        f.write("\n")






