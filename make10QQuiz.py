"""make10QQuiz.py
profhuster at gmail dot com
2017-05-25

This program reads in all of the questions in a GIFT format text file and 
randomizes them. The user then selects how many questions to produce in the 
quiz and which answer key
"""
from glob import glob
from os.path import isfile
from QuestionMC import readMC
import random
iSeed = 1

inFileFormat = "*GIFT*.txt"

"""
dict: IF_AT10 - dictionary of 10 question answer keys
"""
IF_AT10 = {"test (all a's)": "aaaaaaaaaa",
           "D009": "bacdbdbbca",
           "D010": "bbcababbcc",
           "D011": "dbdbddcbcd",
           "D012": "aadcadbbaa",
           "D013": "cbccbaadab",
           "D014": "ddbadbacab",
           "D015": "adacaddcab",
           "D016": "dbbaddbada",
	   "D025": "cacbadbcdd",
	   "D026": "dabccacbdb",
	   "D027": "bacabdbacd",
	   "D028": "addcdabdbc",
	   "D029": "cacbaadcdb",
	   "D030": "abcbddacdd", 
	   "D031": "bdbcdabcda",
	   "D031": "cacdbdbcad",
           }

def main():
    # the array of questions
    mcArray = []
    iSeed = input("Enter iSeed: ")
    random.seed(iSeed)
    
    # Get input files
    done = False
    while not done:
        try:
            print(
              "Input files must have 'GIFT' in the name, and end with '.txt'")
            inFiles = glob(inFileFormat)
            for (iIn, inFile) in enumerate(inFiles):
                print("{} - {}".format(iIn, inFile))
            iIn = int(raw_input("Enter # of input file to use: "))
            fpIn = open(inFiles[iIn], "r")
            done = True
        except (ValueError, IndexError):
            print("Bad choice")
    
    # Get output file
    print("Output files will have '.txt' append to their base name.")
    done = False
    while not done:
        outFile = raw_input("Enter output file base name: ")
        if not outFile.endswith(".txt"):
            outFile += ".txt"
        if isfile(outFile):
            ans = raw_input("{} exists. Overwrite (Y/n):".format(outFile))
            if len(ans) == 0:
                fpOut = open(outFile, "w")
                done = True
                break
            if ans.capitalize()[0] == 'Y':
                fpOut = open(outFile, "w")
                done = True
            else:
                print("Try again")
        else:
            fpOut = open(outFile, "w")
            done = True
    
    done = False
    while not done:
        try:
            cards = IF_AT10.keys()
            cards.sort()
            for (iCard,card) in enumerate(cards):
                print("{} - {}".format(iCard, card))     
            iCard = int(raw_input("Enter IFAT Card #: "))
            thisKey = cards[iCard]
            print("Answers for  key {} are {}".format(thisKey,IF_AT10[thisKey]))
            done = True
        except (IndexError, ValueError):
            print("\n## Try again ##")

    nQuest = 0
    right = IF_AT10[thisKey]
    mc = readMC(fpIn)
    while mc != None:
        mcArray.append(mc)
        print ".",
        nQuest += 1
        mc = readMC(fpIn)
    print("")

    done = False
    while not done:
        nQuiz = input("There are %d question, how many do you want on the quiz? " %
                  (nQuest))
        if nQuiz > 0 and nQuiz <= nQuest:
            done = True

    print "main: len(mcArray)=%d" %(len(mcArray))
    print "main: nQz = %d, nQues = %d" % (nQuiz, nQuest)
    random.shuffle(mcArray)
    for i in range(nQuiz):
        # print "main: i=%d, right[%d]=>%s<" % (i, i, right[i])
        mcArray[i].randomize(right[i])
        outStr = "%d) %s\n" % (i+1, mcArray[i].makeMC())
        fpOut.write(outStr)

    print thisKey
    fpOut.write("Form %s; Seed %d\n" % (thisKey, iSeed))
    fpIn.close()
    fpOut.close()
    print "There were %d questions in the file" % (nQuiz)

main()
