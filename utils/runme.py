import subprocess
import sys

with open('../requirements.txt', 'r') as f:
    for line in f:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', line])
