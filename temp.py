import sys
import random

sys.stdout = open("input.txt",'w')

for i in range(1,1000):
    print(f'g{i} {random.randint(1,100)} {random.randint(1,100)}')