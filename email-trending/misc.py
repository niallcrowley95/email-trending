"""Random stuff that doesn't deserve its own module"""
import csv
import random


def get_quote(file="addons/quotes.csv"):
    """Get random quote from json file"""
    # get length of file
    num_lines = sum(1 for line in open(file))
    # select random row
    index = random.randint(0, num_lines)
    with open(file, 'r', errors='ignore') as f:
        reader = csv.reader(f)
        row = [row for idx, row in enumerate(reader) if idx == index][0]
    return {"author": row[0], "quote": row[1]}


def print_progressbar(iteration,
                      total,
                      prefix='',
                      suffix='',
                      decimals=1,
                      length=50,
                      fill='█',
                      printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
