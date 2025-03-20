import requests
import pandas as pd
from typing import Dict, List, Optional

class PokemonData:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self._pokemon_list = None
        self._sprite_cache = {}
        self._moves_cache = {}
        self._abilities_cache = {}
        self._items_cache = None

    def get_pokemon_list(self) -> List[str]:
        """Fetch list of all Pokemon names."""
        if self._pokemon_list is None:
            try:
                response = requests.get(f"{self.base_url}/pokemon?limit=1000")
                response.raise_for_status()
                data = response.json()
                self._pokemon_list = [pokemon['name'].title() for pokemon in data['results']]
            except requests.RequestException as e:
                raise Exception(f"Failed to fetch Pokemon list: {str(e)}")
        return self._pokemon_list

    def get_pokemon_data(self, name: str) -> Dict:
        """Fetch detailed data for a specific Pokemon."""
        try:
            response = requests.get(f"{self.base_url}/pokemon/{name.lower()}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data for {name}: {str(e)}")

    def get_pokemon_stats(self, name: str) -> Dict[str, int]:
        """Get base stats for a Pokemon."""
        data = self.get_pokemon_data(name)
        return {
            stat['stat']['name']: stat['base_stat']
            for stat in data['stats']
        }

    def get_pokemon_types(self, name: str) -> List[str]:
        """Get types for a Pokemon."""
        data = self.get_pokemon_data(name)
        return [type_data['type']['name'] for type_data in data['types']]

    def get_pokemon_sprite(self, name: str) -> str:
        """Get the official artwork URL for a Pokemon."""
        if name.lower() not in self._sprite_cache:
            data = self.get_pokemon_data(name)
            sprite_url = data['sprites']['other']['official-artwork']['front_default']
            self._sprite_cache[name.lower()] = sprite_url
        return self._sprite_cache[name.lower()]

    def get_pokemon_moves(self, name: str) -> List[Dict[str, str]]:
        """Get available moves for a Pokemon."""
        if name.lower() not in self._moves_cache:
            data = self.get_pokemon_data(name)
            moves = []
            for move_entry in data['moves']:
                move_name = move_entry['move']['name'].replace('-', ' ').title()
                try:
                    move_response = requests.get(move_entry['move']['url'])
                    move_response.raise_for_status()
                    move_data = move_response.json()
                    moves.append({
                        'name': move_name,
                        'type': move_data['type']['name'],
                        'power': move_data.get('power', 0),
                        'accuracy': move_data.get('accuracy', 100)
                    })
                except requests.RequestException:
                    continue
            self._moves_cache[name.lower()] = moves
        return self._moves_cache[name.lower()]

    def get_pokemon_abilities(self, name: str) -> List[Dict[str, str]]:
        """Get available abilities for a Pokemon."""
        if name.lower() not in self._abilities_cache:
            data = self.get_pokemon_data(name)
            abilities = []
            for ability_entry in data['abilities']:
                ability_name = ability_entry['ability']['name'].replace('-', ' ').title()
                try:
                    ability_response = requests.get(ability_entry['ability']['url'])
                    ability_response.raise_for_status()
                    ability_data = ability_response.json()
                    effect_entries = [entry for entry in ability_data['effect_entries'] 
                                   if entry['language']['name'] == 'en']
                    effect = effect_entries[0]['effect'] if effect_entries else "No description available"
                    abilities.append({
                        'name': ability_name,
                        'effect': effect,
                        'is_hidden': ability_entry['is_hidden']
                    })
                except (requests.RequestException, IndexError):
                    continue
            self._abilities_cache[name.lower()] = abilities
        return self._abilities_cache[name.lower()]

    def get_held_items(self) -> List[Dict[str, str]]:
        """Get list of commonly used held items."""
        if self._items_cache is None:
            try:
                # Common competitive items
                items = [
                    {"name": "Choice Band", "effect": "Holder's Attack is 1.5×, but it can only select the first move it executes."},
                    {"name": "Choice Specs", "effect": "Holder's Special Attack is 1.5×, but it can only select the first move it executes."},
                    {"name": "Choice Scarf", "effect": "Holder's Speed is 1.5×, but it can only select the first move it executes."},
                    {"name": "Life Orb", "effect": "Holder's moves do 1.3× damage, but it loses 1/10 its max HP after the attack."},
                    {"name": "Leftovers", "effect": "Holder restores 1/16 of its max HP at the end of each turn."},
                    {"name": "Focus Sash", "effect": "If holder has full HP and would be knocked out, it survives with 1 HP (one-time use)."},
                    {"name": "Expert Belt", "effect": "Holder's super-effective moves do 1.2× damage."},
                    {"name": "Assault Vest", "effect": "Holder's Special Defense is 1.5×, but it can't use status moves."},
                    {"name": "Rocky Helmet", "effect": "If holder is hit by a contact move, the attacker loses 1/6 of its max HP."},
                ]
                self._items_cache = items
            except Exception as e:
                raise Exception(f"Failed to initialize items: {str(e)}")
        return self._items_cache
