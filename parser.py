#!/usr/bin/env python2

from sys import argv
import re

filename = argv[1]

options = ['Ae', 'An', 'ACM', 'AM', 'APh', 'Art', 'Ay', 'BMB', 'BE', 'Bi',
'BEM', 'Ch', 'CHE', 'CDS', 'CNS', 'CS', 'CE', 'Ec', 'ESL', 'EE', 'E', 'EN',
'ESE', 'F', 'FS', 'Ge', 'H', 'HPS', 'Hum', 'L', 'Law', 'Ma', 'MS', 'ME',
'Mu', 'Pl', 'PE', 'Ph', 'PS', 'PA', 'Psy', 'SS', 'SA', 'Wr']

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
                line = first_half + ' ' + second_half
            # Now that we have separated letter and number, we can tokenize
            # the string into 2 list items, hopefully the option and the
            # course number
            tok_line = line.split()
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
    elif state == "section":
       """ section will handle professor first and last names, subtitle,
       annotations, fixed time, times, days, locations, and grades. """
       pass
