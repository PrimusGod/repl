import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create database engine
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Failed to create database engine: {str(e)}")
    raise

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    pokemon = relationship("Pokemon", back_populates="team", cascade="all, delete-orphan")

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ability = Column(String)
    ability_description = Column(Text)
    held_item = Column(String)
    held_item_effect = Column(Text)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="pokemon")
    moves = relationship("Move", back_populates="pokemon", cascade="all, delete-orphan")

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    power = Column(Integer)
    accuracy = Column(Integer)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    pokemon = relationship("Pokemon", back_populates="moves")

# Create all tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Failed to create tables: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_team(name: str, pokemon_list: list, moves_dict: dict = None, abilities_dict: dict = None, items_dict: dict = None) -> int:
    """Save a team and its Pokemon to the database."""
    db = SessionLocal()
    try:
        # Check if team name already exists
        existing_team = db.query(Team).filter(Team.name == name).first()
        if existing_team:
            raise ValueError(f"Team name '{name}' already exists")

        # Create new team
        team = Team(name=name)
        db.add(team)
        db.flush()

        # Add Pokemon and their moves to team
        for pokemon_name in pokemon_list:
            pokemon = Pokemon(
                name=pokemon_name,
                team_id=team.id,
                ability=abilities_dict.get(pokemon_name, {}).get('name') if abilities_dict else None,
                ability_description=abilities_dict.get(pokemon_name, {}).get('effect') if abilities_dict else None,
                held_item=items_dict.get(pokemon_name, {}).get('name') if items_dict else None,
                held_item_effect=items_dict.get(pokemon_name, {}).get('effect') if items_dict else None
            )
            db.add(pokemon)
            db.flush()

            # Add moves if provided
            if moves_dict and pokemon_name in moves_dict:
                for move_data in moves_dict[pokemon_name]:
                    move = Move(
                        name=move_data['name'],
                        type=move_data['type'],
                        power=move_data.get('power', 0),
                        accuracy=move_data.get('accuracy', 100),
                        pokemon_id=pokemon.id
                    )
                    db.add(move)

        db.commit()
        return team.id
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_team(team_name: str) -> dict:
    """Get a team's Pokemon list and their moves by team name."""
    db = SessionLocal()
    try:
        team = db.query(Team).filter(Team.name == team_name).first()
        if team:
            result = {'pokemon': [], 'moves': {}, 'abilities': {}, 'items': {}}
            for pokemon in team.pokemon:
                result['pokemon'].append(pokemon.name)
                result['moves'][pokemon.name] = [
                    {
                        'name': move.name,
                        'type': move.type,
                        'power': move.power,
                        'accuracy': move.accuracy
                    }
                    for move in pokemon.moves
                ]
                if pokemon.ability:
                    result['abilities'][pokemon.name] = {
                        'name': pokemon.ability,
                        'effect': pokemon.ability_description
                    }
                if pokemon.held_item:
                    result['items'][pokemon.name] = {
                        'name': pokemon.held_item,
                        'effect': pokemon.held_item_effect
                    }
            return result
        return None
    except SQLAlchemyError as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()

def get_all_teams() -> list:
    """Get all team names."""
    db = SessionLocal()
    try:
        teams = db.query(Team).all()
        return [team.name for team in teams]
    except SQLAlchemyError as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()
