import os
import pandas as pd

def process_output(dir: str):
    os.chdir(dir)
    with open("people_stat.txt", 'r') as output_file:
        for line in output_file:
            parameters = line.split(";")[:-1]
            print(parameters)

    print("")
    os.chdir("../")

def main():
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_output(dir)

if __name__ == "__main__":
    main()
