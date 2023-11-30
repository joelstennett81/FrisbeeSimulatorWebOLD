import random
import string

from django.db.models import Avg
from faker import Faker
from frisbee_simulator_web.models import Player

fake = Faker()


def create_random_player(request):
    player = Player(
        first_name=generate_random_first_name(6),
        last_name=generate_random_last_name(50),
        jersey_number=random.randint(0, 99),
        height=random.randint(60, 90),
        weight=random.randint(60, 90),
        speed=random.randint(60, 90),
        jumping=random.randint(60, 90),
        flick_distance=random.randint(60, 90),
        flick_accuracy=random.randint(60, 90),
        backhand_accuracy=random.randint(60, 90),
        backhand_distance=random.randint(60, 90),
        cutter_defense=random.randint(60, 90),
        handler_defense=random.randint(60, 90),
        agility=random.randint(60, 90),
        handle_cuts=random.randint(60, 90),
        under_cuts=random.randint(60, 90),
        deep_cuts=random.randint(60, 90),
        throw_ability=random.randint(60, 90),
        cut_ability=random.randint(60, 90)
    )
    player.overall = calculate_player_rating(player)
    player.save()
    return player


def generate_random_first_name(length):
    return fake.name()[:length]


def generate_random_last_name(length):
    return fake.last_name()[:length]


def generate_random_city(length):
    return fake.city()[:length]


def generate_random_mascot():
    animals = ['Aardvarks', 'Albatrosses', 'Alligators', 'Alpacas', 'Ants', 'Anteaters', 'Antelopes', 'Apes',
               'Armadillos', 'Asp', 'Baboons', 'Badgers', 'Barracudas', 'Bass', 'Bats', 'Bears', 'Beavers', 'Bees',
               'Bisons', 'Boars', 'Buffaloes', 'Butterflies', 'Camels', 'Carp', 'Caterpillars', 'Cheetahs', 'Chickens',
               'Chimpanzees', 'Cobras', 'Cockroaches', 'Cods', 'Cougars', 'Cows', 'Coyotes', 'Crabs', 'Cranes',
               'Crocodiles', 'Crows', 'Deers',
               'Dingos', 'Dolphins', 'Donkeys', 'Doves', 'Dragonflies', 'Ducks', 'Eagles', 'Echidnas', 'Eels',
               'Elephants',
               'Emus', 'Falcons', 'Ferrets', 'Fishes', 'Flamingos', 'Flies', 'Foxes', 'Frogs', 'Gazelles', 'Geckos',
               'Gerbils', 'Giraffes',
               'Goats',
               'Goldfish',
               'Geese', 'Gorillas', 'Grasshoppers', 'Grizzlies', 'Guinea pigs', 'Hamsters', 'Hares', 'Hawks',
               'Hippopotamuses',
               'Horses', 'Hummingbirds', 'Hyenas', 'Iguanas', 'Impalas', 'Jackals', 'Jaguars', 'Jellyfish', 'Kangaroos',
               'Koalas', 'Koi', 'Komodo dragons', 'Koupreys', 'Kudus', 'Ladybirds', 'Lapwings', 'Lemurs', 'Leopards',
               'Lions',
               'Llamas', 'Lobsters', 'Loris', 'Louses', 'Lynxes', 'Mallards', 'Mammoths', 'Manatees', 'Mandrills',
               'Mantises',
               'Martens', 'Meerkats', 'Minks', 'Moles', 'Mongooses', 'Monkeys', 'Mooses', 'Mosquitoes', 'Moths', 'Mice',
               'Mules',
               'Narwhals', 'Newts', 'Nightingales', 'Octopuses', 'Okapis', 'Opossums', 'Ostriches', 'Otters', 'Owls',
               'Oxes',
               'Oysters', 'Pandas', 'Panthers', 'Parrots', 'Partridges', 'Peacocks', 'Pelicans', 'Penguins',
               'Pheasants', 'Pigs',
               'Pigeons', 'Pikas', 'Polar bears', 'Porcupines', 'Porpoises', 'Possums', 'Prairie dogs', 'Prawns',
               'Puffins',
               'Pumas', 'Pythons', 'Quails', 'Queleas', 'Quokkas', 'Rabbits', 'Raccoons', 'Rails', 'Rams', 'Rats',
               'Ravens',
               'Red deers', 'Red pandas', 'Reindeers', 'Rhinoceroses', 'Right whales', 'Roadrunners', 'Rooks',
               'Rottweilers',
               'Ruffs', 'Salamanders', 'Salmon', 'Sandpipers', 'Sardines', 'Scorpions', 'Seahorses', 'Seals', 'Sharks',
               'Sheep',
               'Shrews', 'Shrimps', 'Snakes', 'Snails', 'Sparrows', 'Spiders', 'Spoonbills', 'Squids', 'Squirrels',
               'Starfish',
               'Stingrays', 'Stinkpots', 'Stoats', 'Sturgeons', 'Swallows', 'Swans', 'Tapirs', 'Tarsiers', 'Termites',
               'Tigers',
               'Toads', 'Trouts', 'Turkeys', 'Turtles', 'Vipers', 'Vultures', 'Walruses', 'Wasps', 'Water buffaloes',
               'Weasels',
               'Whales', 'Whippets', 'Wildebeests', 'Wolves', 'Wolverines', 'Wombats', 'Woodpeckers', 'Worms', 'Wrens',
               'Yaks',
               'Zebras']

    return random.choice(animals)


def calculate_player_rating(player):
    rating_attributes = [
        player.speed, player.jumping, player.flick_distance, player.flick_accuracy,
        player.backhand_accuracy, player.backhand_distance, player.cutter_defense,
        player.handler_defense, player.agility, player.handle_cuts, player.under_cuts,
        player.deep_cuts, player.throw_ability, player.throw_ability
    ]
    rating_sum = sum(rating_attributes)
    overall_rating = rating_sum / len(rating_attributes)
    return overall_rating


def calculate_team_rating(team):
    players = team.players
    return team.players.all().aggregate(Avg('overall_rating')).get('overall_rating__avg')