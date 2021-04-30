import time
import random


class Unit:
    def __init__(self, name, health, armor, mana, melee_power, magic_power, modifier):
        self.name = name
        self.health = health
        self.armor = armor
        self.mana = mana
        self.melee_power = melee_power
        self.magic_power = magic_power
        self.modifier = modifier
        self.ability_dict = {}

    def cast_ability(self, ability, power_type):
        full_damage = self.ability_dict[ability].ability_damage + power_type
        return full_damage

    @staticmethod
    def get_ability(usable_abilities, spell_to_use):
        if spell_to_use is None:
            spell_to_use = random.choice(list(usable_abilities.keys()))
            chosen_ability = spell_to_use
            return chosen_ability
        else:
            spell_list = list(usable_abilities.keys())
            chosen_ability = spell_list[spell_to_use - 1]
            print(chosen_ability)
            return chosen_ability

    # these need to be different because when you take damage you may be weak to something
    def take_damage(self, incoming_damage, ability_name, damage_type=None):
        if self.armor >= incoming_damage:
            leftover_damage = 1
        else:
            leftover_damage = incoming_damage - self.armor
        self.health = self.health - leftover_damage
        print(f"{self.name} has been hit with a {ability_name} for {leftover_damage}! "
              f"{self.name}'s new health is {self.health}")
        time.sleep(.1)

    # when you're dealing damage you're selecting an ability and
    def deal_damage(self, opponent, outgoing_damage, ability_name):
        if self.armor >= outgoing_damage:
            leftover_damage = 1
        else:
            leftover_damage = outgoing_damage - self.armor

        opponent.health -= leftover_damage
        print(f"{opponent.name} has been hit with a {ability_name} for {leftover_damage}! "
              f"{opponent.name}'s new health is {opponent.health}")
        time.sleep(.1)

    def __str__(self):
        return self.name


class AbilityValues:
    def __init__(self, ability_damage, ability_type, mana_cost, damage_type):
        self.ability_damage = ability_damage  # raw damage number
        self.ability_type = ability_type  # type of damage, melee or magic
        self.mana_cost = mana_cost  # cost of mana
        self.damage_type = damage_type


class HeroClass(Unit):
    def __init__(self, name, health, armor, mana, melee_power, magic_power, modifier):
        super().__init__(name=name,
                         health=health,
                         armor=armor,
                         mana=mana,
                         melee_power=melee_power,
                         magic_power=magic_power,
                         modifier=modifier)
        self.experience = 0
        self.level = 1
        self.level_modifier = 1

    def experience_gain(self, experience_earned):
        self.experience += experience_earned
        if self.experience >= self.level * self.level_modifier:
            self.level += 1
            self.experience = 0
            self.level_modifier *= .25

    def print_level(self):
        print(f"Your current level is {self.experience}")


class Warrior(HeroClass):
    def __init__(self, name, modifier=0):
        super().__init__(name,
                         health=100,
                         armor=35,
                         mana=0,
                         melee_power=15,
                         magic_power=0,
                         modifier=0)

        self.ability_dict = {"Basic Attack": AbilityValues(ability_damage=10 + modifier,
                                                           ability_type=self.melee_power,
                                                           mana_cost=0,
                                                           damage_type="Physical"),
                             "Smash": AbilityValues(ability_damage=15 + modifier,
                                                    ability_type=self.melee_power,
                                                    mana_cost=0,
                                                    damage_type="Physical")}


class Wizard(HeroClass):
    def __init__(self, name, modifier=0):
        super().__init__(name,
                         health=25,
                         armor=15,
                         mana=100,
                         melee_power=5,
                         magic_power=5,
                         modifier=0)

        self.ability_dict = {"Fireball": AbilityValues(ability_damage=15 + modifier,
                                                       ability_type=self.magic_power,
                                                       mana_cost=10,
                                                       damage_type="Fire"),
                             "Lightning Bolt": AbilityValues(ability_damage=5,
                                                             ability_type=self.magic_power,
                                                             mana_cost=10,
                                                             damage_type="Lightning")}


class Goblin(Unit):
    def __init__(self, modifier=0):
        super().__init__(name="Goblin",
                         health=60,
                         armor=5,
                         mana=0,
                         melee_power=2.5,
                         magic_power=0,
                         modifier=0)
        self.experience_value = 50
        self.ability_dict = {"Basic Attack": AbilityValues(ability_damage=5 + modifier,
                                                           ability_type=self.melee_power,
                                                           mana_cost=0,
                                                           damage_type="Physical")}

    def take_damage(self, damage, ability_name, damage_type=None):
        if damage_type == "Fire":
            damage *= 1.5
        super().take_damage(damage, ability_name, damage_type)

    def deal_damage(self, opponent, damage=None, ability_name=None):
        ability_name = self.get_ability(usable_abilities=self.ability_dict, spell_to_use=None)
        damage = self.cast_ability(ability=ability_name, power_type=self.ability_dict[ability_name].ability_type)
        super().deal_damage(opponent, damage, ability_name)


class Cyclops(Unit):
    def __init__(self, modifier=0):
        super().__init__(name="Cyclops",
                         health=175,
                         armor=20,
                         mana=0,
                         melee_power=25,
                         magic_power=0,
                         modifier=0)
        self.chance_to_hit = 100
        self.wild_swing_chance = 0
        self.experience_value = 200
        self.modifier = modifier
        self.ability_dict = {"Basic Attack": 20 + modifier,
                             "Wild Swing": 30 + modifier}

    def take_damage(self, damage, ability_name, damage_type=None):
        if damage_type == "Lightning":
            self.chance_to_hit = random.randrange(0, 100)
            print("You struck the ogre with lightning!")
            if self.chance_to_hit > 65:
                print(f"The {self.name} can still see nearly perfectly!")
            elif self.chance_to_hit >= 35 & self.chance_to_hit < 65:
                print(f"The {self.name} has been struck, there's a chance it will miss!")
            elif self.chance_to_hit < 35:
                print(f"The {self.name} has been blinded and cannot attack outside of wild swings!")
            super().take_damage(damage, ability_name, damage_type)

    def wild_swing(self):
        self.wild_swing_chance = random.randrange(0, 100)

    def deal_damage(self, opponent, damage=0, ability_name=None):
        self.wild_swing()
        if self.wild_swing_chance > 90:
            damage = self.ability_dict["Wild Swing"]
            ability_name = "Wild Swing"
        else:
            if self.chance_to_hit < 35:
                print(f"{self.name} is blinded and cannot attack!")
                damage = 0
            else:
                if self.chance_to_hit <= 65:
                    print(f"{self.name} is partially blinded and does reduced damage")
                    damage = self.ability_dict["Basic Attack"] - (self.chance_to_hit * .5)
                    ability_name = "Basic Attack"
        super().deal_damage(opponent, damage, ability_name)


class Dungeon:
    def __init__(self):
        self.rooms = 0
        self.enemies = {}
        self.units = [Goblin, Cyclops]

    def generate_rooms(self):
        self.rooms = random.randrange(1, 12)
        if self.rooms == 1:
            self.enemies[1]: Cyclops(modifier=5)
        else:
            count = 1
            while count != self.rooms:
                unit = random.choice(self.units)
                self.enemies[count] = unit()
                count += 1

    def enter_dungeon_prompt(self, user_class):
        print("You enter a dark and dingy dungeon, you can't see very far ahead. "
              "If you enter now you fear you may not be able to come out until you reach the other side.")
        while True:
            user_input = input("Would you like to enter the dungeon? (yes/no)\n")
            if user_input == "yes":
                self.traverse_dungeon(user_class)
                return True
            elif user_input == "no":
                print("You decide you're not strong enough yet and head back to town")
                return False

    def traverse_dungeon(self, user_class):
        count = 1
        while count != self.rooms:
            print(f"You enter the room and discover a {self.enemies[count]}, it's a fight to the death!")
            while self.enemies[count].health > 0:
                fight_mechanics(user_class, enemy_object=self.enemies[count])


def introduction():
    # Beginning of game. Player assigns their name.
    print("You arrive to a faraway town plagued by a scourge of monsters.")
    print("They seep from nearby forests and caves, vandalizing the village and attacking the townspeople.")
    print("A tired guard stationed at the gate hails you as a stranger...")
    player_name = input("Guard: Halt. State your name.\n")
    print(f"Guard: Oh, yes. {player_name} the mercenary. We've been expecting you.")
    print("Guard: I haven't been informed of your capabilities. What is your battle discipline?")
    return player_name


def select_class():
    hero_classes = ["Warrior", "Wizard"]
    hero_classes_string = " or ".join(hero_classes)
    user_choice = ""
    while user_choice not in hero_classes:
        user_choice = input(f"Are you a {hero_classes_string}?\n").capitalize()
    return user_choice


def confirm_class_selection(name):
    selected_choice = select_class()
    confirmation = ""
    while confirmation != "yes":
        confirmation = input(f"Ah so you're a {selected_choice}? (yes or no)\n").lower()
        if confirmation == "no":
            selected_choice = select_class()
    if selected_choice == "Warrior":
        return Warrior(name)
    elif selected_choice == "Wizard":
        return Wizard(name)


def tutorial_fight_prompt():
    fight_input = ""
    while fight_input != "yes":
        fight_input = input("There have been some pesky goblins around, can you go take care of them for us? "
                            "(yes or no)\n").lower()
    return True


def fight_mechanics(user_class, enemy_object, count=0):
    selected_ability_name = get_fight_input(user_class, enemy=enemy_object)
    ability_type = user_class.ability_dict[selected_ability_name].ability_type
    damage = user_class.cast_ability(selected_ability_name, ability_type)
    ability_damage_type = user_class.ability_dict[selected_ability_name].damage_type
    enemy_object.take_damage(damage=damage, ability_name=selected_ability_name, damage_type=ability_damage_type)
    enemy_object.deal_damage(opponent=user_class)
    count += 1

    if user_class.health <= 0:
        print(f"You have died! RIP {user_class.name}")
        return False
    elif enemy_object.health <= 0:
        print(f"You have killed {enemy_object.name}")
        user_class.experience += enemy_object.experience_value
        return True
    else:
        print(f"After turn {count} - ")
        print(f"My health is at - {user_class.health}")
        print(f"{enemy_object.name}'s health is at - {enemy_object.health}")


def simulate_tutorial_fight(user_class):
    goblin1 = Goblin(modifier=-3)
    print("Goblins are susceptible to fire!")
    while True:
        fight_conclusion = fight_mechanics(user_class=user_class, enemy_object=goblin1)
        if fight_conclusion is True:
            print("You killed it! Thank you! You look strong, "
                  "why don't you come back to the inn and I'll show you around the town?\n")
            break


def get_fight_input(user_class, enemy):
    usable_abilities = user_class.ability_dict
    num_of_abilities = len(user_class.ability_dict)
    num = 0
    spells = list(usable_abilities.keys())
    spell_sentence = ""
    for i in spells:
        if num + 1 != len(spells):
            spell_sentence += f"({num+1}){spells[num]}, "
        else:
            spell_sentence += f"({num+1}){spells[num]}"
        num += 1

    print(f"The spells you can use are {spell_sentence}\n")

    while True:
        spell_to_use = input(f"What would you like to do to {enemy}?\n")

        if " " in spell_to_use:
            chosen_ability_name = " ".join(word.capitalize() for word in spell_to_use.split())
        else:
            chosen_ability_name = spell_to_use.capitalize()
        if chosen_ability_name in spells:
            return chosen_ability_name
        elif chosen_ability_name.isdigit() is True:
            if int(chosen_ability_name) <= num_of_abilities:
                chosen_ability_name = int(chosen_ability_name)
                ability_name = user_class.get_ability(usable_abilities=usable_abilities,
                                                      spell_to_use=chosen_ability_name)
                return ability_name


def read_monster_book():
    book = {1: "Goblins are susceptible to fire, they can't stand the heat!",
            2: "Cyclops have one eye and are large and angry! "
               "If you can shoot them in the eye with a bolt of lightning though they can't see you!"}
    print("You can read about various monsters here, press enter to go through each page or enter a specific page "
          "to skip there!")
    print("Enter 'quit' to leave")

    page_count = 1
    page_nums = list(book.keys())
    while True:
        user_input = input()
        if len(user_input) == 0:
            print(book[page_count])
            page_count += 1
            if page_count > len(page_nums):
                page_count = 1
        elif user_input.isdigit() and int(user_input) <= len(page_nums):
            print(book[page_count])
        elif user_input.lower() == "quit":
            break
        else:
            print("Please make sure to enter quit or a number, or turn the page with enter")


def dungeon_crawl(user_class):
    print("Would you like to enter a dungeon? (yes/no)")
    user_input = ""
    while user_input != "yes" or user_input != "no":
        user_input = input().lower()
        if user_input == "yes":
            dungeon = Dungeon()
            dungeon.generate_rooms()
            enter_dunegon = dungeon.enter_dungeon_prompt(user_class)
            if enter_dunegon is True:
                dungeon.traverse_dungeon(user_class)
            else:
                break


def go_to_inn():
    pass


def choose_option(user_class):
    print("There are several things to do in town, what would you like to do? (Choose a number, 1, 2 or 3)")
    print("1. Read about the book of monsters\n"
          "2. Go back out to continue fighting\n"
          "3. Sleep at the Inn and spend your experience\n"
          "4. Quit game")
    user_input = ""
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4":
        user_input = input("What would you like to do?\n").strip()
    if user_input == "1":
        read_monster_book()
    elif user_input == "2":
        dungeon_crawl(user_class)
    elif user_input == "3":
        go_to_inn()
    elif user_input == "4":
        return False


def main():
    name = introduction()
    user_class = confirm_class_selection(name)
    prompt = tutorial_fight_prompt()
    if prompt:
        simulate_tutorial_fight(user_class)
    while True:
        game = choose_option(user_class)
        if game is False:
            break


main()
