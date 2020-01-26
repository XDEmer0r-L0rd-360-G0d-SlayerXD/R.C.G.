import os
import Run_System
import time


def main():
    now = time.time()
    os.chdir('data')
    with open('links.txt', 'r') as f:
        links = f.read().split('\n')
    os.chdir('..')
    for a in links:
        print(a)
        Run_System.main(a)
    print('done:', len(links), time.time() - now, (time.time() - now) / 60, (time.time() - now) / 60 / len(links))


if __name__ == '__main__':
    main()
