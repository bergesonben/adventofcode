import sys

def main(): 
    with open('input') as f:
        lines = f.readlines()
        
    count = 0
    for line in lines:
        outputs = [i.strip() for i in line.split('|')[1].split()]
        for output in outputs:
            if len(output) == 2 or len(output) == 3 or len(output) == 4 or len(output) == 7:
                count += 1
    
    print(count)


    
    
if __name__ == '__main__':
    sys.exit(main())

