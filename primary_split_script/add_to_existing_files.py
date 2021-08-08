import argparse
import os

def splitter(file, number):
    with open(file, 'r', encoding= 'unicode_escape') as f:
        para = sum(line.isspace() for line in f) + 1

    with open(file, 'r+', encoding= 'unicode_escape') as f:
        contents = f.read()

    name = os.path.basename(file).split(".")[:-1]
    name = ''.join(map(str, name))
    contents = contents.split('\n\n')
    for i in range(para):
        try:
            with open('{}-{}.txt'.format(name,number+1), 'w', encoding= 'unicode_escape') as o1:
                o1.write(str(contents[i]))
            counter+=1
        except:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Pass a directory to find original licenses')
    parser.add_argument('number', help='Number of existing licenses')
    args = parser.parse_args()
    path = args.path
    number = args.number
    splitter(path, number)
    