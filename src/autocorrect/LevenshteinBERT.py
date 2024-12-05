import csv
from transformers import pipeline
from Levenshtein import distance

# Initializes BERT pipeline
fill_masker = pipeline(model="google-bert/bert-base-uncased")

# Function to calculate Levenshtein distance
# Uses distance function from Levenshtein module
def levenshtein_distance(word1, word2):
    return distance(word1, word2)


filename = "/dataset/train.csv"  # Replace with the actual path
x_predictions = 5  # Number of top predictions to consider

# Reads csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Skips the header

    # Accuracy trackers
    total_cases = 0
    bert_alone_correct = 0
    bert_lev_correct = 0

    # Processes each row
    for row in csvreader:
        total_cases += 1
        sentence = row[2]
        misspelled_word = row[3]
        correct_word = row[4]

        # Gets BERT predictions
        predictions = fill_masker(sentence, top_k=x_predictions)  # top_k gets specified number of predictions
        predicted_words = [pred['token_str'] for pred in predictions]  # extracts predicted words

        # Takes BERT'S first prediction
        bert_alone_guess = predicted_words[0]
        if bert_alone_guess == correct_word:
            bert_alone_correct += 1

        # Use Levenshtein to find BERT prediction with smallest distance
        best_guess = None
        min_distance = 10000
        for predicted_word in predicted_words:
            dist = levenshtein_distance(predicted_word, correct_word)
            if dist < min_distance:
                min_distance = dist
                best_guess = predicted_word

        if best_guess == correct_word:
            bert_lev_correct += 1

print("Total Cases:", total_cases)
print(f"BERT Alone Accuracy: {bert_alone_correct / total_cases * 100:.2f}%")
print(f"BERT + Levenshtein Accuracy: {bert_lev_correct / total_cases * 100:.2f}%")

