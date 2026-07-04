import sys
sys.path.append('src/gateways')
from fsda_gateway import FSDA
import matlab
import numpy as np

fsda = FSDA()

try:
    # Test 1: zscoreFS (simple numeric)
    print("--- Testing zscoreFS ---")
    data = matlab.double([[1,2,3],[4,5,6],[7,8,9]])
    result = fsda.run('zscoreFS', data)
    print(result)

    # Test 2: FSM (Forward Search, no plots)
    print("\n--- Testing FSM ---")
    Y = matlab.double(np.random.randn(200, 3).tolist())
    result_fsm = fsda.run('FSM', Y, 'plots', False, 'msg', False)
    print("FSM ran successfully")

    # Test 3: FSR (Robust Regression)
    print("\n--- Testing FSR ---")
    y = matlab.double(np.random.randn(200, 1).tolist())
    X = matlab.double(np.random.randn(200, 3).tolist())
    result_fsr = fsda.run('FSR', y, X, 'plots', False, 'msg', False)
    print("FSR ran successfully")

    # Test 4: getYahoo (real-world, string args + options)
    print("\n--- Testing getYahoo ---")
    result_yahoo = fsda.run('getYahoo', 'AAPL', 'plots', False, 'LastPeriod', '1d')
    print("Ticker:", result_yahoo['Ticker'])
    print("Success:", result_yahoo['Success'])

    print("\n--- ALL TESTS PASSED ---")

except Exception as e:
    print(f"\n[!] TEST FAILED: {e}")

finally:
    fsda.close()