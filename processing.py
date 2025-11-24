import os
import re

class Person:
    def __init__(self, name, messages_count=0, media_count=0, kkks_count=0):
        self.name           = name
        self.messages_count = messages_count
        self.media_count    = media_count
        self.kkks_count     = kkks_count

def extract_datetime(line):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s*[,]?\s*\d{1,2}:\d{2}\s*-\s*)'
    
    match = re.match(pattern, line)
    if match:
        datetime_part = match.group(1)
        content_part = line[len(datetime_part):]
        return datetime_part, content_part.strip()
    
    return None, line

def person_on_list(person, people, rest):
    for p in people:
        if p.name == person:
            if rest == " <Mídia oculta>" or rest == " <Media omitted>":
                p.media_count += 1
            else:
                p.messages_count += 1
            return
    
    people.append(Person(person, messages_count=1))

def process_txt(dir):
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

    os.chdir("../")


def main():
    # print(os.listdir(os.getcwd()))
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_txt(dir)
            print("\n")

if __name__ == "__main__":
    main()
