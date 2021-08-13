from tqdm import tqdm
import time
import random

i = 0
a = 0

# pbar = tqdm(total=100)
# for i in range(10):
#     sleep(0.1)
#     pbar.update(10)
# pbar.close()

pbar = tqdm(total=100)
while i < 50 or a != 3:
    time.sleep(0.1)
    a = random.randint(0, 10)
    pbar.update(1)
    i = i + 1
    # if a == 3:
    #     print(f'a={a}')
# pbar.update(pbar.g)
pbar.clear()
pbar.close()
