import os, psutil
from subprocess import check_output

print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
