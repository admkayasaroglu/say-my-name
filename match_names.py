import fuzzy
import random

class Matcher:
    def __init__(self):
        (first, last) = self.create_dicts()
        self.first_names = first
        self.last_names = last

    def dtm(self, name):
        dmeta = fuzzy.DMetaphone(4)
        return dmeta(name)

    def add_name(self, names, name, gender):
        sounds = self.dtm(name)
        name_info = {"name": name, "gender": gender}
        for sound in sounds:
            if sound:
                if sound in names:
                    names[sound].append(name_info)
                else:
                    names[sound] = [name_info]

    def create_dicts(self):
        f = open("first_names.txt", 'r')
        names = {}
        for line in f:
            (num, boy, girl) = line.split()
            self.add_name(names, girl, "F")
            self.add_name(names, boy, "M")

        f = open("last_name.txt", 'r')
        last_names = {}
        for line in f:
            name_array = line.split()
            if name_array:
                name = name_array[0].title()
                self.add_name(last_names, name, None)

        return (names, last_names)

    def get_matches(self, name, name_dict, gender):
        sounds = self.dtm(name)
        matches = []
        for sound in sounds:
            if sound:
                if sound in name_dict:
                    options = name_dict[sound]
                    if gender:
                        options = [n for n in options if n["gender"]==gender]
                    matches.extend([n["name"] for n in options])

        return matches

    def get_match_array(self, name, num_matches, primary_dict, secondary_dict):
        matches = self.get_matches(name, primary_dict, None)
        if len(matches) < num_matches:
            extras = self.get_matches(name, secondary_dict, None)
            num_to_add = min(num_matches - len(matches), len(extras))
            chosen = random.sample(extras, num_to_add)
            matches.extend(chosen)
        return matches

    def match(self, name, num_matches):
        name_array = name.split()
        first = name_array[0]
        last = name_array[-1]

        name_choices = []
        for n in name_array[:-1]: # first and middle names
            matches = self.get_match_array(n, num_matches, self.first_names, self.last_names)
            name_choices.append(matches)
        matches = self.get_match_array(last, num_matches, self.last_names, self.first_names)
        if len(matches) < num_matches:
            mult = num_matches / len(matches) + 1
            matches = (matches * mult)[:num_matches] 
        random.shuffle(matches)
        name_choices.append(matches)

        final_names = map(" ".join, zip(*name_choices))
        return final_names

    def try_names(self):
        while True:
            name = raw_input("what's your name?")
            self.match_me(name, 5)
            
    def try_first_names(self):
        while True:
            name = raw_input("what's your name?")
            sounds = self.dtm(name)
            print sounds
            for sound in sounds:
                if sound:
                    if sound in self.first_names:
                        options = self.first_names[sound]
                        print options
                    if sound in self.last_names:
                        options = self.last_names[sound]
                        print options









    


