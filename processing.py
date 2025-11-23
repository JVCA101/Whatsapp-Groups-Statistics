import os
import re

class Person:
    def __init__(self, name, messages_count=0, media_count=0, kkks_count=0):
        self.name           = name
        self.messages_count = messages_count
        self.media_count    = media_count
        self.kkks_count     = kkks_count

# def has_valid_datetime_format(text):
    # pattern = r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2} - '
    # pattern2= r'^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - '
    # return bool(re.match(pattern, text)) or bool(re.match(pattern2, text))

# def extract_datetime(text):
    # patterns = [
        # r'(^\d{2}/\d{2}/\d{4} \d{2}:\d{2} - )',
        # r'(^\d{1}/\d{2}/\d{4}, \d{2}:\d{2} - )'
    # ]
    # 
    # for pattern in patterns:
        # match = re.match(pattern, text)
        # if match:
            # datetime_part = match.group(1)
            # content_part = text[len(datetime_part):]
            # return datetime_part, content_part
    # 
    # return None, text

def extract_datetime(line):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s*[,]?\s*\d{1,2}:\d{2}\s*-\s*)'
    
    match = re.match(pattern, line)
    if match:
        datetime_part = match.group(1)
        content_part = line[len(datetime_part):]
        return datetime_part, content_part.strip()
    
    return None, line

def person_on_list(person, people):
    for p in people:
        if p.name == person:
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
                    person_on_list(rest.split(":")[0], people)
                    message_count += 1
            else:
                pass

    print(message_count)
    for person in people:
        print(person.name + ":" + str(person.messages_count))
    os.chdir("../")


def main():
    # print(os.listdir(os.getcwd()))
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_txt(dir)
            print("\n")

if __name__ == "__main__":
    main()
