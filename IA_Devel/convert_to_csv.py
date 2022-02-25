#!/usr/bin/env python3

"""
    This program cleans up the dataset.txt file
    Then converts the results to comments.csv
"""

import os
import sys

def parse_dataset():
    print("Input: 'dataset.txt'")
    print("Output: 'comments.csv'")
    try:
        src = open('dataset.txt', 'r')
        dest = open('comments.csv', 'w+')
        count = 0

        s_count = 0
        while True:
            count += 1

            # Read file line by line
            line = src.readline()
            # If at end of file break loop
            if not line:
                break

            # Split line on delimiter
            s = line.split(';')

            if count != 1:
                s[1] = s[1].replace('\'', '\\\'').replace(';', '').replace(
                    '&#34', '').replace('""', '\\\'').replace('"', '\\\'')
                s[1] = ' '.join(s[1].split())

                if "&#" not in s[1]:
                    if len(s) > 3:
                        print("Size Error line: {}".format(count))

                    # If positive set 1 else 0 (negative)
                    if s[2] == "positive\n" or s[2] == "positive":
                        s[2] = "1\n"
                    else:
                        s[2] = "0\n"

                    dest.writelines('"' + s[1] + '" ; ' + str(s[2]))
                    s_count += 1
                else:
                    print("Skipping Bad line: {}".format(count))

        dest.close()
        src.close()
        print("{} entries converted successfully!".format(s_count))
        return True

    except FileNotFoundError:
        print("Error: Cannot find file 'dataset.txt'")
        return False


if __name__ == "__main__":
    if parse_dataset():
        sys.exit(0)
    else:
        sys.exit(1)
