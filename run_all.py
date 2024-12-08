# from dec1 import *
# from dec2 import *
# from dec3 import *
# from dec4 import *
# from dec5 import *
# from dec6 import *
import importlib
import os
import unittest

suite = unittest.TestSuite()
for filename in sorted(os.listdir('.')):
    if filename.startswith('dec') and filename.endswith('.py'):
        name = filename.replace('.py', '')
        # print(name)
        # module = importlib.import_module(name)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)