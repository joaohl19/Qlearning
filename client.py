import connection as cn
import random
import time

s = cn.connect(2037)

print(s)

def choose_action(jogadas):
    action = random.randint(0, 2)
    return action

def initialize_table(q_table):
    for i in range(96):
        #print("\n")
        linha = []
        for j in range(3):
            #print(f'{0}', end=" ")
            linha.append(0)

        q_table.append(linha)

def q_table_update(q_value, coluna, alfa, gama, reward, max_value):
    # Updates q_table
    q_value = (1 - alfa) * q_value + (alfa * (reward + (gama * max_value)))

# As linhas de 0 <= index <= 23 indicam as plataformas da 0 até a 23 com a direção do personagem NORTH

# As linhas de 24 <= index <= 47 indicam as plataformas da 0 até a 23 com a direção do personagem EAST

# As linhas de 48 <= index <= 71 indicam as plataformas da 0 até a 23 com a direção do personagem SOUTH

# As linhas de 72 <= index <= 95 indicam as plataformas da 0 até a 23 com a direção do personagem WEST

# As colunas de 0 a 2 representam, nessa ordem, LEFT, RIGHT, JUMP


jogadas = ["left", "right", "jump"] # Define as possíveis jogadas

q_table = []
initialize_table(q_table) # Inicializa a Q-Table

alfa = 0.2 # Taxa de aprendizagem
gama = 0.5 # Taxa de desconto

# Modelando o estado inicial
current_platform = 0 # 0
current_direction = 0 # North
current_state = current_platform + (24 * current_direction) # Multiplicação da direção pelo número da plataforma para mapear a linha certa de acordo com a direção

while True:

    action_idx = choose_action(jogadas)
    action = jogadas[action_idx]

    current_value = q_table[current_state][action_idx] # Atribui ao CURRENT VALUE o valor da tabela para o estado CURRENT STATE com a ação escolhida
    
    state_str, reward = cn.get_state_reward(s, action)  # Recebe o estado e a recompensa resultantes da ação

    state_str = str(state_str)
    platform = int(state_str[2:7], 2) # Converting platform number to integer
    direction = int(state_str[7:9], 2) # North = 0 / East = 1 / South = 2 / West= 3

    print(action)
    print(platform)
    print(direction)

    time.sleep(30)
    
    state = platform + (direction * 24) # Nova variável STATE como inteiro para ser usada nos acessos à q_table

    max_value = max(q_table[state][0], q_table[state][1], q_table[state][2]) # Defiine o maior reforço futuro possível

    q_table_update(current_value, action_idx, alfa, gama, reward, max_value) # Atualiza a q_table

    current_state = state # Atualiza o current state antes da próxima jogada
    
  





