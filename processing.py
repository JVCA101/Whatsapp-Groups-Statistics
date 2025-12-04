import os
import re
import numpy as np

# struct of Person
class Person:
    def __init__(self, name: str, messages_count=0, media_count=0, kkks_count=None):
        self.name           = name
        self.messages_count = messages_count
        self.media_count    = media_count

        if kkks_count == None:
            self.kkks_count = []
        else:
            self.kkks_count = kkks_count

def extract_datetime(line: str):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s*[,]?\s*\d{1,2}:\d{2}\s*-\s*)'
    
    match = re.match(pattern, line)
    if match:
        datetime_part = match.group(1)
        content_part = line[len(datetime_part):]
        return datetime_part, content_part.strip()
    
    return None, line

def count_kk(message: str):
    message = message.lower()
    
    # did not find laugh
    if message.find("kk") < 1:
        return [-1]

    # processing string to count how many k's are on each laugh
    substrings = message.split(' ')
    counter_kk = []

    for s in substrings:
        if s.count("kk") >= 1:
            counter_kk.append(s.__len__())

    return counter_kk

def person_on_list(person: str, people, rest: str):
    for p in people:
        if p.name == person:
            if rest == "this message was deleted":
                print("message deleted")
                continue
            elif rest == " <Mídia oculta>" or rest == " <Media omitted>":
                p.media_count += 1
            else:
                p.messages_count += 1
                counter_kk = count_kk(rest)
                for laugh in counter_kk:
                    if laugh >= 2:
                        p.kkks_count.append(laugh)
            return
    
    people.append(Person(person, messages_count=1))

def process_txt(dir: str):
    people = []
    message_count = 0
    os.chdir(dir)
    
    with open(dir+".txt", "r") as file:
        for line in file:
            datetime, rest = extract_datetime(line)
            if datetime != None:

                # if is not a message by someone, the skip
                if ":" in rest:
                    person_on_list(rest.split(":")[0], people, rest.split(":")[1])
                    message_count += 1
            else:
                pass

    print("Total: " + str(message_count))
    print("Quantidade de mensagens por pessoa")
    for person in people:
        print(person.name + ": " + str(person.messages_count))
    print("\nQuantidade de media por pessoa")
    for person in people:
        print(person.name + ": " + str(person.media_count))
    print("\nQuantidade de k's por mensagem por pessoa")
    for person in people:
        print(person.name + ": " + str(np.sum(person.kkks_count)))
    print("\nMédia de quantidade de k's por mensagem por pessoa")
    for person in people:
        if person.kkks_count.__len__() > 0:
            print(person.name + ": " + str(np.sum(person.kkks_count) / person.kkks_count.__len__()))


    with open("output.txt", 'w') as output_file:
        for person in people:
            output_file.write(str(person.name)           + ';' +
                              str(person.messages_count) + ';' +
                              str(person.media_count)    + ';')

            if person.kkks_count.__len__() > 0:
                output_file.write(str(np.sum(person.kkks_count) / person.kkks_count.__len__()) + ';')
            else:
                output_file.write(';')
            output_file.write('\n')

    os.chdir("../")


def main():

    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_txt(dir)

if __name__ == "__main__":
    main()
