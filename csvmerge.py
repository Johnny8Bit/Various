'''
Merges all CSV files in current working directory into single CSV file

'''
import os
import csv

FILE_EXTENSION = ".csv"
NEW_FILE = "merged.csv"

def read_all_csv(): 

    data = []
    files = (file for file in os.listdir(os.getcwd()) if file.endswith(FILE_EXTENSION))
    for file in files:

        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)

    return data

def write_new_csv(data):

    with open(NEW_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':

    write_new_csv(read_all_csv())