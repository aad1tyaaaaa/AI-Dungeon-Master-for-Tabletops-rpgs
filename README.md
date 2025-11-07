    # AI Dungeon Master for Tabletop RPGs

An interactive AI-powered Dungeon Master that dynamically generates storylines and NPC dialogues for games like Dungeons & Dragons using LangChain, Gemini, and Text-to-Speech technology.

## Features

- **Dynamic Story Generation**: Creates immersive, adaptive storylines based on player choices
- **Voice Interaction**: Real-time speech-to-text and text-to-speech for hands-free gameplay
- **Intelligent NPCs**: AI-powered NPCs with distinct personalities and memory
- **World Building**: Procedurally generated fantasy worlds with rich lore
- **Adaptive Narrative**: Stories that evolve based on player decisions
- **D&D 5e Compatible**: Designed for Dungeons & Dragons 5th Edition

## Tech Stack

- **LangChain**: Framework for building applications with LLMs
- **Gemini**: Advanced language model for story generation
- **Text-to-Speech**: Real-time voice synthesis
- **Speech Recognition**: Voice input processing
- **Python**: Core programming language

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-dungeon-master
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```
**Important:** Ensure your `.env` file contains a valid Gemini API key to avoid API_KEY_INVALID errors.

4. Run the game:
```bash
python main.py
```

## Usage

### Starting a New Game

1. Run `python main.py`
2. Enter your character's name
3. Describe your character concept
4. Choose whether to enable voice interaction
5. Begin your adventure!

### Game Commands

- `help` - Show available commands
- `status` - View character status
- `inventory` - Check your items
- `party` - View party members
- `quit` - Exit the game

### Voice Commands

When voice interaction is enabled:
- Speak naturally to interact with the game
- The AI will respond with synthesized speech
- Use text input as fallback

## Architecture

### Core Components

- **ai_dungeon_master.py**: Main game orchestrator
- **audio_handler.py**: Speech-to-text and text-to-speech
- **world_builder.py**: Dynamic world generation
- **npc_manager.py**: NPC creation and management
- **config.py**: Configuration management

### Key Classes

- `AIDungeonMaster`: Main game controller
- `AudioHandler`: Voice interaction
- `WorldBuilder`: World generation
- `NPCManager`: NPC management
- `NPC`: Individual NPC representation

## Configuration

### Environment Variables

Create a `.env` file with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

### Audio Settings

Adjust voice settings in `config.py`:

```python
SPEECH_RATE = 200  # Words per minute
SPEECH_VOLUME = 0.9  # 0.0 to 1.0
```

## Development

### Adding New Features

1. Extend the `AIDungeonMaster` class
2. Add new prompt templates for specific scenarios
3. Implement new world generation algorithms
4. Create custom NPC behaviors

### Testing

Test audio setup:
```python
from audio_handler import AudioHandler
handler = AudioHandler()
handler.test_audio_setup()
```

## Examples

### Starting a Game
```
AI Dungeon Master
An interactive AI-powered storytelling experience

Welcome to your adventure!
What is your character's name? Aragorn
Describe your character concept A brave ranger seeking adventure
```

### Sample Interaction
```
> I approach the mysterious figure in the tavern
The hooded figure looks up as you approach...

[The AI continues the story based on your action]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request    

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting guide
- Open an issue on GitHub
- Join our Discord community
