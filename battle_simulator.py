from typing import Dict, List, Optional
import random

class BattlePokemon:
    def __init__(self, name: str, stats: Dict[str, int], moves: List[Dict], 
                 types: List[str], ability: Dict, held_item: Dict):
        self.name = name
        self.max_hp = stats['hp']
        self.current_hp = stats['hp']
        self.attack = stats['attack']
        self.defense = stats['defense']
        self.special_attack = stats['special-attack']
        self.special_defense = stats['special-defense']
        self.speed = stats['speed']
        self.moves = moves
        self.types = types
        self.ability = ability
        self.held_item = held_item
        self.status = None

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def calculate_damage(self, move: Dict, opponent: 'BattlePokemon') -> int:
        # Base damage calculation
        power = move['power']
        if power == 0:  # Status moves don't deal damage
            return 0

        # Get attack and defense stats based on move category
        # For simplicity, we'll assume physical/special based on power
        if power > 0:
            attack = self.attack
            defense = opponent.defense
        else:
            attack = self.special_attack
            defense = opponent.special_defense

        # Calculate base damage
        damage = ((2 * 50 / 5 + 2) * power * attack / defense) / 50 + 2

        # Apply STAB (Same Type Attack Bonus)
        if move['type'] in self.types:
            damage *= 1.5

        # Apply type effectiveness (simplified)
        type_multiplier = 1.0
        # This will be expanded with the full type chart

        damage *= type_multiplier

        # Random factor (85-100%)
        damage *= random.uniform(0.85, 1.0)

        return int(damage)

class BattleSimulator:
    def __init__(self, player_team: List[BattlePokemon], opponent_team: List[BattlePokemon]):
        self.player_team = player_team
        self.opponent_team = opponent_team
        self.current_player_pokemon = 0
        self.current_opponent_pokemon = 0
        self.turn = 0

    def get_active_pokemon(self) -> tuple[BattlePokemon, BattlePokemon]:
        return (self.player_team[self.current_player_pokemon],
                self.opponent_team[self.current_opponent_pokemon])

    def execute_turn(self, player_move_index: int) -> Dict[str, any]:
        """Execute a single turn of battle."""
        player_pokemon, opponent_pokemon = self.get_active_pokemon()
        
        # Select opponent's move randomly
        opponent_move_index = random.randint(0, len(opponent_pokemon.moves) - 1)
        
        # Get moves
        player_move = player_pokemon.moves[player_move_index]
        opponent_move = opponent_pokemon.moves[opponent_move_index]
        
        # Determine who goes first based on Speed
        first = player_pokemon if player_pokemon.speed >= opponent_pokemon.speed else opponent_pokemon
        second = opponent_pokemon if first == player_pokemon else player_pokemon
        first_move = player_move if first == player_pokemon else opponent_move
        second_move = opponent_move if first == player_pokemon else player_move
        
        turn_results = {
            'first_attacker': first.name,
            'second_attacker': second.name,
            'first_move': first_move['name'],
            'second_move': second_move['name'],
            'first_damage': 0,
            'second_damage': 0,
            'fainted': []
        }
        
        # Execute first move
        if not first.is_fainted():
            damage = first.calculate_damage(first_move, second)
            second.current_hp -= damage
            turn_results['first_damage'] = damage
            
            if second.is_fainted():
                turn_results['fainted'].append(second.name)
        
        # Execute second move
        if not second.is_fainted():
            damage = second.calculate_damage(second_move, first)
            first.current_hp -= damage
            turn_results['second_damage'] = damage
            
            if first.is_fainted():
                turn_results['fainted'].append(first.name)
        
        self.turn += 1
        return turn_results

    def get_battle_status(self) -> Dict[str, any]:
        """Get current battle status."""
        player_pokemon, opponent_pokemon = self.get_active_pokemon()
        
        return {
            'turn': self.turn,
            'player_pokemon': {
                'name': player_pokemon.name,
                'current_hp': player_pokemon.current_hp,
                'max_hp': player_pokemon.max_hp,
                'moves': player_pokemon.moves
            },
            'opponent_pokemon': {
                'name': opponent_pokemon.name,
                'current_hp': opponent_pokemon.current_hp,
                'max_hp': opponent_pokemon.max_hp
            }
        }

    def is_battle_over(self) -> Optional[str]:
        """Check if the battle is over and return the winner if it is."""
        player_fainted = all(p.is_fainted() for p in self.player_team)
        opponent_fainted = all(p.is_fainted() for p in self.opponent_team)
        
        if player_fainted:
            return "opponent"
        elif opponent_fainted:
            return "player"
        return None
