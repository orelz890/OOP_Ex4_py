import json
from unittest import TestCase
from Ex4.src.client_python.pokemon import Pokemon


class TestPokemon(TestCase):
    json_dict = {
        "value": 5.0,
        "type": -1,
        "pos": "35.197656770719604,32.10191878639921,0.0"
    }


    def test_load_pokemon(self):
        pokemon: Pokemon = Pokemon()
        pokemon.load_pokemon(self.json_dict)
        print(pokemon.value)
        self.assertEqual(5.0, pokemon.value)
        self.assertEqual(-1, pokemon.type)
        self.assertEqual((35.197656770719604, 32.10191878639921, 0.0), pokemon.pos)
