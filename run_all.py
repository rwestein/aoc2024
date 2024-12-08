import os
import unittest

suite = unittest.TestSuite()
for filename in sorted(os.listdir('.')):
    if filename.startswith('dec') and filename.endswith('.py'):
        name = filename.replace('.py', '')
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)