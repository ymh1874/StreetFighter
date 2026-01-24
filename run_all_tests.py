#!/usr/bin/env python3
"""
Comprehensive test runner for Street Fighter game
Runs all test suites and provides a summary
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode for pygame

import subprocess
import sys

def run_test_suite(test_file):
    """Run a test suite and return results"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}...")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Filter out noise (ALSA warnings, pygame messages)
        output_lines = result.stdout.split('\n')
        filtered_lines = [
            line for line in output_lines 
            if not any(noise in line for noise in ['ALSA', 'pygame community', 'Warning'])
        ]
        
        print('\n'.join(filtered_lines))
        
        if result.returncode == 0:
            print(f"✓ {test_file} PASSED")
            return True
        else:
            print(f"✗ {test_file} FAILED")
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error running {test_file}: {e}")
        return False

def main():
    """Run all test suites"""
    print("\n" + "="*60)
    print("STREET FIGHTER GAME - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    test_suites = [
        'test_basic.py',
        'test_enhanced_features.py',
        'test_game_integration.py',
    ]
    
    results = {}
    for test_file in test_suites:
        results[test_file] = run_test_suite(test_file)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_file, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_file:40} {status}")
    
    print("="*60)
    print(f"Total: {passed}/{total} test suites passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
