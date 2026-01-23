# 🎮 CMUQ Arena - Quick Start Guide

## 🚀 Running the Game (1 Minute)

```bash
cd /home/yousef/repos/StreetFighter
source venv/bin/activate
python main.py
```

## 🎯 Basic Controls (Player 1)

**Movement**: W/A/S/D  
**Attack**: J (Light) / K (Heavy) / L (Kick)  
**Special**: I  
**Dash**: Left Shift  
**Block**: Hold S  

## 🎯 Basic Controls (Player 2)

**Movement**: Arrow Keys  
**Attack**: Numpad 1/2/3  
**Special**: Numpad 0  
**Dash**: Right Shift  
**Block**: Hold Down Arrow  

## 🔥 Try These First

1. **Pick Your Fighter**: Use A/D or Arrow Keys
2. **Press J/Numpad 1**: Confirm selection
3. **Try a Combo**: J → J → L (Player 1)
4. **Block**: Hold S when opponent attacks
5. **Dash**: Shift + Direction for quick movement
6. **Special**: Press I to shoot projectile (Eduardo, Hasan, Hammoud)

## ⚔️ Combat Tips

- **Dash** is on cooldown (800ms) - use wisely
- **Block** reduces damage by 75%
- **Perfect Parry**: Release and re-press block just as attack hits
- **Super Meter**: Fills as you fight, enables powerful combos
- **Knockdown**: Heavy attacks knock opponent down for 60 frames
- **Combos**: Input attacks quickly within 500ms window

## 🏆 Win Condition

**Best of 3 Rounds**  
- Reduce opponent's health to 0
- OR have more health when timer reaches 0

## 📊 Characters at a Glance

| Character | Strength | Play Style |
|-----------|----------|------------|
| **Khalid** | High HP | Tank/Melee |
| **Eduardo** | Projectiles | Zoner |
| **Hasan** | Balanced | All-rounder |
| **Hammoud** | Speed | Rushdown |

## 🎨 What to Expect

✅ Vintage arcade aesthetic with CRT scanlines  
✅ Smooth 60 FPS stick figure animations  
✅ Screen shake on heavy hits  
✅ Particle effects for projectiles and hits  
✅ Real-time combo counter  
✅ Super meter system  
✅ Round-based matches (best of 3)  

## 🐛 Troubleshooting

**"No music file found"**: Normal - music is optional  
**pygame.mixer warnings**: Safe to ignore  
**Game won't start**: Make sure venv is activated  
**Black screen**: Try pressing ESC to exit and restart  

## 🧪 Verify Everything Works

```bash
python test_features.py
```

Should show:
```
✓ TEST 1: Professor Characters (4)
✓ TEST 2: Combat Constants
✓ TEST 3: Projectile System
✓ TEST 4: StickFigure Animations (15 states)
✓ TEST 5: Fighter Class Advanced Features
✓ TEST 6: Character Combos
All Features Verified Successfully!
```

---

**Ready to Fight?** Run `python main.py` and press START! 🎮
