import transformers
from transformers import pipeline
import csv


fill_masker = pipeline(model="google-bert/bert-base-uncased")

filename = "../dataset/train.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)


for row in rows[:2]:
    predicted_words = []
    # parsing each column of a row
    sentence = row[2]
    predictions = fill_masker(sentence)
    for prediction in predictions:
        predicted_words.append(prediction['token_str'])

    print(f"Original Word: {row[4]}\tPredicted Words: {','.join(predicted_words)}")
