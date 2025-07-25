import os
from pathlib import Path

a = Path('tests.py')
b = os.path.basename(a)
print(b)