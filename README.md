# Professor Fighting Game 🥋

A vintage arcade-style fighting game featuring four unique professor characters, each with their own special abilities and fighting styles!

## 🎮 Characters

### Professor Khalid - "The Taekwondo Master"
- **Stats:** Health: 110 | Speed: 6 | Jump: -19
- **Special Move:** Spinning Kick - Multi-hit spinning attack that moves forward
- **Fighting Style:** Balanced, martial arts focused

### Professor Eduardo - "The Pizza Master"
- **Stats:** Health: 95 | Speed: 5 | Jump: -16
- **Special Move:** Pizza Throw - Launches 3 pizza slices in rapid succession
- **Fighting Style:** Projectile-based, ranged attacks

### Professor Hasan - "The Pyromancer"
- **Stats:** Health: 100 | Speed: 5 | Jump: -18
- **Special Move:** Fireball - Fast sine-wave projectile
- **Fighting Style:** Magic-based, unpredictable projectiles

### Professor Hammoud - "The Tech Wizard"
- **Stats:** Health: 85 | Speed: 7 | Jump: -20
- **Special Move:** Circuit Board - Slow but homing projectile
- **Fighting Style:** Tech-based, strategic

## 🎮 Controls

### Keyboard Controls

#### Player 1
- **Movement:** W/A/S/D
- **Light Punch:** J
- **Heavy Punch:** K
- **Light Kick:** L
- **Heavy Kick:** I
- **Special Move:** U
- **Dash:** Left Shift
- **Block:** Hold S (Down)
- **Parry:** O

#### Player 2
- **Movement:** Arrow Keys
- **Light Punch:** Numpad 1
- **Heavy Punch:** Numpad 2
- **Light Kick:** Numpad 3
- **Heavy Kick:** Numpad 4
- **Special Move:** Numpad 0
- **Dash:** Right Shift
- **Block:** Hold Down Arrow
- **Parry:** Numpad 5

### Arcade Box Controls (CMU Arcade Machine)

| Action | Button |
|--------|--------|
| Movement | Joystick |
| Light Punch | B (Button 0) |
| Heavy Punch | A (Button 1) |
| Light Kick | X (Button 2) |
| Heavy Kick | Y (Button 3) |
| Special Move | Insert (Button 4) |
| Dash | Select (Button 8) |
| Parry | Start (Button 9) |
| **EXIT/RESET** | **P1 (Button 5)** |

**Note:** The P1 button (Button 5) will immediately exit the game. This is the reset button for the arcade box.

## ⚡ Combat Mechanics

### Attack Frame Data
- **Light Attacks:** Fast recovery, can move almost immediately
- **Heavy Attacks:** Slower recovery, more damage
- **Special Moves:** 2000ms cooldown, unique per character

### Defense System
- **Blocking:** Hold down to block attacks. Reduces damage by 75% and knockback by 50%
- **Parry:** Press parry button for a 6-frame window. Successfully parrying:
  - Negates all damage
  - Reflects projectiles back at the attacker
  - Triggers special visual effect (yellow particles)
  - Has a 30-frame cooldown between uses

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


## 🎓 Credits

Created for CMU-Q Arena Fighting Game Project
Version 1.0 - 2026

---

**Enjoy the fight!** 🥊🔥
