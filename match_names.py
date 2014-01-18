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
            if sound and sound in name_dict:
                options = name_dict[sound]
                if gender:
                    options = [n for n in options if n["gender"]==gender]
                matches.extend([n["name"] for n in options])

        
        matches = list(set(matches))
        return matches

    def get_match_array(self, name, num_matches, primary_dict, secondary_dict):
        matches = self.get_matches(name, primary_dict, None)

        if len(matches) < num_matches:
            extras = self.get_matches(name, secondary_dict, None)
            random.shuffle(extras)
            while len(matches) < num_matches and len(extras) > 0:
                new_name = extras.pop()
                if new_name not in matches:
                    matches.append(new_name)
        return matches

    def match(self, name, min_matches):
        name_array = name.split()

        name_choices = []
        # First and middle names
        for n in name_array[:-1]: # first and middle names
            matches = self.get_match_array(n, min_matches, self.first_names, self.last_names)
            if len(matches) == 0: 
                matches = [n.title()]
            name_choices.append(matches[:])
        # Last names
        last = name_array[-1]
        matches = self.get_match_array(last, min_matches, self.last_names, self.first_names)
        if len(matches) == 0:
            matches = [last.title()]
        name_choices.append(matches[:])

        #number of matches we will create
        min_uniques = min(len(names) for names in name_choices)
        max_uniques = max(len(names) for names in name_choices) 
        if min_uniques < min_matches:
           num_matches = min( min_uniques*3, max_uniques, min_matches)
           for i in range(len(name_choices)):
               matches = name_choices[i]
               mult = int(num_matches / len(matches) + 1)
               random.shuffle(matches)
               matches = (matches * mult)[:num_matches] 
               name_choices[i] = matches

        for matches in name_choices:
            random.shuffle(matches)

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









    


