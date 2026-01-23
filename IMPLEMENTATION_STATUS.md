# CMUQ Arena - Professor Fighting Game
## Complete Implementation Guide

### ✅ COMPLETED SO FAR:

1. **Config Updated** (`config.py`)
   - 4 Professors defined: Khalid, Eduardo, Hasan, Hammoud
   - All stats, combos, and special move types configured
   - New combat constants added (dash, parry, combo system)
   
2. **Partial Entities** (`entities_new.py`)
   - Particle system with visual effects
   - Complete Projectile base class with parabolic physics
   - 3 Projectile types: PizzaSlice, Fireball, CircuitBoard
   - Full StickFigure animation class (15 states)
   - Fighter class started with new attributes

### 🚧 IN PROGRESS:

Need to complete `entities_new.py` with Fighter class methods:

#### Required Fighter Methods:
1. **Movement Methods:**
   - `dash()` - Execute dash with cooldown and distance
   - `block()` - Enter blocking state with damage reduction
   - `crouch()` - Lower hitbox
   - `air_dash()` - One-time aerial dash
   
2. **Combat Methods:**
   - `parry(attacker)` - Frame-perfect parry system
   - `shoot_projectile(aim_direction)` - Fire character-specific projectile
   - `apply_knockdown()` - Enter knockdown state
   - `get_up()` - Exit knockdown with invincibility
   
3. **Combo System Methods:**
   - `add_to_combo_buffer(input)` - Track recent inputs
   - `detect_combo()` - Match input sequences to combos
   - `execute_combo(combo_data)` - Perform combo with bonus damage
   - `reset_combo()` - Clear combo state
   
4. **Super Meter Methods:**
   - `gain_super_meter(amount)` - Increase meter
   - `spend_super_meter(amount)` - Decrease meter
   - `can_use_super()` - Check if meter is full
   
5. **Enhanced Existing Methods:**
   - `move()` - Add dash, block, crouch logic
   - `attack()` - Add parry check, combo detection
   - `update()` - Add knockdown, invincibility, dash cooldown
   - `draw()` - Use stick figure animations

### 📋 TODO - PHASE BY PHASE:

#### **Phase 1: Complete Fighter Class** (2-3 hours)
- [ ] Finish all Fighter methods
- [ ] Test movement (dash, block, crouch)
- [ ] Test basic attacks with new system

#### **Phase 2: Projectile Integration** (1-2 hours)
- [ ] Update game.py to manage projectile list
- [ ] Add projectile collision detection
- [ ] Test all 3 projectile types
- [ ] Add aiming system (up/neutral/down)

#### **Phase 3: Combo System** (2 hours)
- [ ] Implement input buffering
- [ ] Add combo detection logic
- [ ] Display combo counter on screen
- [ ] Test all character combos

#### **Phase 4: Advanced Combat** (2 hours)
- [ ] Implement parry system with 6-frame window
- [ ] Add knockdown mechanics
- [ ] Test super meter gain/usage
- [ ] Add damage scaling for long combos

#### **Phase 5: Visual Effects** (1-2 hours)
- [ ] Screen shake on heavy hits
- [ ] Slow motion (KO and parry)
- [ ] Victory/defeat animations
- [ ] Particle effects for projectiles

#### **Phase 6: Round System** (1 hour)
- [ ] Best of 3 rounds tracking
- [ ] Round countdown and FIGHT! text
- [ ] Victory screen with stats
- [ ] Round win indicators

#### **Phase 7: Testing & Polish** (2-3 hours)
- [ ] Write automated tests
- [ ] Balance character stats
- [ ] Fix bugs
- [ ] Add debug overlays (F1, F2, F3)

### 📊 ESTIMATED TOTAL TIME: 12-15 hours

### 🎯 IMMEDIATE NEXT STEPS:

1. Complete `entities_new.py` Fighter class
2. Replace old `entities.py` with new version
3. Update `game.py` to handle projectiles
4. Test basic functionality

### 📝 NOTES:

- Game is currently running with new professor config
- Stick figure animations are complete and ready
- Projectile classes are fully implemented
- Need to connect all systems together

### 🔧 TESTING STRATEGY:

**Unit Tests Needed:**
- `test_parry_timing()` - Verify 6-frame window
- `test_combo_detection()` - Input buffer matching
- `test_projectile_physics()` - Parabolic trajectory
- `test_dash_cooldown()` - 800ms timing
- `test_knockdown_duration()` - 60 frames
- `test_super_meter_gain()` - Correct percentages

**Integration Tests:**
- Round system flow
- Projectile vs fighter collision
- Combo into super move
- Parry → counter attack

Would you like me to:
A) Continue completing entities.py with all Fighter methods?
B) Create the test suite first?
C) Update game.py for projectile support?
D) Something else?

Let me know and I'll continue with laser focus! 🎮
