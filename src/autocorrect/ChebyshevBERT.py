import csv
from transformers import pipeline
from scipy.spatial.distance import chebyshev

# Initializes BERT pipeline
fill_masker = pipeline(model="google-bert/bert-base-uncased")


# Calculates Chebyshev distance
def chebyshev_distance(word1, word2):
    # Checks if words are same length
    if len(word1) != len(word2):
        max_len = max(len(word1), len(word2))
        # .ljust() adds spaces at the end of shorter word
        word1 = word1.ljust(max_len)
        word2 = word2.ljust(max_len)
    # Creates a list of ascii values for each character
    vec1 = [ord(c) for c in word1]
    vec2 = [ord(c) for c in word2]
    # Finds chebyshev distance of two vectors
    return chebyshev(vec1, vec2)


filename = "../dataset/train.csv"
x_predictions = 5  # Number of top predictions to consider

rows = []

# Reads csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Skips the header
    for row in csvreader:
        rows.append(row)

# Accuracy trackers
total_cases = 0
bert_alone_correct = 0
bert_chebyshev_correct = 0

# Processes each row
for row in rows[:1000]:  # Change number here to match num of rows wanted
    total_cases += 1
    sentence = row[2]
    misspelled_word = row[3]
    correct_word = row[4]

    # Gets BERT predictions
    predictions = fill_masker(sentence, top_k=x_predictions)  # top_k gets specified number of predictions
    predicted_words = [pred['token_str'] for pred in predictions]  # extracts predicted words

    # Takes standalone BERT's best guess
    bert_alone_guess = predicted_words[0]
    if bert_alone_guess == correct_word:
        bert_alone_correct += 1

    # Uses chebyshev distance to find BERT prediction with the smallest distance
    best_guess = None
    min_distance = 10000
    for predicted_word in predicted_words:
        dist = chebyshev_distance(predicted_word, correct_word)
        if dist < min_distance:
            min_distance = dist
            best_guess = predicted_word

    if best_guess == correct_word:
        bert_chebyshev_correct += 1

print("Total Cases:", total_cases)
print(f"BERT Alone Accuracy: {bert_alone_correct / total_cases * 100:.2f}%")
print(f"BERT + Chebyshev Accuracy: {bert_chebyshev_correct / total_cases * 100:.2f}%")
