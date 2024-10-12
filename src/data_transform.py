# Has not been run, need to add give_typo() functionality
import csv
import random
import re

def give_typo(given_word):
    characters = given_word.strip().split()


def create_data(read_file, write_file):
    with open(read_file, mode='f') as rf:
        for line in rf:
            context_blocks = line.split("\n")

    with open(write_file, mode='w'):
        with open(write_file, 'w', newline='') as wf:
            csv_writer = csv.writer(wf)
            csv_writer.writerow(['Context Block ID', 'Message ID', 'Misspelled Message', 'Misspelled Word', 'Correct Word'])
            for block_idx, context_block in enumerate(context_blocks):
                messages = context_block.split("__eou__")

                for sentence_idx, message in enumerate(messages):
                    pattern = r"\s*([',.!?])\s*"
                    message = re.sub(pattern, r"\1", message)

                    words = message.split()
                    chosen_word = random.choice(words)
                    mispelled_word = give_typo(chosen_word)

                    # csv_writer.writerow([block_idx + 1, sentence_idx + 1, sentence, misspelled_word, chosen_word])