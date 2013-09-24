#!/usr/bin/env python2

from sys import argv
import re

filename = argv[1]

options = ['Ae', 'An', 'ACM', 'AM', 'APh', 'Art', 'Ay', 'BMB', 'BE', 'Bi',
'BEM', 'Ch', 'CHE', 'CDS', 'CNS', 'CS', 'CE', 'Ec', 'ESL', 'EE', 'E', 'EN',
'ESE', 'F', 'FS', 'Ge', 'H', 'HPS', 'Hum', 'L', 'Law', 'Ma', 'MS', 'ME',
'Mu', 'Pl', 'PE', 'Ph', 'PS', 'PA', 'Psy', 'SS', 'SA', 'Wr']

types = ['course_name', 'section number', 'units', 'prof name', 'days/time',
        'location', 'grade scheme', 'annotation', 'unsure']

state = 'course'
cur_option = ""
cur_number = 0
cur_name = ""
cur_units = []
cur_class = ""
cur_section = ""

with open(filename, "r") as f:
    lines = f.readlines()

for line in lines:
    line = " ".join(line.split())
    # Are we looking at an option?
    option_line = False
    for opt in options:
        m = re.match(opt, line)
        if (m):
            # We have a potential option at the beginning of our line, so we
            # will insert a space between any occurrence of letter-number
            match = re.search('[A-Za-z][0-9]', line)
            if (match):
                # We need to separate letter-number now
                first_half = line[0: match.start() + 1]
                second_half = line[match.end() - 1:]
                newline = first_half + ' ' + second_half
            # Now that we have separated letter and number, we can tokenize
            # the string into 2 list items, hopefully the option and the
            # course number
            tok_line = newline.split()
            if len(tok_line) != 2:
                # Must contain two tokens (option, course_number) to be
                # option line
                break
            if not (re.match('[0-9]+[A-Za-z]*', tok_line[1])):
                # Must have a course number matching the above regex
                break
            option_line = True
        if option_line: 
            break
    if state == "course":
        # Course state will handle option, number, name, and units.
        #tok_line = line.split()
        if option_line:
            cur_option = tok_line[0]
            cur_number = tok_line[1]
            print "Option: %s, Number: %s" % (cur_option, cur_number)
        elif (len(tok_line) > 1):
            # Assuming all courses have a name longer than one word.
            cur_name = " ".join(tok_line)
            print cur_name
        else:
            # Token line has 1 "word" only, this means units
            cur_units = tok_line[0].split("-")
            print cur_units
        option_line = False
    elif state == "section":
       """ section will handle professor first and last names, subtitle,
       annotations, fixed time, times, days, locations, and grades. """
       pass

#types = ['course_name', 'section number', 'units', 'prof name', 'days/time',
        #'location', 'grade scheme', 'annotation', 'unsure']

def f_0(tokens, string): 
    # Return true if tokens match guess 0 from typelist, false otherwise
    if len(tokens) == 2:
        opt = tokens[0]
        number = tokens[1]
        if opt + number == string or opt + ' ' + number == string:
            # Our tokens, when combined (modulo space) should give us back
            # our original string.
            if opt in options:
                # Final check for opt being a valid option
                return True
        return False

def f_1(tokens, string):
    # Return true if tokens match section number
    if len(tokens) == 1 and re.match('^[0-9]{1,2}$', tokens[0]):
        if tokens[0] == string:
            return True
    return False

def f_2(tokens, string):
    # Return true if tokens match units
    if len(tokens) == 3:
        for tok in tokens:
            if not re.match('1?[0-9]', tok) or not tok in string:
                return False
        return True

def f_3(tokens, string):
    # Return true if tokens match professor name(s). Assuming that names
    # will already have commas stripped
    if (
    
def f_4(tokens, string):
    # Check if tokens match days/time
    if (len(tokens) == 4):
        if matches('[MWTRF]+', tokens[0]):
            if matches(r'([0-9]|0[0-9]|1[0-9]|2[0-3])\.?[0-9]?', tokens[1])
                and matches(r'([0-9]|0[0-9]|1[0-9]|2[0-3])\.?[0-9]?',
                        tokens[3]):
                    return True
    return False
