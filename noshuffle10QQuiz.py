"""
This program reads in all of the questions in a GIFT file and keeps them
in order.
The user then selects which
answer key
"""
from QuestionMC import *
import random
iSeed = 1

# I have forms D009, 10, 11, and 16
IF_AT10 = {0: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
           9: "bacdbdbbca",
           10: "bbcababbcc",
           11: "dbdbddcbcd",
           12: "aadcadbbaa",
           13: "cbccbaadab",
           14: "ddbadbacab",
           15: "adacaddcab",
           16: "dbbaddbada",
           }

formName = {0: "test",
            9: "D009",
            10: "D010",
            11: "D011",
            12: "D012",
            13: "D013",
            14: "D014",
            15: "D015",
            16: "D016",
            }

def main():
    # the array of questions
    mcArray = []
    iSeed = input("Enter iSeed: ")
    random.seed(iSeed)
    # the answers on the IF AT cards
    inFile = raw_input("Enter input GIFT file: ")
    outFile = raw_input("Enter output text file: ")
    iIF_AT = input("Enter IF AT Key number (9 - 16, 0=all a's):")

    fpIn = open(inFile, "r")
    fpOut = open(outFile, "w")
    nQuest = 0
    right = IF_AT10[iIF_AT]
    mc = readMC(fpIn)
    while mc != None:
        mcArray.append(mc)
        print "Reading question %d" % (nQuest+1)
        nQuest += 1
        mc = readMC(fpIn)

    done = False
    while not done:
        nQuiz = input("There are %d question, how many do you want on the quiz? " %
                  (nQuest))
        if nQuiz > 0 and nQuiz <= nQuest:
            done = True

    print "main: len(mcArray)=%d" %(len(mcArray))
    print "main: nQz = %d, nQues = %d" % (nQuiz, nQuest)
    # Don's shuffle
    #random.shuffle(mcArray)
    for i in range(nQuiz):
        # print "main: i=%d, right[%d]=>%s<" % (i, i, right[i])
        mcArray[i].randomize(right[i])
        outStr = "%d) %s\n" % (i+1, mcArray[i].makeMC())
        fpOut.write(outStr)

    print iIF_AT
    fpOut.write("Form %s; Seed %d\n" % (formName[iIF_AT], iSeed))
    fpIn.close()
    fpOut.close()
    print "There were %d questions in the file" % (nQuiz)

main()
