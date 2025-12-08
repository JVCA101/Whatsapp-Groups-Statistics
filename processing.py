import os
import emoji
import re
import numpy as np

people = []

# struct of Person
class Person:
    def __init__(self, name: str, messages_count=0, media_count=0, kkks_count=None):
        self.name            = name
        self.messages_count  = messages_count
        self.media_count     = media_count
        self.deleted_message = 0
        self.emoji_count   = 0

        if kkks_count == None:
            self.kkks_count = []
        else:
            self.kkks_count = kkks_count

def extract_datetime(line: str):
    """
    Extracts the date and time of a string, expected to be a message
    """
    pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s*[,]?\s*\d{1,2}:\d{2}\s*-\s*)'
    
    match = re.match(pattern, line)
    if match:
        datetime_part = match.group(1)
        content_part = line[len(datetime_part):]
        return datetime_part, content_part.strip()
    
    return None, line

def count_kk(message: str):
    """
    Counts the k's inside a string
    """
    message = message.lower()
    
    # did not find laugh
    if message.find("kk") < 1:
        return [-1]

    # processing string to count how many k's are on each laugh
    substrings = message.split(' ')
    counter_kk = list()

    for s in substrings:
        if s.count("kk") >= 1:
            counter_kk.append(s.__len__())

    return counter_kk

def person_on_list(name):
    """
    Verifies if a person is already in the "people" list
    """
    for person in people:
        if person.name == name:
            return person
    return None

def has_emoji(person: Person, message: str) -> None:
    for c in message:
        if emoji.is_emoji(c):
            person.emoji_count += 1

def is_media(message: str) -> bool:
    return (message == " <Mídia oculta>") or (message == " <Media omitted>")

def process_message(message: str, person: Person) -> None:
    """
    Processes the start of the message, before any '\n'
    """
    if message == "this message was deleted":
        person.deleted_message += 1
        return
    elif is_media(message):
        person.media_count += 1
        return
    else:
        person.messages_count += 1
        has_emoji(person, message)
        counter_kk = count_kk(message)
        for laugh in counter_kk:
            if laugh >= 2:
                person.kkks_count.append(laugh)

def process_continous_message(previous_person_name: str, message: str):
    if previous_person_name != "":
        person = person_on_list(previous_person_name)
        if person is None:
            print("ERROR: " + str(previous_person_name) + " is not in people list when it should be")
            exit(1)
        counter_kk = count_kk(message)
        for laugh in counter_kk:
            if laugh >= 2:
                person.kkks_count.append(laugh)
        has_emoji(person, message)

def split_message(message: str):
    """
    Splits a message in person_name and content
    """
    return message.split(":")[0], ':'.join(message.split(":")[1:])

def process_line(full_message: str):
    """
    Processes line, expected to be a message
    """
    # if is not a message by someone, then skip
    if ":" in full_message:
        person_name, message = split_message(full_message)
        person               = person_on_list(person_name)
        if person is None:
            people.append(Person(person_name, messages_count=1))
        else:
            process_message(message, person)
        return person_name
    return ""

def process_txt_person(dir: str):
    """
    Process .txt file with the same name as dir on directory dir and outputs in
    people_stat.txt with the statistics of people on the same directory.
    """
    os.chdir(dir)
    people.clear()

    with open(dir+".txt", "r") as file:
        previous_person_name = ""
        for line in file:
            datetime, full_message = extract_datetime(line)
            if datetime != None:
                previous_person_name = process_line(full_message)
            else:
                process_continous_message(previous_person_name, full_message)

    with open("people_stat.txt", 'w') as output_file:
        for person in people:
            output_file.write(str(person.name)           + ';' +
                              str(person.messages_count) + ';' +
                              str(person.media_count)    + ';' +
                              str(person.emoji_count)    + ';')

            if person.kkks_count.__len__() > 0:
                output_file.write(str(np.sum(person.kkks_count) / person.kkks_count.__len__()) + ';')
            else:
                output_file.write(';')
            output_file.write('\n')

    os.chdir("../")

def process_txt_global(dir: str):
    """
    Process .txt file with the same name as dir on directory dir and outputs in
    output.txt with the global statistics inside the dir directory
    """
    os.chdir(dir)
    emoji_hash = dict()

    with open(dir+".txt", 'r') as file:
        for line in file:
            _date, full_message = extract_datetime(line)
            _name, message      = split_message(full_message)
            for c in message:
                if emoji.is_emoji(c):
                    if c not in emoji_hash.keys():
                        emoji_hash[str(c)] = 1
                    else:
                        emoji_hash[str(c)] += int(1)
        print(emoji_hash)
    
    with open("output.txt", 'w') as output_file:
        output_file.write("teste")
        pass

    os.chdir("../")

def main():
    dirs = []
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_txt_person(dir)
            process_txt_global(dir)
            dirs.append(dir)
    with open("directories.txt", 'w') as file:
        for dir in dirs:
            file.write(dir + "\n")

if __name__ == "__main__":
    main()
