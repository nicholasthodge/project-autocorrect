# Preliminary Testing - can ignore
from transformers import AutoTokenizer, TFBartForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained("veghar/spell_correct_bart_base")
model = TFBartForConditionalGeneration.from_pretrained("veghar/spell_correct_bart_base")

text= "wha's"
text_tok=tokenizer(text,padding=True, return_tensors='tf')
input_ids = text_tok['input_ids']
outputs = model.generate(input_ids=input_ids, max_length=10,num_return_sequences=1)
corrected_sentences = tokenizer.batch_decode(outputs, skip_special_tokens=True)

print('Misspelled word:', text)
print('Corrected word:', corrected_sentences)
