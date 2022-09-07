import re
import random

words = []
with open('speech.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        line = re.sub(r'[\"\'\:\,\-\_\;\‘]', ' ', line)
        words.extend(line.split())
    
predictions = {}
for i in range(0, len(words) - 1):
    if words[i] in predictions:
        if words[i+1] in predictions[words[i]]:
            predictions[words[i]][words[i+1]] += 1
        else:
            predictions[words[i]][words[i+1]] = 1
    else:
        predictions[words[i]] = {}
        predictions[words[i]][words[i+1]] = 1

sentence = random.choice(words)
while sentence.endswith(('.', '?', '!')) or not sentence[0].isupper():
    sentence = random.choice(words)
    
while True:
    nextWord = random.choice(sorted(predictions[sentence.split()[-1]], key=predictions[sentence.split()[-1]].get, reverse=True)[:5])
    sentence = ' '.join([sentence, nextWord])
    if nextWord.endswith(('.', '?', '!')):
        print(sentence)
        break