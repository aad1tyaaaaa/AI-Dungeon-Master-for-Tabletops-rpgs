import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

logger = logging.getLogger(__name__)

class NPC:
    """Represents an NPC with personality and memory"""
    
    def __init__(self, name: str, description: str, personality: Dict):
        self.name = name
        self.description = description
        self.personality = personality
        self.memory = ConversationBufferMemory(
            memory_key="conversations",
            return_messages=True,
            max_token_limit=1000
        )
        self.relationships = {}
        self.current_location = None
        self.stats = {
            "level": personality.get("level", 1),
            "hp": personality.get("hp", 10),
            "race": personality.get("race", "human"),
            "class": personality.get("class", "commoner")
        }
        self.last_interaction = datetime.now()
    
    def get_personality_prompt(self) -> str:
        """Get the personality prompt for this NPC"""
        return f"""You are {self.name}, {self.description}.
        
        Personality traits:
        - Demeanor: {self.personality.get('demeanor', 'neutral')}
        - Speech pattern: {self.personality.get('speech_pattern', 'normal')}
        - Values: {', '.join(self.personality.get('values', ['survival']))}
        - Fears: {', '.join(self.personality.get('fears', ['unknown']))}
        - Goals: {', '.join(self.personality.get('goals', ['live peacefully']))}
        
        When speaking, embody these traits fully. Use appropriate dialect, 
        mannerisms, and emotional responses based on your personality.
        Remember past interactions and maintain consistency."""
    
    def update_relationship(self, player_name: str, change: int):
        """Update relationship score with a player"""
        current = self.relationships.get(player_name, 0)
        self.relationships[player_name] = max(-10, min(10, current + change))
    
    def get_relationship_status(self, player_name: str) -> str:
        """Get relationship status with player"""
        score = self.relationships.get(player_name, 0)
        if score >= 8:
            return "loyal friend"
        elif score >= 5:
            return "friendly"
        elif score >= 1:
            return "cordial"
        elif score >= -1:
            return "neutral"
        elif score >= -5:
            return "suspicious"
        else:
            return "hostile"

class NPCManager:
    """Manages NPCs and their interactions"""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.npcs: Dict[str, NPC] = {}
        self.active_npcs: List[str] = []
    
    async def create_npc(self, name: str, description: str, personality: Dict) -> NPC:
        """Create a new NPC"""
        npc = NPC(name, description, personality)
        self.npcs[name] = npc
        return npc
    
    async def generate_npc(self, location: str, role: str) -> NPC:
        """Generate an NPC based on location and role"""
        prompt = f"""Create a detailed NPC for a D&D campaign.
        
        Location: {location}
        Role: {role}
        
        Include:
        - Full name and title
        - Physical description
        - Personality traits (demeanor, speech pattern, values, fears, goals)
        - Background story
        - Current motivations
        - Secrets or hidden knowledge
        
        Format as JSON with: name, description, personality (object), background, 
        secrets, current_motivation."""
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            npc_data = json.loads(response.content)
            npc = await self.create_npc(
                npc_data["name"],
                npc_data["description"],
                npc_data["personality"]
            )
            npc.background = npc_data.get("background", "")
            npc.secrets = npc_data.get("secrets", [])
            npc.current_motivation = npc_data.get("current_motivation", "")
            
            logger.info(f"Generated NPC: {npc.name}")
            return npc
            
        except Exception as e:
            logger.error(f"Error generating NPC: {e}")
            # Fallback NPC
            return await self.create_npc(
                "Generic NPC",
                f"A {role} at {location}",
                {
                    "demeanor": "helpful",
                    "speech_pattern": "normal",
                    "values": ["honesty", "kindness"],
                    "fears": ["danger"],
                    "goals": ["help others"]
                }
            )
    
    def get_npc(self, name: str) -> Optional[NPC]:
        """Get an NPC by name"""
        return self.npcs.get(name)
    
    def get_active_npcs(self) -> List[Dict]:
        """Get all active NPCs"""
        return [
            {
                "name": npc.name,
                "description": npc.description,
                "location": npc.current_location,
                "relationship": npc.get_relationship_status("player")
            }
            for name, npc in self.npcs.items()
            if name in self.active_npcs
        ]
    
    def add_npc_to_scene(self, npc_name: str):
        """Add an NPC to the current scene"""
        if npc_name in self.npcs:
            self.active_npcs.append(npc_name)
    
    def remove_npc_from_scene(self, npc_name: str):
        """Remove an NPC from the current scene"""
        if npc_name in self.active_npcs:
            self.active_npcs.remove(npc_name)
    
    async def interact_with_npc(self, npc_name: str, player_input: str) -> str:
        """Handle interaction with a specific NPC"""
        npc = self.get_npc(npc_name)
        if not npc:
            return f"{npc_name} is not present."
        
        # Update last interaction
        npc.last_interaction = datetime.now()
        
        # Get NPC's personality prompt
        system_prompt = npc.get_personality_prompt()
        
        # Get conversation history
        history = npc.memory.chat_memory.messages
        
        # Generate response
        prompt = f"""{system_prompt}
        
        Previous conversation: {history[-5:] if history else "None"}
        
        Player says: {player_input}
        
        Respond as {npc.name}, staying in character and considering your personality traits."""
        
        response = await self.llm.ainvoke(prompt)
        
        # Update memory
        npc.memory.chat_memory.add_user_message(player_input)
        npc.memory.chat_memory.add_ai_message(response.content)
        
        return response.content
    
    async def generate_random_encounter(self, location: str) -> str:
        """Generate a random NPC encounter"""
        roles = ["merchant", "traveler", "guard", "villager", "mysterious stranger", "bard", "priest", "thief"]
        role = roles[len(self.npcs) % len(roles)]
        
        npc = await self.generate_npc(location, role)
        self.add_npc_to_scene(npc.name)
        
        return f"You encounter {npc.name}, {npc.description}"
