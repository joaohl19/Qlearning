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

def q_table_update(q_table, linha, coluna, alfa, gama, reward, state):
    q_table[linha][coluna] = (1 - alfa) * q_table[linha][coluna] + alfa * (reward + (gama *  ))


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


while True:
    action_idx = choose_action(jogadas)
    action = jogadas[action_idx]

    # Recebe o estado e a recompensa resultantes da ação
    state, reward = cn.get_state_reward(s, action)

    state = str(state)
    platform = int(state[2:7], 2) # Converting platform number to integer
    direction = state[7:9] # North = 00 / East = 01 / South = 10 / West= 11
    print(action)
    print(platform)
    print(direction)

    time.sleep(5)
    direction_int = int(direction, 2) # Conversão da direção pra inteiro
    
    linha = direction_int * platform # Multiplicação da direção pelo número da plataforma para mapear a linha certa de acordo com a direção

    q_table[linha][action_idx]
    
  





