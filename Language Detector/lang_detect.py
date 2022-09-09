from math import log
import sys
import re
import operator

train_data = sys.argv[1]
test_data = sys.argv[2]
output_data = sys.argv[3]

words = {}
words_count = {}
total_words_count = 0
lang_prob = {}
with open(train_data, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        lang = re.split(r',', line)[-1].replace('\n', '')
        line_words = re.sub(r'[\W+]', ' ', line.replace(f",{re.split(r',', line)[-1]}", '')).split()
        if lang in words:
            words[lang].extend(line_words)
            words_count[lang] += len(line_words)
        else:
            words[lang] = line_words
            words_count[lang] = len(line_words)
        for word in line_words:
            if lang in lang_prob:
                if word in lang_prob[lang]:
                    lang_prob[lang][word] += 1
                else:
                    lang_prob[lang][word] = 2
            else:
                lang_prob[lang] = {}
                if word in lang_prob[lang]:
                    lang_prob[lang][word] += 1
                else:
                    lang_prob[lang][word] = 2
        total_words_count += len(line_words)

null_lang_prob = {}
for lang in lang_prob:
    for word in lang_prob[lang]:
        lang_prob[lang][word] /= (total_words_count + words_count[lang])
        lang_prob[lang][word] = log(lang_prob[lang][word], 10)
    null_lang_prob[lang] = 1 / (total_words_count + words_count[lang])
    null_lang_prob[lang] = log(null_lang_prob[lang], 10)
        
line_lang = {}
with open(test_data, 'r', encoding='utf-8') as file:
    for line  in file.readlines():
        line_words = re.sub(r'[\W+]', ' ', line.replace(f",{re.split(r',', line)[-1]}", '')).split()
        line_lang_prob = {}
        for lang in lang_prob:
            for word in line_words:
                if word in lang_prob[lang]:
                    if lang in line_lang_prob:
                        line_lang_prob[lang] += lang_prob[lang][word]
                    else:
                        line_lang_prob[lang] = lang_prob[lang][word]
                else:
                    if lang in line_lang_prob:
                        line_lang_prob[lang] += null_lang_prob[lang]
                    else:
                        line_lang_prob[lang] = null_lang_prob[lang]
        line_lang[line] = max(line_lang_prob.items(), key=operator.itemgetter(1))[0]

with open(output_data, 'w', encoding='utf-8') as file:
    for line in line_lang:
        file.write(f'{line_lang[line]}\t{line}')

print(f'{len(line_lang)} lines where processed successfully!')