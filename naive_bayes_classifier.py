import sys
import csv

'''Naive Bayes Classifier'''
'''
Assumptions: 1. Missing Data is considered as OTHER data and is counted similar to existing data
2. If a variable is not encountered before then lapalace smoothing is used, which is P[unknown data] = 1/(count + size + 1)

No datapoint is ignored throught the dataset.

In the output, first value is the probability that the mushroom is poisonous and second value is the probability that the mushroom is edible.
Mushroom is classified based the value which has higher probabilty.
Final line is the accuracy of the classifier.

For running the code use the following command:
python naive_bayes_classifier.py <trainfile> <testfile>

The angular brackets <> should be rplaces with the respective values.
Python 2.7.12 is used.
'''

trainfile = sys.argv[1]
testfile = sys.argv[2]

train = open(trainfile,"r")
trainreader = csv.reader(train)
test = open(testfile,"r")
testreader = csv.reader(test)

global poisonous, edible, poisonuscount, ediblecount, totalcount, c
poisonous = [{} for i in range(22)]
edible = [{} for i in range(22)]
poisonouscount = 0
ediblecount = 0
totalcount = 0
c = 0
print 'Probabilty that it is Poisonous', 'Probability that it is edible'

def computeCounts(row):
    global poisonouscount, ediblecount, totalcount, poisonous, edible
    totalcount += 1
    if row[0] == 'p':
        poisonouscount += 1
        for i in range(22):
            if row[i+1] in poisonous[i]:
                poisonous[i][row[i+1]] += 1
            else:
                poisonous[i][row[i+1]] = 1
    else:
        ediblecount += 1
        for i in range(22):
            if row[i+1] in edible[i]:
                edible[i][row[i+1]] += 1
            else:
                edible[i][row[i+1]] = 1

def classify(row,poisonousprob,edibleprob):
    global poisonous, edible, poisonuscount, ediblecount
    pclassify = 1
    eclassify = 1
    for i in range(22):
        if row[i] in poisonous[i]:
            pclassify *= poisonous[i][row[i]]
        else:
            pclassify *= 1/float(len(poisonous[i])+poisonouscount+1)
        if row[i] in edible[i]:
            eclassify *= edible[i][row[i]]
        else:
            eclassify *= 1/float(len(edible[i])+ediblecount+1)

    pclassify *= poisonousprob
    eclassify *= edibleprob
    alpha = 1/float(pclassify+eclassify)

    pclassify /= alpha
    eclassify /= alpha

    print pclassify,eclassify
    if pclassify > eclassify:
        return 'p'
    else:
        return 'e'

for row in trainreader:
    computeCounts(row)

for i in range(22):
    for key in poisonous[i]:
        poisonous[i][key] /= float(poisonouscount)

    for key in edible[i]:
        edible[i][key] /= float(ediblecount)

poisonousprob = poisonouscount/float(totalcount)
edibleprob = ediblecount/float(totalcount)

correct = 0
testcount = 0
for row in testreader:
    testcount += 1
    h = classify(row[1:],poisonousprob,edibleprob)

    if(h == row[0]):
        correct += 1

print "Accuracy of predictions for test set:", (correct/float(testcount))*100,'%'
