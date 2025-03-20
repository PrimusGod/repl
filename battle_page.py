import streamlit as st
from battle_simulator import BattlePokemon, BattleSimulator
from pokemon_data import PokemonData

def create_battle_pokemon(pokemon_data: PokemonData, name: str, moves: list, 
                        ability: dict, held_item: dict) -> BattlePokemon:
    """Create a BattlePokemon instance from the given data."""
    stats = pokemon_data.get_pokemon_stats(name)
    types = pokemon_data.get_pokemon_types(name)
    return BattlePokemon(name, stats, moves, types, ability, held_item)

def display_pokemon_status(pokemon_data: dict, is_player: bool = True):
    """Display Pokemon battle status with a health bar."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write(f"**{pokemon_data['name']}**")
    with col2:
        # Create health bar
        health_percentage = (pokemon_data['current_hp'] / pokemon_data['max_hp']) * 100
      
