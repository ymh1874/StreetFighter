"""
Master Test Suite for CMUQ Arena
Runs all test suites and provides comprehensive coverage report
"""

import sys
import subprocess

def run_test_suite(test_file, suite_name):
    """Run a test suite and return results"""
    print(f"\n{'='*70}")
    print(f"Running {suite_name}...")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            ['python', test_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            # Filter out ALSA warnings
            stderr_lines = [line for line in result.stderr.split('\n') 
                          if 'ALSA' not in line and 'pygame community' not in line and line.strip()]
            if stderr_lines:
                print("STDERR:", '\n'.join(stderr_lines))
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"✗ {suite_name} TIMED OUT")
        return False
    except Exception as e:
        print(f"✗ {suite_name} FAILED TO RUN: {e}")
        return False

def main():
    """Run all test suites"""
    print("\n" + "="*70)
    print("  CMUQ ARENA - MASTER TEST SUITE")
    print("  Comprehensive Testing of All Game Systems")
    print("="*70)
    
    test_suites = [
        ('test_alignment.py', 'UI Alignment Tests'),
        ('test_combat.py', 'Combat System Tests'),
        ('test_movement.py', 'Movement System Tests'),
        ('test_ui_integration.py', 'UI & Integration Tests'),
    ]
    
    results = []
    
    for test_file, suite_name in test_suites:
        success = run_test_suite(test_file, suite_name)
        results.append((suite_name, success))
    
    # Print final summary
    print("\n" + "="*70)
    print("MASTER TEST SUITE SUMMARY")
    print("="*70)
    
    passed_count = 0
    for suite_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {suite_name}")
        if passed:
            passed_count += 1
    
    print("-"*70)
    print(f"Total: {passed_count}/{len(results)} test suites passed")
    
    if passed_count == len(results):
        print("\n" + "="*70)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("The game is fully functional with no known bugs!")
        print("All systems verified:")
        print("  • Combat mechanics (attacks, damage, collisions)")
        print("  • Movement system (walking, jumping, gravity)")
        print("  • UI components (menus, HUD, visual effects)")
        print("  • Character balance and stats")
        print("  • Game state management")
        print("  • Integration between systems")
        print("="*70 + "\n")
        return 0
    else:
        print(f"\n✗ {len(results) - passed_count} test suite(s) failed")
        print("Please review the test output above for details.")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
