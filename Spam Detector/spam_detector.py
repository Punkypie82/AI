import sys
import re

trainFile = sys.argv[1]
testFile = sys.argv[2]
outputFile = sys.argv[3]
spamWords = []
hamWords = []
with open(trainFile, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        if  re.split(r'\t', line)[0] == 'ham':
            hamWords.extend(re.sub(r'[\W+]', ' ', re.split(r'\t', line)[1]).split())
        else:
            spamWords.extend(re.sub(r'[\W+]', ' ', re.split(r'\t', line)[1]).split())
spamLen = len(spamWords)
hamLen = len(hamWords)
pSpam = spamLen/(spamLen+hamLen)
pHam = hamLen/(spamLen+hamLen)
pWiSpam = {}
pWiHam = {}
pWiSpamNonExistant = 1/(spamLen * 2 + hamLen)
pWiHamNonExistant = 1/(hamLen * 2 + spamLen)

for word in spamWords:
    if word in pWiSpam:
        pWiSpam[word] += (1)/(spamLen * 2 + hamLen)
    else:
        pWiSpam[word] = (2)/(spamLen * 2 + hamLen)
for word in hamWords:
    if word in pWiHam:
        pWiHam[word] += (1)/(hamLen * 2 + spamLen)
    else:
        pWiHam[word] = (2)/(hamLen * 2 + spamLen)
    
inputData = []
outputData = []
with open(testFile, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        inputData.append(line)
        words = re.sub(r'[\W+]', ' ', line).split()
        hamProb = pHam
        spamProb = pSpam
        for word in words:
            if word in pWiHam:
                hamProb *= pWiHam[word]
            else:
                hamProb *= pWiHamNonExistant
            if word in pWiSpam:
                spamProb *= pWiSpam[word]
            else:
                spamProb *= pWiSpamNonExistant
        if spamProb > hamProb:
            outputData.append('spam')
        else:
            outputData.append('ham')

with open(outputFile, 'w', encoding='utf-8') as file:
    for i in range(0, len(inputData) - 1):
        file.write(outputData[i] + '\t' + inputData[i])