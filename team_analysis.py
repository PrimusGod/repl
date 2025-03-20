import typing import Dict, List, Set, Tuple

class TeamAnalyzer:
    def __init__(self):
        self.type_chart = {
            'normal': {'weak': ['fighting'], 'immune': ['ghost']},
            'fighting': {'weak': ['flying', 'psychic', 'fairy']},
            'flying': {'weak': ['electric', 'ice', 'rock']},
            'poison': {'weak': ['ground', 'psychic']},
            'ground': {'weak': ['water', 'ice', 'grass'], 'immune': ['electric']},
            'rock': {'weak': ['water', 'grass', 'fighting', 'ground', 'steel']},
            'bug': {'weak': ['flying', 'rock', 'fire']},
            'ghost': {'weak': ['ghost', 'dark'], 'immune': ['normal', 'fighting']},
            'steel': {'weak': ['fighting', 'ground', 'fire']},
            'fire': {'weak': ['water', 'ground', 'rock']},
            'water': {'weak': ['electric', 'grass']},
            'grass': {'weak': ['flying', 'poison', 'bug', 'fire', 'ice']},
            'electric': {'weak': ['ground']},
            'psychic': {'weak': ['bug', 'ghost', 'dark']},
            'ice': {'weak': ['fighting', 'rock', 'steel', 'fire']},
            'dragon': {'weak': ['ice', 'dragon', 'fairy']},
            'dark': {'weak': ['fighting', 'bug', 'fairy']},
            'fairy': {'weak': ['poison', 'steel'], 'immune': ['dragon']}
        }

    def analyze_team_weaknesses(self, team_types: List[List[str]]) -> Dict[str, int]:
        """Analyze team weaknesses based on Pokemon types."""
        weakness_count = {}
        for type_name in self.type_chart.keys():
            weakness_count[type_name] = 0

        for pokemon_types in team_types:
            for type_name in pokemon_types:
                if type_name in self.type_chart:
                    for weak_against in self.type_chart[type_name]['weak']:
                        weakness_count[weak_against] += 1

        return weakness_count

    def get_detailed_weakness_analysis(self, team_types: List[List[str]]) -> Dict[str, Dict]:
        """Provide detailed analysis of team weaknesses with severity levels."""
        weakness_count = self.analyze_team_weaknesses(team_types)

        analysis = {}
        for type_name, count in weakness_count.items():
            if count >= 3:
                severity = "Critical"
                impact = "Your team is highly vulnerable"
            elif count == 2:
                severity = "Moderate"
                impact = "Your team shows some vulnerability"
            elif count == 1:
                severity = "Minor"
                impact = "Your team has slight vulnerability"
            else:
                severity = "None"
                impact = "Your team is well-protected"

            analysis[type_name] = {
                "count": count,
                "severity": severity,
                "impact": impact
            }

        return analysis

    def generate_strategic_advice(self, team_types: List[List[str]]) -> List[str]:
        """Generate specific strategic advice based on team composition."""
        analysis = self.get_detailed_weakness_analysis(team_types)
        advice = []

        # Critical weaknesses advice
        critical_weaknesses = [t for t, data in analysis.items() if data["severity"] == "Critical"]
        if critical_weaknesses:
            advice.append(f"⚠️ Critical: Consider adding Pokemon resistant to {', '.join(critical_weaknesses)}")

        # Type coverage gaps
        coverage = self.get_team_coverage(team_types)
        missing_coverage = set(self.type_chart.keys()) - coverage
        if missing_coverage:
            advice.append(f"🎯 Offensive: Your team lacks coverage against {', '.join(missing_coverage)}")

        # Team composition advice
        type_counts = {}
        for types in team_types:
            for t in types:
                type_counts[t] = type_counts.get(t, 0) + 1

        # Check for over-reliance on certain types
        over_relied = [t for t, count in type_counts.items() if count >= 3]
        if over_relied:
            advice.append(f"⚖️ Balance: Your team might be too reliant on {', '.join(over_relied)} type Pokemon")

        return advice

    def suggest_pokemon_types(self, current_types: List[List[str]]) -> List[str]:
        """Suggest Pokemon types to cover team weaknesses."""
        weaknesses = self.analyze_team_weaknesses(current_types)
        major_weaknesses = [t for t, count in weaknesses.items() if count >= 2]

        suggested_types = set()
        for weakness in major_weaknesses:
            for type_name, matchups in self.type_chart.items():
                if 'immune' in matchups and weakness in matchups['immune']:
                    suggested_types.add(type_name)
                elif weakness in self.type_chart[type_name]['weak']:
                    suggested_types.add(type_name)

        return list(suggested_types)

    def get_team_coverage(self, team_types: List[List[str]]) -> Set[str]:
        """Get the types that the team is effective against."""
        coverage = set()
        for pokemon_types in team_types:
            for type_name in pokemon_types:
                if type_name in self.type_chart:
                    coverage.update(self.type_chart[type_name]['weak'])
        return coverage
