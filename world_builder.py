import json
import logging
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)

class WorldBuilder:
    """Handles dynamic world generation and lore management"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        
    async def generate_world(self) -> Dict:
        """Generate the initial world state and lore"""
        prompt = """You are a JSON generator. Create a rich fantasy world for a D&D campaign strictly formatted as valid JSON. Include the following keys with detailed values:

        1. world_name: string - Name of the world
        2. current_era: string - Current era/age
        3. geography: object - Major geographical features and continents
        4. kingdoms: array - List of major kingdoms/empires with name and type
        5. factions: array - List of factions including guilds, religious orders, arcane institutions
        6. conflicts: array - Current conflicts including plot hooks, political tensions, ancient threats
        7. tone: string - Overall mood (hopeful, dark, epic, etc.)
        8. starting_location: string - Starting town or village
        9. immediate_hooks: array - Adventure hooks or events

        Ensure the JSON is valid and parsable. Do not include any explanations or text outside the JSON object.

        Example format:
        {
          "world_name": "Example World",
          "current_era": "Age of Heroes",
          "geography": {...},
          "kingdoms": [...],
          "factions": [...],
          "conflicts": [...],
          "tone": "epic fantasy",
          "starting_location": "a small village",
          "immediate_hooks": [...]
        }
        """
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            world_data = json.loads(response.content)
            logger.info(f"Generated world: {world_data.get('world_name', 'Unknown')}")
            return world_data
        except json.JSONDecodeError:
            logger.error("Failed to parse world data as JSON")
            # Fallback to structured format
            return self._parse_world_fallback(response.content)
    
    def _parse_world_fallback(self, content: str) -> Dict:
        """Fallback parser for world data"""
        return {
            "world_name": "The Forgotten Realms",
            "current_era": "The Age of Heroes",
            "geography": {
                "continents": ["mainland"],
                "features": ["mountains", "forests", "rivers"]
            },
            "kingdoms": [
                {"name": "Kingdom of Light", "type": "human kingdom"},
                {"name": "Elvenwood", "type": "elven realm"}
            ],
            "factions": [
                {"name": "The Adventurer's Guild", "type": "mercenary"},
                {"name": "The Arcane Order", "type": "mages"}
            ],
            "conflicts": ["ancient evil awakening", "political tensions"],
            "tone": "epic fantasy",
            "starting_location": "a small village",
            "immediate_hooks": ["mysterious disappearances"]
        }
    
    async def generate_location(self, location_type: str, context: Dict) -> Dict:
        """Generate a specific location based on type and context"""
        prompt = f"""You are a JSON generator. Create a detailed {location_type} for a D&D campaign strictly formatted as valid JSON.

        Context: {json.dumps(context, indent=2)}

        Include the following keys with detailed values:
        1. name: string - Name of the location
        2. description: string - Detailed description
        3. npcs: array - List of notable NPCs (3-5) with name and role
        4. locations: array - Points of interest (5-7)
        5. events: array - Current events or hooks
        6. atmosphere: string - Atmosphere and sensory details
        7. secrets: array - Secrets or hidden elements

        Ensure the JSON is valid and parsable. Do not include any explanations or text outside the JSON object.

        Example format:
        {{
          "name": "Example Location",
          "description": "A detailed description...",
          "npcs": [...],
          "locations": [...],
          "events": [...],
          "atmosphere": "mysterious and foreboding",
          "secrets": [...]
        }}
        """
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            return json.loads(response.content)
        except:
            return {
                "name": f"The {location_type.title()}",
                "description": f"A typical {location_type}",
                "npcs": [],
                "locations": [],
                "events": [],
                "atmosphere": "mysterious",
                "secrets": []
            }
    
    async def generate_encounter(self, location: str, party_level: int) -> Dict:
        """Generate an encounter based on location and party level"""
        prompt = f"""You are a JSON generator. Create an engaging encounter for a level {party_level} party at {location} strictly formatted as valid JSON.

        Include the following keys with detailed values:
        1. type: string - Encounter type (combat, social, exploration, puzzle)
        2. description: string - Detailed description of the encounter
        3. challenge_rating: number - Challenge level appropriate for party
        4. participants: array - NPCs or monsters involved
        5. environment: object - Environmental factors
        6. rewards: object - Rewards for success
        7. consequences: array - Consequences for failure or choices

        Ensure the JSON is valid and parsable. Do not include any explanations or text outside the JSON object.

        Example format:
        {{
          "type": "combat",
          "description": "A detailed encounter description...",
          "challenge_rating": {party_level},
          "participants": [...],
          "environment": {{...}},
          "rewards": {{...}},
          "consequences": [...]
        }}
        """
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            return json.loads(response.content)
        except:
            return {
                "type": "exploration",
                "description": "You discover something interesting...",
                "challenge_rating": party_level,
                "participants": [],
                "environment": {},
                "rewards": {"xp": 100},
                "consequences": []
            }
    
    async def expand_lore(self, topic: str, existing_lore: Dict) -> str:
        """Expand on existing lore for a specific topic"""
        prompt = f"""Expand on the following topic in the game world:
        
        Topic: {topic}
        Existing Lore: {json.dumps(existing_lore, indent=2)}
        
        Provide rich, detailed lore that maintains consistency with existing world-building.
        Include historical context, cultural significance, and potential adventure hooks."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content
