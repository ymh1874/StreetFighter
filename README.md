# Professor Fighting Game 🥋

A vintage arcade-style fighting game featuring four unique professor characters, each with their own special abilities and fighting styles!

## 🎮 Characters

### Professor Khalid - "The Taekwondo Master"
- **Appearance:** Orange taekwondo gi, slicked-back black hair, athletic build
- **Stats:** Health: 110 | Speed: 6 | Jump: -19
- **Special Move:** Spinning Kick - Multi-hit spinning attack that moves forward
- **Fighting Style:** Balanced, martial arts focused

### Professor Eduardo - "The Pizza Master"
- **Appearance:** Red chef's apron, white chef hat, jolly build
- **Stats:** Health: 95 | Speed: 5 | Jump: -16
- **Special Move:** Pizza Throw - Launches 3 pizza slices in rapid succession
- **Fighting Style:** Projectile-based, ranged attacks

### Professor Hasan - "The Pyromancer"
- **Appearance:** Yellow/orange wizard robes, completely bald, mystical
- **Stats:** Health: 100 | Speed: 5 | Jump: -18
- **Special Move:** Fireball - Fast sine-wave projectile
- **Fighting Style:** Magic-based, unpredictable projectiles

### Professor Hammoud - "The Tech Wizard"
- **Appearance:** Green lab coat, modern glasses, buzz cut
- **Stats:** Health: 85 | Speed: 7 | Jump: -20
- **Special Move:** Circuit Board - Slow but homing projectile
- **Fighting Style:** Tech-based, strategic

## 🎮 Controls

### Player 1
- **Movement:** W/A/S/D
- **Light Punch:** J
- **Heavy Punch:** K
- **Light Kick:** L
- **Heavy Kick:** I
- **Special Move:** U
- **Dash:** Left Shift

### Player 2
- **Movement:** Arrow Keys
- **Light Punch:** Numpad 1
- **Heavy Punch:** Numpad 2
- **Light Kick:** Numpad 3
- **Heavy Kick:** Numpad 4
- **Special Move:** Numpad 0
- **Dash:** Right Shift

## ⚡ Combat Mechanics

### Attack Frame Data
- **Light Attacks:** Fast recovery, can move almost immediately
- **Heavy Attacks:** Slower recovery, more damage
- **Special Moves:** 2000ms cooldown, unique per character

### Combo System
- Maximum combo: 5 hits
- Damage scaling on hits 4-5 (80% damage)
- Combos automatically break after 5 hits

### Projectile Balance
| Projectile | Speed | Damage | Special Property |
|-----------|-------|--------|------------------|
| Hasan's Fireball | Fast (8px/f) | 15 | Sine wave motion |
| Eduardo's Pizza | Medium (5px/f) | 6 per slice | 3 projectiles |
| Hammoud's Circuit | Slow (4px/f) | 20 | Homing |

## 🎨 Features

- **Hand-drawn characters** using pygame primitives (no sprites)
- **Comic book style hit effects** ("POW!", "BOOM!", "WHAM!")
- **Screen shake** on heavy hits
- **Segmented health bars** with 10 chunks
- **Special move cooldowns** (2000ms)
- **Unique victory poses** for each character
- **Smooth 60 FPS gameplay**
- **Vintage arcade aesthetic**

## 🚀 How to Run

```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

## 🎯 Game Modes

1. **Character Select:** Choose your fighter from 4 unique professors
2. **Fight:** Engage in intense 1v1 combat
3. **Victory:** Unique victory poses for each character

## 📁 Project Structure

```
StreetFighter/
├── main.py          # Entry point
├── game.py          # Main game loop and state management
├── config.py        # Character stats and constants
├── entities.py      # Fighter, Projectile, and Particle classes
├── drawing.py       # Character drawing functions (pygame primitives)
├── combat.py        # Combat system, frame data, combos
├── ui_components.py # UI elements and text rendering
└── README.md        # This file
```

## 🛠️ Technical Details

- **Engine:** Pygame
- **Resolution:** 800x600 (scaled to fullscreen)
- **FPS:** 60
- **Art Style:** Hand-drawn using pygame drawing functions
- **Combat:** Frame-based with precise timing

## 🎓 Credits

Created for CMU-Q Arena Fighting Game Project
Version 1.0 - 2026

---

**Enjoy the fight!** 🥊🔥