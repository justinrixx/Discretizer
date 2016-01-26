#!/usr/bin/python

""" discretizer.py: Discretizes a csv file """

import numpy as np
import sys

def main(argv):
    # Get the source and destination files

    if len(argv) == 3:
        srcfile = argv[1]
        dstfile = argv[2]
    else:
        srcfile = input("Source Filename: ")
        dstfile = input("Destination Filename: ")

    # read the file into a multidimensional array of strings
    csv = np.genfromtxt(srcfile, delimiter=',', dtype=str)

    columns = csv[0]
    numeric_columns = []
    # look for numeric columns that need to be changed
    for i, attribute in enumerate(columns):
        numeric_columns.append(i)

    sets = []
    # create an empty set for each numeric column
    for column in numeric_columns:
        sets.append(set())

    # now get all the possible values for the columns in the sets
    for instance in csv:
        for i, column in enumerate(numeric_columns):
            sets[i].add(instance[column])

    # next get user clarification
    for i, column in enumerate(numeric_columns):

        is_numeric = False

        for value in sets[i]:
            if is_number(value):
                is_numeric = True

        if is_numeric:
            print("How many bins would you like to break column ", i, " into?")
            choice = input()

            # be sure to get a positive number
            while int(choice) < 1:
                print("How many bins would you like to break column ", i, " into?")
                choice = input()

            separators = []

            # get the min and max values for the column
            max_val = float(max(csv[:, i]))
            min_val = float(min(csv[:, i]))

            # calculate the midpoints
            for j in range(int(choice) - 1):
                separators.append((max_val - min_val) * ((j + 1) / int(choice)) + min_val)

            # replace the values with discrete values
            for j, instance in enumerate(csv):

                val = 0
                if float(instance[i]) > separators[-1]:
                    val = len(separators)

                else:
                    for k in range(len(separators)):
                        if k != 0:
                            if separators[k - 1] < float(instance[i]) <= separators[k]:
                                val = k
                        else:
                            if float(instance[i]) <= separators[k]:
                                val = k

                # replace it with the correct value
                csv[j][i] = val

    # write the file
    np.savetxt(dstfile, csv, delimiter=',', fmt='%s')
    print("Done")


def is_number(s):
    """Determines if a string represents a number
    :param s: The string to check
    Tries to cast the string to a float. If an exception
    is raised, returns false. If not, returns true
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

# This is here to ensure main is only called when
#   this file is run, not just loaded
if __name__ == "__main__":
    main(sys.argv)