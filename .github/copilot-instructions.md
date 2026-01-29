# CMUQ Arena - AI Coding Instructions

## Project Overview
A 2D arcade-style fighting game built with **pygame** for the CMU-Q arcade machine. Features 4 professor characters with unique special moves, frame-based combat, combo system, and joystick/arcade box support.

## Architecture

### Core Module Responsibilities
- **main.py** → Entry point, instantiates `Game` and runs game loop
- **game.py** → Central game class managing states (`MAIN_MENU`, `CHARACTER_SELECT`, `FIGHT`, `GAME_OVER`), input routing, and screen transitions
- **entities.py** → `Fighter` class (player logic), `Projectile` subclasses (PizzaSlice, SineWaveFireball, HomingCircuitBoard), visual effects
- **combat.py** → `CombatSystem` (combo tracking, combo strings), `FrameData` (attack timing), `AttackBuffer` (input buffering)
- **config.py** → All constants, colors, character stats, control mappings, frame data definitions
- **drawing.py** → Procedural character rendering with pygame primitives (no sprite images)
- **joystick.py** → Arcade box/gamepad abstraction with callback-based input handling
- **ui_components.py** → `Button`, `VintageTextRenderer`, `ScanlineEffect`, `GradientBackground` for UI
- **pygame_compat.py** → Cross-platform pygame import compatibility layer (arcade box + standard pygame)

### Data Flow
1. Input → `joystick.py` callbacks or keyboard events in `game.py`
2. `Fighter.update()` processes input using controls from `config.py`
3. Combat resolved via `combat.py` frame data and hitbox detection
4. Rendering: `game.py` calls `drawing.py` functions per character

## Key Patterns

### Pygame Compatibility (IMPORTANT for Arcade Machine)
All files use `pygame_compat.py` instead of direct `import pygame`:
```python
from pygame_compat import pygame
```
This ensures compatibility with both standard pygame and CMU arcade box's bundled pygame.

### Character Configuration (config.py)
Characters are defined in `CHARACTERS` list with stats. To add a character:
```python
{'name': 'NEWCHAR', 'color': COLOR, 'skin': SKIN_COLOR, 
 'speed': 5, 'jump': -18, 'health': 100, 'dmg_mult': 1.0,
 'desc': 'DESCRIPTION', 'special': 'special_move_name'}
```

### Frame Data System
Attacks use frame data in `config.FRAME_DATA`:
- `startup`: frames before hitbox activates
- `active`: frames hitbox is active
- `recovery`: frames before next action
- `can_move_early`: allows movement cancel

### Combo System (combat.py)
- `CombatSystem.record_hit()` tracks combos with timing windows
- Combo announcements at 3, 5, 7+ hits
- Combo strings defined in `COMBO_STRINGS` dict for bonus damage
- Counter attack window grants 50% bonus damage after successful parry

### Drawing Characters
Each character has a dedicated draw function in `drawing.py`:
```python
drawing.draw_khalid(surface, x, y, facing_right, animation_state='punch', frame=0)
```

### UI Components (ui_components.py)
- `VintageTextRenderer`: Cross-platform font rendering with `render()` and `render_outlined()` methods
- `GradientBackground`: Vertical/radial gradients for menus
- `draw_panel()`: Styled panels with shadows

### Joystick/Arcade Box Integration
- `joystick.init()` called once at startup
- Callbacks set via `joystick.set_callbacks(on_press=..., on_release=..., on_hold=..., on_digital_axis=...)`
- Button mappings in `config.py` (`ARCADE_P1_BUTTONS`, `ARCADE_P2_BUTTONS`)
- Button 5 (P1/RESET) immediately exits game

## Development

### Running the Game
```bash
pip install pygame
python main.py
```

### Testing Input
The game runs fullscreen. Use keyboard controls (WASD + JKLI for P1, Arrows + Numpad for P2) or connect arcade box/gamepad.

### Adding Special Moves
1. Create projectile class in `entities.py` (extend `Projectile`)
2. Add draw function in `drawing.py`
3. Register special name in character config (`'special': 'move_name'`)
4. Handle special in `Fighter.execute_special_move()` method

### Adding Combo Strings
Define in `combat.py` `COMBO_STRINGS` dict:
```python
'character_name': {
    'combo_id': {
        'inputs': ['light_punch', 'light_punch', 'heavy_kick'],
        'bonus_damage': 0.3,
        'name': 'COMBO NAME'
    }
}
```

## Conventions
- All positions/sizes use internal resolution (800×600), auto-scaled to fullscreen
- Colors defined as RGB tuples in `config.py`
- Frame timing at 60 FPS (use `c.FPS`)
- Character stats balanced around base health=100, speed=5, jump=-18
- Use `pygame_compat` for all pygame imports (arcade machine compatibility)
