import csv
import random
import re
from src.autocorrect.keyboard_approach import chars_within_given_distance


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Replace non-ASCII characters with an empty string


# Function to introduce random typos in a word
def give_typo(given_word):
    characters = list(given_word)  # Convert the word to a list of characters
    error_count = random.randint(1, 3)  # Randomly decide how many errors (typos) to introduce
    # Keep track of indices that have already been modified to avoid multiple modifications to the same character
    modified_indices = set()

    # We need to address only characters
    for idx, char in enumerate(characters):
        # If character is not a-z or A-Z
        if not char.isalpha():
            modified_indices.add(idx)  # Mark this index as 'modified' to not use it

    for _ in range(error_count):
        available_indices = [i for i in range(len(characters)) if
                             i not in modified_indices]  # List of indices that haven't been modified yet
        if not available_indices:  # If there are no available indices left, exit the loop
            break
        index = random.choice(available_indices)  # Pick a random index to introduce the typo
        typo_type = random.choice(['delete', 'swap', 'mistype'])  # Randomly decide which type of typo to apply

        # Typo type: deletion
        if typo_type == 'delete':
            if len(characters) > 1:  # Only delete if the word has more than one character
                del characters[index]  # Delete the character at the chosen index
                modified_indices = {i - 1 if i > index else i for i in
                                    modified_indices}  # Adjust the modified indices after deletion

        # Typo type: character swap
        elif typo_type == 'swap':
            if 0 < index < len(characters) - 1:  # Only swap if the character is not at the beginning or the end
                swap_with = random.choice([-1, 1])  # Decide whether to swap with the left or right character
                swap_index = index + swap_with
                characters[index], characters[swap_index] = characters[swap_index], characters[
                    index]  # Swap the characters
                modified_indices.update([index, swap_index])  # Mark both characters involved in the swap as modified

        # Typo type: mistype (random character replacement)
        elif typo_type == 'mistype':
            # Replace the character with a random letter within a keyboard distance of 1
            mistyped_char = random.choice(chars_within_given_distance(characters[index], 1))
            characters[index] = mistyped_char
            modified_indices.add(index)  # Mark this index as modified

    new_word = ''.join(characters)  # Join the modified characters to form the new word
    return new_word


# Function to process a file and create a CSV with context blocks and typo data
# Function to process a file and create a CSV with context blocks and typo data
def create_data(read_file, write_file):
    # Open the input file for reading
    with open(read_file, mode='r', encoding="utf8") as rf:
        data = rf.read()  # Read the entire content of the file
    context_blocks = data.split(
        "\n")  # Split the file content into context blocks, each block is separated by a newline

    # Open the output file for writing in CSV format
    with open(write_file, 'w', newline='') as wf:
        csv_writer = csv.writer(wf)  # Create a CSV writer object
        # Write the header row in the CSV
        csv_writer.writerow(
            ['Context Block ID', 'Message ID', 'Misspelled Message', 'Misspelled Word', 'Correct Word'])

        # Iterate over each context block
        for block_idx, context_block in enumerate(context_blocks):
            messages = context_block.split(
                "__eou__")  # Split each block into individual messages, separated by '__eou__'

            # Iterate over each message in the block
            for message_idx, message in enumerate(messages):
                if message:
                    # Remove non-ASCII characters (there is lots of this in the original dataset)
                    message = remove_non_ascii(message)

                    pattern = r"\s*([',.!?])"  # Regex pattern to remove spaces around punctuation marks
                    # Clean up the message by removing unnecessary spaces around punctuation
                    message = re.sub(pattern, r"\1", message)

                    words = message.split()  # Split the message into words
                    if words:
                        # Extract punctuation from words
                        word_with_punctuations = [(re.sub(r"[^\w]", "", word), re.findall(r"[^\w]", word))
                                                  for word in words]

                        # Randomly choose a word to introduce a typo
                        chosen_idx = random.randint(0, len(word_with_punctuations) - 1)
                        chosen_word, punctuation = word_with_punctuations[chosen_idx]

                        # Generate a misspelled version of the chosen word
                        misspelled_word = give_typo(chosen_word)

                        # Replace the chosen word in the message with the [MASK] token
                        mask_word_with_punctuation = f"[MASK]{''.join(punctuation)}"
                        words[chosen_idx] = mask_word_with_punctuation

                        # Reconstruct the new message
                        new_message = ' '.join(words)

                        # Write the result as a new row in the CSV
                        # includes context block ID, message ID, original message, misspelled word, and correct word
                        csv_writer.writerow(
                            [block_idx + 1, message_idx + 1, new_message, misspelled_word, chosen_word])


# Driver
create_data("original_DailyDialog_train.txt", "train.csv")
