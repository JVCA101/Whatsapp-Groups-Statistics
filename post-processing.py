import os
import pandas as pd

def process_output(dir: str):
    os.chdir(dir)
    with open("people_stat.txt", 'r') as output_file:
        info = []
        for line in output_file:
            parameters = line.split(";")[:-1]
            print(parameters)
            info.append(parameters)

        user_dictionary = {name: {
                            "messages_count": messages_count,
                            "media_count": media_count,
                            "emojis_count": emojis_count,
                            "kkks_max": kkks_max,
                            "kkks_min": kkks_min,
                            "kkks_avg": kkks_avg
                            } for name, messages_count, media_count, emojis_count, kkks_max, kkks_min, kkks_avg in info}
        print(user_dictionary)
    print("")
    os.chdir("../")

def main():
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_output(dir)

if __name__ == "__main__":
    main()
