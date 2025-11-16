# 🎲 AI Dungeon Master for Tabletop RPGs

<div align="center">

<p align="left">

  <img src="https://img.shields.io/badge/Version-1.0.0-FF00FF?style=for-the-badge&logo=semanticrelease&logoColor=FF00FF&labelColor=0D0D0D" />
  <img src="https://img.shields.io/badge/Python-3.8%2B-39FF14?style=for-the-badge&logo=python&logoColor=39FF14&labelColor=0D0D0D" />
  <img src="https://img.shields.io/badge/License-MIT-00FFFF?style=for-the-badge&logo=open-source-initiative&logoColor=00FFFF&labelColor=0D0D0D" />

</p>

*An interactive AI-powered Dungeon Master that dynamically generates storylines and NPC dialogues for games like Dungeons & Dragons using LangChain, Gemini, and Text-to-Speech technology.*

[Features](#features) • [Technical Stack](#technical-stack) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Configuration](#configuration)

</div>

## 🌟 Features

<div align="left">

- 🎭 **Dynamic Story Generation**: Creates immersive, adaptive storylines based on player choices
- 🗣️ **Voice Interaction**: Real-time speech-to-text and text-to-speech for hands-free gameplay
- 👥 **Intelligent NPCs**: AI-powered NPCs with distinct personalities and memory
- 🏰 **World Building**: Procedurally generated fantasy worlds with rich lore
- 📚 **Adaptive Narrative**: Stories that evolve based on player decisions
- 🎯 **D&D 5e Compatible**: Designed for Dungeons & Dragons 5th Edition

</div>

## 🔧 Technical Stack

<div class="tech-stack">

### Core Technologies
```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│     LangChain      │  │       Gemini        │  │      Python 3.8+    │
│  AI Orchestration  │  │    Language Model   │  │   Core Runtime      │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

### Audio Processing
```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│        TTS         │  │  SpeechRecognition  │  │       PyDub        │
│  Text-to-Speech    │  │  Voice Recognition  │  │   Audio Processing  │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

### Backend Framework
```
┌─────────────────────┐  ┌─────────────────────┐
│      FastAPI       │  │      Uvicorn       │
│    API Server      │  │   ASGI Server      │
└─────────────────────┘  └─────────────────────┘
```

### Development Tools
```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   python-dotenv    │  │      colorama      │  │        rich         │
│  Config Management │  │  Terminal Colors   │  │  Terminal UI/Output │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

</div>

## 📥 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ai-dungeon-master
```

2. **Set up Python environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```
**Important:** Ensure your `.env` file contains a valid Gemini API key to avoid API_KEY_INVALID errors.

5. **Run the application:**
```bash
python main.py
```

## 🎮 Usage

### Starting a New Game

1. Launch the application:
```bash
python main.py
```
2. Follow the interactive setup:
   - Enter your character's name
   - Describe your character concept
   - Choose voice interaction preferences
   - Begin your adventure!

### Game Commands

| Command | Description |
|---------|-------------|
| `help` | Display available commands |
| `status` | View character status |
| `inventory` | Check your items |
| `party` | View party members |
| `quit` | Exit the game |

### Voice Commands
When voice interaction is enabled:
- 🗣️ Speak naturally to interact with the game
- 🔊 Receive AI responses through synthesized speech
- ⌨️ Text input available as fallback

## 🏗️ Architecture

### Core Components
```
┌─────────────────────┐
│  ai_dungeon_master  │
│    Main Engine     │
└─────────────────────┘
         ↓
┌─────────────┬─────────────┬─────────────┐
│  audio      │   world     │    npc      │
│  handler    │  builder    │  manager    │
└─────────────┴─────────────┴─────────────┘
         ↓
┌─────────────────────┐
│      config        │
│  Configuration     │
└─────────────────────┘
```

### Key Classes

- `AIDungeonMaster`: Core game controller
- `AudioHandler`: Voice interaction management
- `WorldBuilder`: Procedural world generation
- `NPCManager`: NPC creation and state management
- `NPC`: Individual NPC behavior and memory

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">

Made with ❤️ by aad1tyaaaaa

</div>

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






