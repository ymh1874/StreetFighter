# CMUQ Arena - Testing Guide

## Quick Start

Run all tests:
```bash
source venv/bin/activate
python test_comprehensive.py
```

Expected output: **354/354 tests passing (100%)**

---

## Test Categories

### 1. Configuration (6 tests)
Tests game settings and constants.

### 2. Character Definitions (64 tests)
Validates all 4 professors:
- PROF. KHALID (Tornado Fighter)
- PROF. EDUARDO (Pizza Master)
- PROF. HASAN (Firestorm Warrior)
- PROF. HAMMOUD (Circuit Breaker)

### 3. Projectile System (30 tests)
Tests all 3 projectile types:
- PizzaSlice
- Fireball
- CircuitBoard

### 4. Animation System (15 tests)
Validates 15 different character animations.

### 5. Fighter Class (164 tests)
Comprehensive fighter testing:
- 41 attributes per character
- 13 methods per character
- All 4 characters instantiated

### 6. Combat Mechanics (9 tests)
Attack system, super meter, combos, knockdowns.

### 7. Movement (4 tests)
Move, dash, block mechanics.

### 8. Particle System (6 tests)
Visual effect particles.

### 9. Game Constants (18 tests)
Timing and balance values.

### 10. Combo System (17 tests)
All 8 combos across 4 characters.

### 11. Projectile Updates (6 tests)
Movement and collision physics.

### 12. Attack Class (9 tests)
Attack data structures.

---

## Manual Game Testing

### Launch Game:
```bash
source venv/bin/activate
python main.py
```

### Game Modes to Test:

**1P vs AI Mode:**
- Select a character
- Press 1 for AI Easy
- Press 2 for AI Medium
- Press 3 for AI Hard
- Fight the AI opponent

**2P Mode:**
- Select characters
- Press SPACE to start
- Player 1: WASD + JKL keys
- Player 2: Arrow keys + UIO keys

**AI vs AI Mode:**
- Select two characters
- Press 4 for AI vs AI
- Watch the AI battle

### Controls to Test:

**Player 1 (WASD):**
- W: Jump
- S: Crouch
- A: Move Left
- D: Move Right
- J: Light Punch
- K: Light Kick
- L: Heavy Punch
- I: Heavy Kick
- U: Special Move / Projectile
- SHIFT: Dash
- P: Block

**Player 2 (Arrows):**
- UP: Jump
- DOWN: Crouch
- LEFT: Move Left
- RIGHT: Move Right
- U: Light Punch
- I: Light Kick
- O: Heavy Punch
- RSHIFT: Special Move
- RCTRL: Dash
- [: Block

### Features to Verify:

✅ Character selection works
✅ All 4 characters selectable
✅ Character animations play correctly
✅ Movement in all directions
✅ Dash mechanic works
✅ All 5 attack types work
✅ Blocking reduces damage
✅ Projectiles spawn and move
✅ Projectiles hit and deal damage
✅ Health bars decrease on hit
✅ Super meter fills on attack
✅ Combos execute (test combo inputs)
✅ Knockdown animation plays
✅ Victory/defeat screens show
✅ AI opponents attack and defend
✅ Game doesn't crash

---

## Combo Testing

Test each combo by entering the input sequence:

**PROF. KHALID:**
- Tornado Rush: L → L → I (3 hits, 1.3x damage)
- Flying Axe: W → I (while jumping, 1.4x damage)

**PROF. EDUARDO:**
- Pizza Barrage: J → J → U (3 hits, 1.35x damage)
- Giant Disc: K → U (2 hits, 1.5x damage)

**PROF. HASAN:**
- Flame Uppercut: L → K → U (3 hits, 1.4x damage)
- Double Fireball: U → U (2 projectiles, 1.6x damage)

**PROF. HAMMOUD:**
- Binary Rush: J → J → L → I (4 hits, 1.45x damage)
- EMP Blast: W → U (aerial special, 1.5x damage)

---

## Automated Test Details

### What Gets Tested:

**Existence Tests:**
- All classes instantiate without errors
- All required attributes exist
- All required methods exist

**Functionality Tests:**
- Attacks execute and create hitboxes
- Projectiles move and collide
- Particles update positions
- Health decreases on damage
- Super meter increases

**Data Validation:**
- All stats are numbers
- All colors are valid
- All combos have inputs
- All damage multipliers exist

**Integration Tests:**
- Fighter + Projectile interaction
- Attack + Damage system
- Combo + Super meter

### Test Output Format:

```
✓ Test Name - Test passed
✗ Test Name - Test failed

Pass Rate: X/Y tests (Z%)
```

---

## Debugging Failed Tests

If a test fails:

1. **Check the error message**
   - Test name indicates what failed
   - Error details show the specific issue

2. **Verify attribute existence**
   ```python
   print(hasattr(object, 'attribute_name'))
   ```

3. **Check attribute values**
   ```python
   print(object.attribute_name)
   ```

4. **Test manually**
   - Launch the game
   - Try to trigger the failed scenario
   - Check for error messages

---

## Continuous Integration

To ensure code quality:

1. **Before committing:**
   ```bash
   python test_comprehensive.py
   ```
   
2. **Only commit if:** All 354 tests pass

3. **After pulling changes:**
   ```bash
   python test_comprehensive.py
   ```

4. **When adding features:**
   - Add corresponding tests
   - Ensure existing tests still pass

---

## Performance Testing

Test game performance:

```bash
# Run game for 5 seconds
timeout 5 python main.py
echo $?  # Should be 124 (timeout) not 1 (error)
```

Expected: Game runs smoothly at 60 FPS

---

## Test Files

- **test_comprehensive.py** - Main test suite (354 tests)
- **TEST_REPORT.md** - Test results documentation
- **FIXES_APPLIED.md** - Bug fix history

---

## Known Limitations

- No music file (expected, game runs without it)
- AVX2 warning (cosmetic, doesn't affect functionality)
- Tests don't validate graphics (only logic)

---

## Support

If tests fail or game crashes:

1. Check [FIXES_APPLIED.md](FIXES_APPLIED.md) for known issues
2. Check [TEST_REPORT.md](TEST_REPORT.md) for expected behavior
3. Run tests to identify specific failures
4. Check terminal output for error messages

---

**Current Status: 354/354 Tests Passing ✅**
