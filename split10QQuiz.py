"""
This program reads in all of the questions in a GIFT file and randomizes them
The user then selects how many quizzes to make and which
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

    fpIn = open(inFile, "r")
    nQuest = 0
    mc = readMC(fpIn)

# Read questions
    while mc != None:
        mcArray.append(mc)
        #print "Reading question %d" % (nQuest+1)
        nQuest += 1
        mc = readMC(fpIn)
    fpIn.close()

# get number of quizzes
    done = False
    while not done:
        nQuiz = input("There are %d question, how many quizzes do you want? " \
                      % (nQuest))
        nQuestQuiz = input("How many questions on each quiz? ")
        if nQuiz > 0 and nQuestQuiz > 0 and nQuestQuiz * nQuiz <= nQuest:
            done = True

    # shuffle questions
    random.shuffle(mcArray)

    outFileBase = raw_input("Enter output text file base name: ")
# loop over quizzes
    for iQz in range(nQuiz):
        outFile = "%s-%d.txt" % (outFileBase, iQz)
        fpOut = open(outFile, "w")

        iIF_AT = input("Enter IF AT Key number (9 - 16, 0=all a's):")
        right = IF_AT10[iIF_AT]
#
        print "main: iQz = %d, nQuesQuiz = %d" % (iQz, nQuestQuiz)
        for iQuest in range(nQuestQuiz):
            # print "main: i=%d, right[%d]=>%s<" % (i, i, right[iQuest])
            mcArray[iQuest + iQz * nQuestQuiz].randomize(right[iQuest])
            outStr = "%d) %s\n" % (iQuest+1, mcArray[iQuest + iQz * nQuestQuiz].makeMC())
            fpOut.write(outStr)

        print iIF_AT
        fpOut.write("Form %s; Seed %d\n" % (formName[iIF_AT], iSeed))
        fpOut.close()

main()
