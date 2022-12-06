#!/usr/bin/env python3
import time

data = open("day6.txt").read()

# Print the data string and highlight the current substring with 4 unique characters
for i in range(0, len(data) - 4):
    cur_sample = data[i : i + 4]
    cur_set = set(cur_sample)

    # Print the data string with the current substring highlighted in red and green
    highlighted = ""
    count = {}
    for char in cur_sample:
        if char in count:
            count[char] += 1
            if count[char] > 1:
                highlighted += "\033[31m" + char + "\033[0m"
            else:
                highlighted += "\033[32m" + char + "\033[0m"
        else:
            count[char] = 1
            highlighted += "\033[32m" + char + "\033[0m"
    time.sleep(0.25)
    print(data[:i] + highlighted + data[i + 4:] + '\r', end='')

    # If the set has 4 unique characters, print the index of the 4th character and break
    if len(set(cur_sample)) == 4:
        print(f"Solution 1: Index of 4th character = {i + 4}")

        # Loop through the rest of the data string and look for a substring with 14 unique characters
        for j in range(i + 4, len(data) - 14):
            s2 = data[j : j + 14]

            # Print the data string with the current substring highlighted in red and green
            highlighted = ""
            count = {}
            for char in s2:
                if char in count:
                    count[char] += 1
                    if count[char] > 1:
                        highlighted += "\033[31m" + char + "\033[0m"
                    else:
                        highlighted += "\033[32m" + char + "\033[0m"
                else:
                    count[char] = 1
                    highlighted += "\033[32m" + char + "\033[0m"
            time.sleep(0.25)
            print(data[:j] + highlighted + data[j + 14:] + '\r', end='')

            # If the set has 14 unique characters, print the index of the 14th character and break

            if len(set(s2)) == 14:
                print(f"Solution 2: Index of 14th character = {j+14}")
                break
        break
