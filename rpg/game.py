import inquirer
import random 

## здесь будут классы

class Player:
    def __init__(self, name): ##имя игрока
        self.name = name
    
    def greet(self):
        return self.name

class Character(Player):

    def __init__(self, name, health, mana, stamina, damage):
        super().__init__(name)
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.damage = damage
    
    def greet(self):
        base = super().greet()
        return f"имя: {base} \nздоровье: {self.health}\nмана: {self.mana}\nвыносливость: {self.stamina}\nурон: {self.damage}"

class Levels:

    def __init__(self, level, description, checkpoint):
        self.level = level
        self.description = description
        self.checkpoint = checkpoint

class Enemies:

    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage


    
def Character_creation():
    print("Введите имя персонажа")
    char_name = input()
    print("Выберите класс бойца")
    warrior_type = ["Рыцарь", "Лучник", "Маг"]
    
    question = [
    inquirer.List(
        "choose_class",
        message = "Выбери класс",
        choices = warrior_type
        )
    ]
    answer = inquirer.prompt(question)
    user_choice = answer["choose_class"] ## Создаем переменну. чтобы передать в свитч
    match user_choice:

        case "Рыцарь":
            char = Character(char_name, 7, 3, 8, 5)
            print("Класс Рыцарь:\n", char.greet())
        case "Лучник":
           char = Character(char_name, 6, 4, 6, 6)
           print("Класс Лучник\n", char.greet())
        case "Маг":
            char = Character(char_name, 5, 9, 2, 7)
            print("Класс Маг\n", char.greet())
    return char




#def Charcter_action():
 #   action_type = ["Удар", "Уклонение", "Защита"]


## Структура уровня
def Level_structure():
    num_level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    level_count = 3
    place_decription = [
        "Dungeon",
        "Forest",
        "Desert",
       # "Island",
       # "Citadel",
       # "Castle",
       # "Anor-Londo",
       # "Ruin",
       # "Forogtten-Izalit"
    ]
    bonfire = "костер"
    return num_level, level_count, place_decription, bonfire

##Враги
def Enemies_structure():
    enemies_type = [    
        "goblin",
        "skeleton",
        "cosher"
    ]  
    en_amount = [1, 2, 3]
    return enemies_type, en_amount  

def Game():
    num_level, level_count, place_decription, bonfire = Level_structure()
    enemies_type, en_amount = Enemies_structure()
    char = Character_creation()
    action_type = ["Удар", "Уклонение", "Защита"]
    

    ## Игрок тепается на левел
    for i  in range (level_count):
        ## en_amrand = rand.choice(en_amount) ##генрируем случаное кол-во врагов на будущее
        random_level = Levels(i, place_decription, bonfire)
        match i:
            case 0:
                enemy_char = Enemies("goblin", 3, random.randint(0, 2))
            case 1:
                enemy_char = Enemies("skeleton", 4, random.randint(0, 3))
            case 2:
                enemy_char = Enemies("cosher", 5, random.randint(0, 4))

        print("вы находитесь на уровне", i+1,"вы находитесь в ", place_decription[i], "вы встерчаете ", enemy_char.name)

        while char.health > 0 and enemy_char.health > 0:
            print(char.health, enemy_char.health)
            player_choice = [
                inquirer.List(
                    "choose action",
                    message = "Выбери что делать",
                    choices = action_type
                )
            ]
            player_answer = inquirer.prompt(player_choice)
            answer_action = player_answer["choose action"]
            
            match answer_action:
                case "Удар":
                    enemy_char.health = enemy_char.health - char.damage
                    char.health = char.health - enemy_char.damage
                    print(f"Вы нанесли ", {enemy_char.name}, {char.damage}, "\nВаше здоровье: ", {char.health}, "\nЗдоровье {enemy_char}: ", {enemy_char.health} )
                case "Уклонение":
                    if char.stamina > 0:
                        char.health = char.health - enemy_char.damage + (char.stamina)/4
                        print(f"Вы уклонились от {enemy_char.name}, но он вам нанес {enemy_char.damage}, ваше здоровье {char.health}, ваша выносливость {char.stamina}")
                    else:
                        char.health = char.health - enemy_char.damage
                case "Защита":                    
                    char.stamina = char.stamina - enemy_char.damage
                    print(f"Вы защитились от {enemy_char.name}, но потратили выносливость, теперь ваша выносливость {char.stamina}")
            
            if char.health <= 0 and enemy_char.health >= 1:
                print("Вы мерты")
                break
            elif char.health > 0 and enemy_char.health <= 0:
                print("Вы победили")
                break
            else:
                continue
def main():
    print("Добро пожоловать в RPG")
    Game()

if __name__ == "__main__":
    main()