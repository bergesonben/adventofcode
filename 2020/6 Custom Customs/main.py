import argparse
import sys
sys.path.append('.')
import part1
import part2
import pathlib

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('part', type=int, help='which part to run', default=1, nargs='?', choices=[1, 2])
parser.add_argument('--test', '-t', type=int, help='the test number to try, defaults to blank', nargs='?', default=-1)

args = parser.parse_args()
partNum = args.part
testNum = args.test

if testNum is None:
    input = str(pathlib.Path(__file__).parent.absolute()) + '/test'
elif testNum == -1:
    input = str(pathlib.Path(__file__).parent.absolute()) + '/input'
else:
    input = str(pathlib.Path(__file__).parent.absolute()) + '/test' + str(testNum)

if partNum == 1:
    part1.main(input)
else:
    part2.main(input)