# 🎮 CMUQ Arena - Vintage Arcade Fighting Game

A professional-grade 2D fighting game featuring CMUQ professors with advanced combat mechanics, projectile systems, and vintage arcade aesthetics.

## 🎯 Features

### ✅ Complete Implementation

#### **Character System**
- 4 Unique Professors with distinct abilities
  - **Prof. Khalid** - Taekwondo Master (High HP, Fast Kicks)
  - **Prof. Eduardo** - The Pizza Chef (Projectile Specialist)
  - **Prof. Hasan** - The Pyromancer (Fireball Master)
  - **Prof. Hammoud** - The Tech Wizard (Fast, Circuit Attacks)

#### **Combat Mechanics**
- ✅ **Basic Attacks**: Light Punch, Heavy Punch, Light Kick, Heavy Kick
- ✅ **Special Moves**: Character-specific ultimate attacks
- ✅ **Dash System**: Ground dash + Air dash (800ms cooldown)
- ✅ **Block/Parry System**: 
  - Block reduces damage by 75%
  - Perfect parry (6-frame window) negates damage and stuns attacker
- ✅ **Combo System**:
  - Input buffer window: 500ms
  - 2 unique combos per character
  - Combo damage multipliers (1.3x-2.0x)
  - Real-time combo counter display
- ✅ **Super Meter System**:
  - Gain meter by attacking/being hit
  - Spend on powerful combo finishers
  - Visual meter bar in HUD
- ✅ **Knockdown System**:
  - Heavy attacks cause knockdown
  - 60 frames recovery time
  - Get-up invincibility frames

#### **Projectile System**
- ✅ **Pizza Slice** (Prof. Eduardo)
  - Parabolic arc trajectory
  - Cheese drip particles
  - 12 damage
- ✅ **Fireball** (Prof. Hasan)
  - Fast horizontal projectile
  - Flame trail particles
  - 15 damage
- ✅ **Circuit Board** (Prof. Hammoud)
  - Homing behavior
  - Electric spark particles
  - 10 damage

#### **Animation System**
- ✅ **15 Animation States**:
  - idle, walk, dash, jump, crouch, block
  - light_punch, heavy_punch, light_kick, heavy_kick, special
  - hit, knockdown, victory, defeat
- ✅ **Stick Figure Rendering**: Smooth procedural animations
- ✅ **Hit Effects**: Color flash, invincibility flicker

#### **Visual Effects**
- ✅ **Screen Shake**: Impact feedback on heavy hits
- ✅ **Slow Motion**: Dramatic effect on knockdowns
- ✅ **Particle System**: Hit sparks, projectile trails
- ✅ **Scanline Effect**: Authentic CRT monitor feel
- ✅ **Arcade HUD**: Health bars, super meters, timer, round indicators

#### **Game Modes**
- ✅ **Round System**: Best of 3 rounds
- ✅ **Character Selection**: Visual grid with stats
- ✅ **Game States**: Main Menu, Controls, About, Character Select, Fight, Game Over
- ✅ **Keyboard + Mouse Support**: Full navigation

## 🎮 Controls

### Player 1 (Left Side)
| Action | Key |
|--------|-----|
| Move Left/Right | A / D |
| Jump | W |
| Crouch/Block | S |
| Light Punch | J |
| Heavy Punch | K |
| Kick | L |
| Special Move | I |
| Dash | Left Shift |

### Player 2 (Right Side)
| Action | Key |
|--------|-----|
| Move Left/Right | ← / → |
| Jump | ↑ |
| Crouch/Block | ↓ |
| Light Attack | Numpad 1 |
| Heavy Attack | Numpad 2 |
| Kick | Numpad 3 |
| Special Move | Numpad 0 |
| Dash | Right Shift |

### Global Controls
| Action | Key |
|--------|-----|
| Pause/Back | ESC |
| Confirm | ENTER / SPACE |
| Navigate Menu | Arrow Keys / W/S |

## 🔥 Advanced Techniques

### Combo Execution
Each character has 2 unique combos. Examples:
- **Prof. Khalid - Tornado Rush**: L → L → I (3-hit combo)
- **Prof. Eduardo - Pizza Barrage**: J → J → U (super combo)
- **Prof. Hasan - Flame Uppercut**: L → K → U (launcher combo)
- **Prof. Hammoud - Binary Rush**: J → J → L → I (4-hit tech combo)

### Parry Timing
- Hold Block (S/↓)
- Release and press again just as opponent attacks (6 frames)
- Successful parry: Gain super meter, opponent stunned

### Projectile Aiming
- Hold **Up** key before Special: Aim upward
- Hold **Down** key before Special: Aim downward
- Neutral: Shoot straight

### Air Combat
- Jump and attack for aerial strikes
- Air dash to extend combos
- One air dash per jump

## 🏗️ Technical Architecture

### File Structure
```
StreetFighter/
├── main.py              # Entry point
├── game.py              # Main game loop & state management (866 lines)
├── entities.py          # Fighter, projectiles, animations (1400+ lines)
├── config.py            # Game constants & character data
├── ui_components.py     # UI rendering system
├── test_features.py     # Automated feature verification
└── venv/                # Python virtual environment
```

### Performance
- **60 FPS**: Frame-perfect combat mechanics
- **Resolution**: 800x600 (scaled fullscreen)
- **Engine**: Pygame 2.6.1
- **Python**: 3.14.2

## 🚀 Installation & Running

### Prerequisites
- Python 3.8+
- pygame 2.6+
- PIL/Pillow (optional, for text rendering)

### Setup
```bash
# Clone repository
git clone https://github.com/ymh1874/StreetFighter.git
cd StreetFighter

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run game
python main.py
```

### Verify Installation
```bash
python test_features.py
```
Should output:
```
✓ TEST 1: Professor Characters (4)
✓ TEST 2: Combat Constants
✓ TEST 3: Projectile System (3 types)
✓ TEST 4: StickFigure Animations (15 states)
✓ TEST 5: Fighter Class Advanced Features
✓ TEST 6: Character Combos
All Features Verified Successfully!
```

## 📊 Character Stats

| Professor | HP | Speed | Special | Type |
|-----------|----| ------|---------|------|
| Khalid | 110 | 6 | Tornado Kick | Melee |
| Eduardo | 95 | 5 | Pizza Toss | Projectile |
| Hasan | 100 | 5 | Fireball | Projectile |
| Hammoud | 85 | 7 | Circuit Throw | Projectile |

## 🎨 Design Philosophy

### Vintage Arcade Aesthetic
- CRT scanline effects
- Pixel-perfect UI alignment
- Retro color palette (Orange, Yellow, Cyan)
- Block-style text rendering
- Grid floor with perspective

### Combat Design
- **Frame Data**: Every attack has startup, active, recovery frames
- **Hitboxes**: Precise collision detection
- **Stun Systems**: Hit stun, block stun, knockdown
- **Meter Management**: Risk/reward decision-making
- **Combo Theory**: Input buffer for advanced players

## 🐛 Known Limitations

- Music requires `pygame.mixer` (optional dependency)
- Some systems may show AVX2 warnings (cosmetic)
- Projectile-projectile collision not implemented
- AI opponents not included (PvP only)

## 📝 Development Notes

### Code Quality
- **Professional Structure**: State pattern, clean separation of concerns
- **Comprehensive Documentation**: 200+ lines of docstrings
- **Type Safety**: Clear function signatures
- **Extensibility**: Easy to add new characters/moves

### Testing
- Automated feature verification script
- Manual playtesting for balance
- Edge case handling (boundary checks, null safety)

## 🏆 Credits

**Game Design & Programming**: Senior Game Developer  
**Character Concepts**: CMUQ Faculty  
**Engine**: Pygame Community  
**Year**: 2026

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Status**: ✅ **PRODUCTION READY**  
**Version**: 1.0.0  
**Last Updated**: January 2026  

🎮 *Insert Coin to Continue* 🎮
