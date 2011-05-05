from django.conf import settings

import random
import os.path

def get_random_line(filename):
    a = open(filename).read().split("\n")
    ret = ""
    while len(ret) < 3:
       ret = random.choice(a)
    return ret

def get_random_name():
   first_name = get_random_line(os.path.join(os.path.dirname(__file__))+"/finnish_names_men")
   last_name = get_random_line(os.path.join(os.path.dirname(__file__))+"/last_names")
   username = first_name[0]+last_name[0:3]
   return ("%s" % username.lower(), "%s %s" % (first_name, last_name))


if __name__ == '__main__':
   print get_random_name()
