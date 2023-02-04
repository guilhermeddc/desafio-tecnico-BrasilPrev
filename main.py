import random

class Player:
  def __init__(self, name):
    self.name = name
    self.position = 0
    self.balance = 300
    self.properties = []
    self.wins = 0
    self.active = True
    
  def move(self, dice_roll):
    self.position += dice_roll
        
  def pay_rent(self, amount):
    self.balance -= amount
        
  def receive_rent(self, amount):
    self.balance += amount

  def won(self):
    self.wins += 1

  def reset(self):
    self.position = 0
    self.balance = 300
    self.properties = []
    self.active = True


class ImpulsivePlayer(Player):
  def __init__(self, name):
    super().__init__(name)

  def decide_to_buy(self, property):
    return self.balance >= property.cost


class DemandingPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
        
  def decide_to_buy(self, property):
    return self.balance >= property.cost and property.rent > 50


class CautiousPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
        
  def decide_to_buy(self, property):
    return self.balance >= property.cost and self.balance - property.cost >= 80


class RandomPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
        
  def decide_to_buy(self, property):
    return self.balance >= property.cost and random.choice([True, False])


class Property:
  def __init__(self, name, cost, rent):
    self.name = name
    self.cost = cost
    self.rent = rent
    self.owner = None
        
  def is_available(self):
    return self.owner is None
    
  def buy(self, player):
    if player.balance >= self.cost:
      player.balance -= self.cost
      self.owner = player
      print(f'{player.name} comprou a propriedade {self.name} por R${self.cost} e ficou com saldo de R${player.balance}')
    else:
      print(f'{player.name} não tem dinheiro suficiente para comprar {self.name}')
            
  def charge_rent(self, player):
    if self.owner and self.owner != player:
      player.pay_rent(self.rent)
      self.owner.receive_rent(self.rent)
      print(f'{player.name} pagou aluguel de R${self.rent} para {self.owner.name} e ficou com saldo de R${player.balance}')
        

class Board:
  def __init__(self, properties):
    self.properties = properties
        
  def move(self, player, dice_roll):
    if player.position + dice_roll >= len(self.properties):
      player.position = (player.position + dice_roll) - len(self.properties)
      player.balance += 100
      print(f'{player.name} passou pela partida e ganhou R$100')

    player.move(dice_roll)
    property = self.properties[player.position]
    property.charge_rent(player)
        

class Game:
  def __init__(self, players, board, matches):
    self.players = players
    self.board = board
    self.matches = matches
    self.matches_time_out = 0
    self.match = 1
    self.turns = []
    random.shuffle(self.players)
        
  def play(self):
    count = 0
    winner = None

    self.match += 1
    
    print(f"\n{self.match}º jogo\n")

    for player in self.players:
      player.reset()
      print(f"{player.name} começou o jogo com R${player.balance}")

    while not winner:
      count += 1
      if count == self.matches + 1:
        self.turns.append(count - 1)
        self.matches_time_out += 1
        print(f"\nO jogo não acabou em {self.matches} rodadas.")
        print(f'Os jogadores que ainda estão no jogo são: {", ".join([player.name for player in self.players])}')
        self.players.sort(key=lambda player: player.balance, reverse=True)
        winner = self.players[0]
        self.players[0].won()
        print(f'O jogador vencedor é {winner.name} com saldo de R${winner.balance}')

        print('\nO jogo acabou!\n\n')
        return

      print(f'\nRodada {count}\n')

      for player in self.players:
        if player.active == True:
          dice_roll = random.randint(1, 6)
          print(f'{player.name} rolou um {dice_roll}')

          self.board.move(player, dice_roll)
          print(f'{player.name} está na posição {player.position} com saldo de R${player.balance}')

          if player.position < len(self.board.properties):
            property = self.board.properties[player.position]

            if player.balance < 0:
              for property in player.properties:
                property.owner = None
              player.active = False
              print(f'{player.name} ficou com saldo negativo e todas as suas propriedades foram vendidas.')

            if property.is_available() and player.decide_to_buy(property):
              player.balance -= property.cost
              property.owner = player
              print(f'{player.name} comprou {property.name} por R${property.cost}')

            if len(self.players) == 1:
              self.turns.append(count)
              winner = self.players[0]
              print(f'{winner.name} ganhou o jogo com saldo de {winner.balance}!')
              break
                    

properties = [
  Property('PINHEIRO MACHADO', 60, 2),
  Property('TANCREDO NEVES', 100, 4),
  Property('MENINO JESUS', 120, 8),
  Property('ITARARÉ', 140, 10),
  Property('DORES', 140, 10),
  Property('LURDES', 160, 12),
  Property('NONOAI', 180, 14),
  Property('URLÂNDIA', 180, 14),
  Property('PATRONATO', 200, 16),
  Property('CATURRITA', 220, 18),
  Property('DIVINA PROVIDENCIA', 220, 18),
  Property('CAROLINA', 240, 20),
  Property('NOAL', 260, 22),
  Property('SÃO JOSÉ', 260, 22),
  Property('SANTA MARTA', 280, 24),
  Property('CAMOBI', 300, 26),
  Property('CAXIAS', 300, 26),
  Property('MEDIANEIRA', 320, 28),
  Property('ROSÁRIO', 350, 35),
  Property('SANTA MARIA', 400, 50),
]

board = Board(properties)
players = [
  ImpulsivePlayer('IMPULSIVO'), 
  DemandingPlayer('EXIGENTE'), 
  CautiousPlayer('CAUTELOSO'), 
  RandomPlayer('ALEATÓRIO')
]
matches = 1000
in_range = 300

game = Game(players, board, matches)

for i in range(in_range):
  game.play()

most_wins = 0
best_player = None

print('-' * 80)
print(f'\nO jogo foi jogado {in_range} vezes.\n')
print('-' * 80)
print(f'\nO jogo demorou em média {sum(game.turns) / len(game.turns)} rodadas para terminar.')
print(f'O jogo demorou {game.matches_time_out} vezes para terminar por timeout.\n')
print('-' * 80)
for player in players:
  print(f'{player.name} venceu {player.wins}, com a porcentagem de vitorias {round((player.wins / in_range) * 100, 2)}%')
  if player.wins > most_wins:
    most_wins = player.wins
    best_player = player
print('-' * 80)
print(f'\n{best_player.name} é o grande vencedor com {most_wins} vitórias!\n')
print('-' * 80)
