import json
from unittest import TestCase
from Ex4.src.client_python.pokemon import Pokemon


class TestPokemon(TestCase):
    json_dict = {
        "value": 5.0,
        "type": -1,
        "pos": "35.197656770719604,32.10191878639921,0.0"
    }

    json_dict1 = {
        "value": 12.0,
        "type": 1,
        "pos": "35.1976567707196,32.101918786399,0.0"
    }

    json_dict2 = {
        "value": 55.0,
        "type": -1,
        "pos": "35.197656770719,32.10191878639,0.0"
    }

    def test_load_pokemon(self):
        pokemon: Pokemon = Pokemon()
        pokemon.load_pokemon(self.json_dict)
        self.assertEqual(5.0, pokemon.value)
        self.assertEqual(-1, pokemon.type)
        self.assertEqual((35.197656770719604, 32.10191878639921, 0.0), pokemon.pos)

        pokemon1: Pokemon = Pokemon()
        pokemon1.load_pokemon(self.json_dict1)
        self.assertEqual(12.0, pokemon1.value)
        self.assertEqual(1, pokemon1.type)
        self.assertEqual((35.1976567707196, 32.101918786399, 0.0), pokemon1.pos)

        pokemon2: Pokemon = Pokemon()
        pokemon2.load_pokemon(self.json_dict2)
        self.assertEqual(55.0, pokemon2.value)
        self.assertEqual(-1, pokemon2.type)
        self.assertEqual((35.197656770719, 32.10191878639, 0.0), pokemon2.pos)
