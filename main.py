#!/usr/bin/env python3
"""
AI Dungeon Master - Main Entry Point
An interactive AI-powered Dungeon Master for tabletop RPGs
"""

import asyncio
import logging
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.columns import Columns
from rich.table import Table
from rich.layout import Layout
from rich.align import Align


from config import Config
from world_builder import WorldBuilder
from npc_manager import NPCManager
from langchain_google_genai import ChatGoogleGenerativeAI

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

import uvicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Try to import audio handler, make it optional
try:
    from audio_handler import AudioHandler
    AUDIO_AVAILABLE = True
except ImportError as e:
    logger.info(f"Audio functionality not available: {e}")
    AUDIO_AVAILABLE = False
    AudioHandler = None

class AIDungeonMaster:
    """Main game orchestrator"""

    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.audio_handler = None
        self.world_builder = None
        self.npc_manager = None
        self.llm = None
        self.game_state = {
            "world": None,
            "current_location": None,
            "player_character": None,
            "party": [],
            "inventory": [],
            "active_quests": [],
            "voice_enabled": False
        }

    def print_header(self):
        """Print the game header"""
        from rich.text import Text
        from rich.panel import Panel
        from rich.align import Align

        header_text = Text("AI Dungeon Master", style="bold magenta", justify="center")
        subtitle = Text("An interactive AI-powered storytelling experience", style="cyan", justify="center")

        panel = Panel(
            Align.center(header_text) + "\n\n" + Align.center(subtitle),
            title="[bold blue]Welcome to Your Adventure[/bold blue]",
            border_style="blue"
        )

        self.console.print(panel)

    async def initialize_components(self):
        """Initialize all game components"""
        with self.console.status("[bold green]Initializing AI Dungeon Master...") as status:
            try:
                # Initialize Gemini
                status.update("[bold yellow]Connecting to Gemini...")
                self.llm = ChatGoogleGenerativeAI(
                    google_api_key=self.config.GEMINI_API_KEY,
                    model=self.config.GEMINI_MODEL,
                    temperature=0.7
                )

                # Initialize components
                status.update("[bold yellow]Setting up world builder...")
                self.world_builder = WorldBuilder(self.llm)

                status.update("[bold yellow]Setting up NPC manager...")
                self.npc_manager = NPCManager(self.llm)

                if AUDIO_AVAILABLE:
                    status.update("[bold yellow]Setting up audio handler...")
                    self.audio_handler = AudioHandler()
                else:
                    status.update("[bold yellow]Skipping audio handler (not available)...")

                status.update("[bold green]All systems ready!")
                await asyncio.sleep(1)

            except Exception as e:
                self.console.print(f"[bold red]Error initializing components: {e}[/bold red]")
                raise

    async def setup_game(self):
        """Set up the initial game state"""
        self.console.print("\n[bold cyan]Game Setup[/bold cyan]")

        # Get player character info
        name = Prompt.ask("What is your character's name?")
        concept = Prompt.ask("Describe your character concept")

        self.game_state["player_character"] = {
            "name": name,
            "concept": concept,
            "level": 1,
            "hp": 10,
            "race": "human",
            "class": "adventurer"
        }

        # Voice setup
        voice_choice = Prompt.ask("Enable voice interaction?", choices=["y", "n"], default="n")
        self.game_state["voice_enabled"] = voice_choice.lower() == "y" and AUDIO_AVAILABLE

        if self.game_state["voice_enabled"]:
            self.console.print("[yellow]Voice interaction enabled. Testing audio...[/yellow]")
            if not self.audio_handler.test_audio_setup():
                self.console.print("[red]Audio setup failed. Continuing with text-only mode.[/red]")
                self.game_state["voice_enabled"] = False
        elif not AUDIO_AVAILABLE:
            self.console.print("[yellow]Voice interaction unavailable - audio dependencies missing.[/yellow]")

        # Generate world
        self.console.print("\n[bold green]Generating your world...[/bold green]")
        self.game_state["world"] = await self.world_builder.generate_world()

        # Set starting location
        self.game_state["current_location"] = self.game_state["world"]["starting_location"]

        # Welcome message
        if self.game_state["voice_enabled"]:
            await self.audio_handler.text_to_speech("Welcome to your adventure!")

    def show_status(self):
        """Display current game status"""
        player = self.game_state["player_character"]
        world = self.game_state["world"]

        # Create status table
        status_table = Table(title=f"Character: {player['name']}")
        status_table.add_column("Attribute", style="cyan")
        status_table.add_column("Value", style="white")

        status_table.add_row("Level", str(player["level"]))
        status_table.add_row("HP", str(player["hp"]))
        status_table.add_row("Race", player["race"])
        status_table.add_row("Class", player["class"])
        status_table.add_row("Location", self.game_state["current_location"])
        status_table.add_row("Voice Mode", "Enabled" if self.game_state["voice_enabled"] else "Disabled")

        # World info
        world_panel = Panel(
            f"[bold]{world['world_name']}[/bold]\n"
            f"Era: {world['current_era']}\n"
            f"Tone: {world['tone']}\n\n"
            f"Current Location: {self.game_state['current_location']}",
            title="World Status",
            border_style="blue"
        )

        self.console.print(Columns([status_table, world_panel]))

    async def process_input(self, user_input: str) -> str:
        """Process user input and generate AI response"""
        import asyncio
        from asyncio.exceptions import TimeoutError

        # This is a simplified version - in a full implementation,
        # this would integrate with all the components
        prompt = f"""You are an AI Dungeon Master for a D&D-style RPG.

        World: {self.game_state['world']['world_name']}
        Player Character: {self.game_state['player_character']['name']} - {self.game_state['player_character']['concept']}
        Current Location: {self.game_state['current_location']}

        Player says: {user_input}

        Respond as the Dungeon Master, describing what happens next in an engaging,
        narrative style. Include sensory details, NPC interactions, and adventure hooks.
        Keep the story immersive and maintain D&D conventions."""

        max_retries = 3
        retry_delay = 4  # seconds
        for attempt in range(max_retries):
            try:
                response = await asyncio.wait_for(self.llm.ainvoke(prompt), timeout=20)
                return response.content
            except TimeoutError:
                self.console.print(f"[yellow]Timeout waiting for AI response, retrying ({attempt+1}/{max_retries})...[/yellow]")
                await asyncio.sleep(retry_delay)
            except Exception as e:
                self.console.print(f"[red]Error during AI response: {e}[/red]")
                break
        return "The AI Dungeon Master is currently unavailable. Please try again later."

    async def game_loop(self):
        """Main game loop"""
        self.show_status()

        commands = {
            "help": "Show available commands",
            "status": "Show character and world status",
            "inventory": "Check inventory",
            "quit": "Exit the game"
        }

        self.console.print("\n[bold green]Available Commands:[/bold green]")
        for cmd, desc in commands.items():
            self.console.print(f"  [cyan]{cmd}[/cyan] - {desc}")

        while True:
            try:
                # Get user input
                if self.game_state["voice_enabled"]:
                    self.console.print("[yellow]Listening... (or type 'text' to switch to text mode)[/yellow]")
                    user_input = await self.audio_handler.speech_to_text(timeout=10)

                    if not user_input:
                        user_input = Prompt.ask("Your action")
                else:
                    user_input = Prompt.ask("\n[bold cyan]Your action[/bold cyan]")

                # Handle commands
                if user_input.lower() in commands:
                    if user_input.lower() == "quit":
                        break
                    elif user_input.lower() == "status":
                        self.show_status()
                        continue
                    elif user_input.lower() == "help":
                        self.console.print("\n[bold green]Available Commands:[/bold green]")
                        for cmd, desc in commands.items():
                            self.console.print(f"  [cyan]{cmd}[/cyan] - {desc}")
                        continue
                    elif user_input.lower() == "inventory":
                        self.console.print("[yellow]Inventory: (empty)[/yellow]")
                        continue

                # Process game input
                with self.console.status("[bold green]The AI Dungeon Master is thinking...") as status:
                    response = await self.process_input(user_input)

                # Display response
                self.console.print(f"\n[bold magenta]DM:[/bold magenta] {response}")

                # Speak response if voice is enabled
                if self.game_state["voice_enabled"]:
                    await self.audio_handler.text_to_speech(response)

            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Game interrupted. Type 'quit' to exit.[/bold yellow]")
            except Exception as e:
                self.console.print(f"[bold red]Error: {e}[/bold red]")

    async def run(self):
        """Run the AI Dungeon Master"""
        try:
            self.print_header()
            await self.initialize_components()
            await self.setup_game()
            await self.game_loop()

        except Exception as e:
            self.console.print(f"[bold red]Fatal error: {e}[/bold red]")
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            self.console.print("\n[bold cyan]Thank you for playing AI Dungeon Master![/bold cyan]")
            if self.game_state["voice_enabled"]:
                await self.audio_handler.text_to_speech("Thank you for playing! Farewell, adventurer!")

app = FastAPI()

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    index_path = os.path.join("frontend", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

game_instance = None

@app.get("/")
async def root():
    return {"message": "AI Dungeon Master API"}

@app.post("/start")
async def start_game(data: dict):
    global game_instance
    game_instance = AIDungeonMaster()
    await game_instance.initialize_components()
    game_instance.game_state["player_character"] = {
        "name": data.get("name", "Adventurer"),
        "concept": data.get("concept", "A brave hero"),
        "level": 1,
        "hp": 10,
        "race": "human",
        "class": "adventurer"
    }
    game_instance.game_state["voice_enabled"] = False
    game_instance.game_state["world"] = await game_instance.world_builder.generate_world()
    game_instance.game_state["current_location"] = game_instance.game_state["world"]["starting_location"]
    return {"message": "Game started", "game_state": game_instance.game_state}

@app.get("/status")
async def get_status():
    if not game_instance:
        return {"error": "Game not started"}
    return {"game_state": game_instance.game_state}

@app.post("/input")
async def process_input_endpoint(data: dict):
    if not game_instance:
        return {"error": "Game not started"}
    user_input = data.get("input", "")
    response = await game_instance.process_input(user_input)
    audio_path = ""
    if game_instance.audio_handler and game_instance.game_state.get("voice_enabled", False):
        audio_path = await game_instance.audio_handler.text_to_speech(response)
        # Convert to URL path relative to static folder
        if audio_path.startswith("static/"):
            audio_path = "/" + audio_path.replace("\\", "/")
    return {"response": response, "audio": audio_path}

async def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()

        # Start the game
        game = AIDungeonMaster()
        await game.run()

    except ValueError as e:
        console = Console()
        console.print(f"[bold red]Configuration Error: {e}[/bold red]")
        console.print("\nPlease make sure you have a .env file with your Gemini API key:")
        console.print("  GEMINI_API_KEY=your_api_key_here")
        console.print("  GEMINI_MODEL=gemini-pro (optional)")
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold yellow]Game terminated by user.[/bold yellow]")
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
