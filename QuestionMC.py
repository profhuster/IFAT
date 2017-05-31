"""
QuestionMC.py
ProfHuster at gmail dot com
2017-05-25
v0: documentation modified from 2014 version.

This module defines a class QuestionMC that encapsulizes multiple choice
questions. It will randomize the answers and convert them to a printable
string suitable for inserting into a document.

The module also contains a helper function readMC that reads multiple choice
questions in the GIFT format. The GIFT format is used in the ope source Moodle
course management system.

There is also a test script that needs a file testQ.txt in GIFT format to run.
"""
import string
import random
import copy

class QuestionMC(object):
    """
    QuestionMC is a class for encapsulating multiple choice questions
    
    Args:
        question (str): The stem of the question. Ex. "2 + 3 ="
        rightAns (str): The correct choice. Ex. "5"
        distractors (list of str): The false answers as a list. Note that the
          number of choices is 1 + the umber of distractors
          
    Attributes:
        question (str): see above
        rightAns (str): see above
        distractors (list): see above
        answers (list): all possible answers
        iRight (int): choice of the correct answer. See __choices
        
    Class Attributes:
        __choices (str): a list of answer choices. Initially "abcd...z"
        
    Methods:
        makeMC: returns question in printable form
        randomize: randomly scrambles answers
    """
    __choices = "abcdefghijklmonpqrstuvwxyz"    
    """ alphabetical choices, change to "12345..." for numerical ones
    """
    
    def __init__(self, question, rightAns, distractors):
        self.question = question
        self.rightAns = rightAns
        self.distractors = distractors
        self.answers = [rightAns]
        self.answers.extend(distractors)
        self.iRight = QuestionMC.__choices[0]

    def __str__(self):
        # outputs the question in GIFT format
        str = self.question + '{\n'
        str += "=" + self.rightAns + '\n'
        for a in self.distractors:
            str += "~" + a + '\n'
        str += '}\n'
        return str

    def makeMC(self):
        """ return a string of the question in printable form
        
        Format:
            question\n
            '    '+choice+') '+answer
            for each answer
        """
        str = self.question + '\n'
        for i in range(len(self.answers)):
            str += '    ' + self.__choices[i] + ') ' + self.answers[i] + '\n'
        return str

    def randomize(self, iRight=None):
        """ randomizes the order of the answers. Modifies object.
        """
        # iRight is the position the correct answer should appear in
        if iRight == None:
            iRight = self.__choices[random.randint(0,len(self.answers)-1)]
        elif self.__choices.find(iRight) >= len(self.answers):
            iRight = self.__choices[len(self.answers)-1]
        self.iRight = iRight
        # print "iRight = ", iRight
        self.answers = copy.copy(self.distractors)
        random.shuffle(self.answers)
        self.answers.insert(self.__choices.find(iRight), self.rightAns)

def readMC(fpGIFT):
    """ Reads GIFT files and returns next question as a QuestionMC object
    
    Args:
        fpGIFT (file): file pointer to an open file of GIFT format questions
        
    Returns:
        QuestionMC instance, or None if read failed
    
    Notes:
    - This implementation does not handle errors gracefully
    - empty lines are skipped
    - comment lines begin with '//'
    - the correcct answer line starts with '='
    - distractor lines start with '~'
    """
    # reads a GIFT multiple choice question from an open file.
    # First skip comments and blank lines
    #print "readMC:"
    done = False
    while not done:
        line = fpGIFT.readline()
        if len(line) == 0:
            return None
        line = line.strip()
        #print ">%s<" % line
        if len(line) != 0 and line[0] != '/' and line[1] != '/':
            done = True

    # Aggregate the question
    q = copy.copy(line)
    while q.find('{') < 0:
        # get next line
        line = fpGIFT.readline()
        if len(line) == 0:
            return None
        line = line.strip()
        q = string.join([q, line])
    q = q.strip(' {')
    #print "q=>%s<" % q

    # read the answers
    a = []
    done = False
    while not done:
        line = fpGIFT.readline()
        if len(line) == 0:
            return None
        line = line.strip()
        if line.find('}') >= 0:
            done = True
        #print ">%s<" % line
        #print "line.find('=') = %d" % line.find('=')
        if line.find('=') >= 0:
            rightAns = string.replace(line,'=','')
            #print "rightAns=>%s<" % rightAns
        elif line.find('~') >= 0:
            a.append(string.replace(line,'~',''))
            #print "a=", a
    qMC = QuestionMC(q, rightAns, a)
    return qMC
    

if __name__ == '__main__':
    random.seed(2)
    q1 = QuestionMC("What is 2 + 3?", "5",["2","4","6"])
    print q1
    print q1.randomize()
    print q1.makeMC()
    print q1.randomize()
    print q1.makeMC()
    fp = open("testQ.txt","r")
    quiz = []
    nQuest = 0
    a = readMC(fp)
    while a != None:
        nQuest += 1
        quiz.append(a)
        quiz[nQuest-1].randomize()
        print "===========\nQuestion %2d\n%s" % \
              (nQuest, quiz[nQuest-1].makeMC())
        a = readMC(fp)

# EOF
