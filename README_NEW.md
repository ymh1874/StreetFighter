# CMUQ Arena - Vintage Arcade Fighting Game

A professionally crafted 2D fighting game with authentic vintage arcade aesthetics, featuring a complete menu system, character selection, and intense 1v1 combat.

## ✨ Features

### 🎮 Complete Menu System
- **Main Menu**: START, CONTROLS, ABOUT buttons - fully keyboard and mouse interactive
- **Controls Screen**: Displays all player controls with vintage styling
- **About Screen**: Game information and credits
- **Character Selection**: Choose from 4 unique fighters
- **Game Over**: Winner announcement with rematch option

### 🎨 Vintage Arcade Aesthetic
- Authentic CRT scanline effects
- Retro arcade cabinet frame decorations
- Classic color palette (Orange, Yellow, Black)
- Pixel-perfect alignment and centering
- Professional UI components with shadows and borders

### 👾 4 Unique Characters
1. **PHOENIX** - Balanced Warrior (Red)
   - HP: 100, Speed: 5, Damage: 1.0x
   
2. **TITAN** - Heavy Crusher (Green)
   - HP: 140, Speed: 3, Damage: 1.3x
   
3. **LIGHTNING** - Speed Demon (Yellow)
   - HP: 80, Speed: 7, Damage: 0.8x
   
4. **SHADOW** - Dark Master (Purple)
   - HP: 110, Speed: 4, Damage: 1.1x

### 🕹️ Controls

#### Player 1
- **Movement**: W/A/S/D
- **Light Attack**: J
- **Heavy Attack**: K
- **Kick**: L
- **Special**: I

#### Player 2
- **Movement**: Arrow Keys
- **Light Attack**: Numpad 1
- **Heavy Attack**: Numpad 2
- **Kick**: Numpad 3
- **Special**: Numpad 0

#### Global
- **ESC**: Back/Quit
- **Enter**: Confirm/Select
- **Mouse**: Click buttons in menus

## 🚀 How to Run

### Prerequisites
```bash
# Make sure you have Python 3.7+ installed
python --version

# Install pygame and Pillow
pip install pygame Pillow
```

### Running the Game
```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Run the game
python main.py
```

## 📁 Project Structure

```
StreetFighter/
├── main.py                  # Entry point
├── game.py                  # Main game class with all states
├── ui_components.py         # Reusable UI components (Button, Text, etc.)
├── entities.py              # Fighter and Particle classes
├── config.py                # Game configuration and constants
├── sprites.py               # Sprite and animation management
├── test_alignment.py        # Test suite for UI alignment
├── game_old_backup.py       # Backup of previous version
└── README.md                # This file
```

## 🏗️ Architecture

### Clean Code Principles
- **Separation of Concerns**: UI, game logic, and entities are separate
- **Reusable Components**: Button, text renderer, visual effects
- **Clear State Management**: 6 distinct game states with clean transitions
- **Extensive Documentation**: Every class and method is documented
- **Professional Comments**: Easy to read and maintain

### Game States
1. **MAIN_MENU** - Entry point with menu options
2. **CONTROLS** - Display game controls
3. **ABOUT** - Show game information
4. **CHARACTER_SELECT** - Choose fighters
5. **FIGHT** - Main combat gameplay
6. **GAME_OVER** - Display winner and allow rematch

### UI Components (`ui_components.py`)
- **Button**: Interactive button with hover effects
- **VintageTextRenderer**: Text rendering with PIL/Pillow fallback
- **ArcadeFrame**: Decorative arcade cabinet frame
- **ScanlineEffect**: CRT scanline overlay

## 🎯 Design Decisions

### Why This Structure?
1. **Maintainability**: Clean separation makes it easy to modify
2. **Scalability**: Easy to add new characters, moves, or screens
3. **Readability**: Comprehensive comments and documentation
4. **Testability**: Separate test suite to verify alignment

### Vintage Arcade Look
- All text perfectly centered using mathematical calculations
- Consistent spacing and alignment throughout
- Shadow effects for depth
- Double borders on buttons for authentic arcade feel
- Orange/Yellow color scheme reminiscent of classic arcade games

## 🧪 Testing

Run the test suite to verify all UI elements are properly aligned:

```bash
source venv/bin/activate
python test_alignment.py
```

The test suite checks:
- Button alignment and centering
- Text rendering in all sizes
- Character grid symmetry
- Health bar positioning
- Visual effects initialization
- Screen centering calculations

## 🐛 Troubleshooting

### "No module named 'pygame'"
```bash
# Activate your virtual environment
source venv/bin/activate

# Install pygame
pip install pygame
```

### "No module named 'PIL'"
```bash
# Install Pillow for better text rendering
pip install Pillow

# The game will work without it (uses fallback rendering)
```

### Game runs but text looks blocky
- Install Pillow: `pip install Pillow`
- The game uses PIL/Pillow for smooth text rendering
- Without it, falls back to simple block rendering

## 📝 Version History

### Version 1.0 (January 2026)
- Complete rewrite with professional architecture
- Vintage arcade aesthetic implementation
- Full menu system (Main, Controls, About)
- Mouse and keyboard support
- Perfect UI alignment and centering
- Comprehensive documentation
- Test suite for verification

## 👨‍💻 Development Notes

### For Future Developers

The code is structured to be easily maintainable:

1. **Adding a new menu**: Create `_init_new_menu()`, `_update_new_menu()`, `_draw_new_menu()` methods
2. **Adding a character**: Add to `CHARACTERS` list in `config.py`
3. **Modifying UI**: All visual constants in `ui_components.py`
4. **Changing controls**: Modify control dictionaries in `_start_fight()`

### Code Style
- All methods have docstrings
- Clear variable names
- Consistent indentation (4 spaces)
- Grouped by functionality with section headers
- Type hints in docstrings

## 🎮 Game Flow

```
MAIN_MENU
   ├─→ START ────→ CHARACTER_SELECT ────→ FIGHT ────→ GAME_OVER
   ├─→ CONTROLS ──→ (Back to MAIN_MENU)
   └─→ ABOUT ─────→ (Back to MAIN_MENU)
```

## 🏆 Credits

- **Game Design**: Senior Game Developer
- **Architecture**: Professional clean code principles
- **Art Style**: Vintage arcade aesthetic
- **Year**: 2026

---

**Enjoy the game! Press ESC to quit, Enter to start, and get ready for epic battles!** 🥊
