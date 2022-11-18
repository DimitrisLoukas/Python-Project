#!/usr/bin/env python
# coding: utf-8

# In[157]:


import re
import math
import sys


# In[158]:


class Person:
    def __init__(self,
                 cpr = "",
                 firstName = "",
                 secondName = "",
                 height = 0,
                 weight = 0,
                 eyecolor = "",
                 bloodType = "",
                 children = []):
        
        self.cpr = cpr
        self.firstName = firstName
        self.secondName = secondName
        self.height = height
        self.weight = weight
        self.eyecolor = eyecolor
        self.bloodType = bloodType
        self.children = children


# In[159]:


def Percent(x,total):
    ''' This function calculates the percentage'''# we HAVE TO ADD ERROR HANDLING IF DIVISION BY ZERO!!!!
    result = (x*100)/total
    return round(result, 2)


def Average(inputlist):
    return round(sum(inputlist)/len(inputlist),2)


def Distribution(inputlist, start, end, interval):
    # Initialization
    intervallist = [start]
    counterStart = 0
    counterEnd = 0
       
    # Calculate step
    step = int((end-start)/interval)
    
    # Initialize a list of counters for intermidiate steps
    counterlist = [0]*(step - 2)
    
    # Fill the intermidiate intervals to a list
    for i in range(step):
        intervallist.append(intervallist[i] + interval)
        
    # Counter for first step
    for item in inputlist:
        if int(item) >= intervallist[0] and int(item) <= intervallist[1]:
            counterStart += 1

        # Counter for intermidiate steps   
        elif  int(item) > intervallist[1]:  
            for pos in range(1,len(intervallist)-2):
                if int(item) > intervallist[pos] and int(item) <= intervallist[pos + 1]:
                    counterlist[pos-1] += 1
                    
            # Counter for last step
            if int(item) > intervallist[-2] and int(item) <= intervallist[-1]:
                counterEnd += 1
    
    # Print first interval
    print(f"{intervallist[0]} - {intervallist[1]}:  \t {Percent(counterStart, len(inputlist))}")  
    
    # Print intermidiate intervals
    for pos in range(1, len(intervallist) - 2):
        print(f"{intervallist[pos] + 1} - {intervallist[pos + 1]}:  \t {Percent(counterlist[pos-1], len(inputlist))}")
        
    # Print last interval
    print(f"{intervallist[-2] + 1} - {end}: \t {Percent(counterEnd, len(inputlist))} \n") 

def PossibleBlood(parentBlood):
    if 'A' in parentBlood:
        if 'B' in parentBlood:
            possibletype = {'A','B','AB','O'}
        elif 'O' in parentBlood:
            possibletype = {'A','O'}
        elif 'AB' in parentBlood:
             possibletype = {'A','B','AB'}
        else:
            possibletype = {'A','O'}
    elif 'B' in parentBlood:
        if 'O' in parentBlood:
            possibletype = {'B','O'}
        elif 'AB' in parentBlood:
            possibletype = {'A','B','AB'}
        else:
            possibletype = {'B','0'}
    elif 'O' in parentBlood:
        if 'AB' in parentBlood:
            possibletype = {'A','B'}
        else:
            possibletype = {'O'}
    else:
        possibletype = {'A','B','AB'}
        
    return possibletype
            
    
            


# In[170]:


# Open file
try:
    infile = open('people.db','r')
except IOError as error:
    sys.stdout.write("Can't read file, reason: " + str(error) + "\n")
    sys.exit(1)


# Initialization of data structure and isPerson flag
data = list()
currentPerson = Person()
isPerson = False

for line in infile:
    if line.startswith('CPR'):
        isPerson = True
        
        # Initialize CPR flag
        isCPR = None
        
        # Search for CPR and save it
        isCPR = re.search(r'(\d+\-\d+)', line)
        if isCPR != None:
            CPR = isCPR.group(1)
            currentPerson.cpr = CPR
            continue
             
    if line.startswith("First"):
        # Initialize CPR flag
        isFirstName = None
        
        # Search for CPR and save it
        isFirstName = re.search(r'\:\s(\w+)', line)
        if isFirstName != None:
            firstName = isFirstName.group(1)
            currentPerson.firstName = firstName
            continue
            
    if line.startswith("Last"):
        # Initialize CPR flag
        isSecondName = None
        
        # Search for CPR and save it
        isSecondName = re.search(r'\:\s(\w+)', line)
        if isSecondName != None:
            secondName = isSecondName.group(1)
            currentPerson.secondName = secondName
            continue
            
    if line.startswith("Height"):
        # Initialize CPR flag
        isHeight = None
        
        # Search for CPR and save it
        isHeight = re.search(r'\:\s(\d+)', line)
        if isHeight != None:
            height = isHeight.group(1)
            currentPerson.height = height 
            continue
    
    if line.startswith("Weight"):
        # Initialize CPR flag
        isWeight = None
        
        # Search for CPR and save it
        isWeight = re.search(r'\:\s(\d+)', line)
        if isWeight != None:
            weight = isWeight.group(1)
            currentPerson.weight = weight
            continue
    
    if line.startswith("Eye"):
        # Initialize CPR flag
        iseyeColor = None
        
        # Search for CPR and save it
        isEyeColor = re.search(r'\:\s(\w+)', line)
        if isEyeColor != None:
            eyeColor = isEyeColor.group(1)
            currentPerson.eyeColor = eyeColor
            continue      
    
    if line.startswith("Blood"):
        # Initialize CPR flag
        isbloodType = None
        
        # Search for CPR and save it
        isbloodType = re.search(r'\:\s(\w+(\+|\-)?)', line)
        if isbloodType != None:
            bloodType = isbloodType.group(1)
            currentPerson.bloodType = bloodType
            continue
  
    if line.startswith("Children"):
        # Initialize children flag
        isChildren = None
        
        # Search for children and save it
        isChildren = re.findall(r'(\d+\-\d+)', line)
        if isChildren != None:
            children = isChildren
            currentPerson.children = children
    
    if line == "\n" and isPerson == True:
        data.append(currentPerson)
        currentPerson = Person()
        
# Close file        
infile.close() 


# In[184]:


#Initialization
age = list()
ageFirstFather = list()
ageFirstMother = list()
cprChildren = list()
childWithTwoParents = list()
ageDifference = list()
women = []
men = []
couples = list()

counterMother = 0
counterFather = 0
counterFemale = 0
counterMale = 0
countGrandparent = 0
FirstbornMale = 0
FirstbornFemale = 0
countMoreWomen = 0
countMoreMen = 0

for person in data:
        # Save age to a list
        age.append(100 -int(person.cpr[4:6]))
        
        # Only person with children
        if len(person.children) > 0:
            
            # Find earliest born child    
            minYear = 100 
            firstborn = 100
            
            # find firstborn child
            for birthdate in person.children:
                Month = int(birthdate[2:4])
                
                if int(birthdate[4:6]) == minYear:
                    minMonth = int(firstborn[2:4])
                    
                    if Month < int(minMonth):
                        firstborn = birthdate
                        
                    if Month == minMonth:
                        minDay = int(firstborn[0:2])
                        
                        if int(birthdate[0:2]) < minDay:
                            firstborn = birthdate
                        
                        #we checked for twins and there are no twins
                        '''if int(birthdate[0:2]) == minDay:
                            print('cacca')'''
                
                if int(birthdate[4:6]) < minYear:
                    minYear = int(birthdate[4:6])
                    firstborn = birthdate     
            
            # find gender of firstborn child
            if int(firstborn[-1]) % 2 == 0:
                FirstbornFemale += 1
            else:
                FirstbornMale += 1
                    
            # Count female/male parent
            if (int(person.cpr[-1]) % 2) == 0:
                counterMother += 1
                # Save age of becoming first time MOTHER to a list
                ageFirstMother.append(minYear - int(person.cpr[4:6]))
                
                
                for child in person.children:
                    for father in data:
                        if child in father.children:
                            if int(father.cpr[-1]) % 2 != 0 and father not in men:
                                men.append(father)
                if len(men) > 1:
                    countMoreMen += 1
                    for man in men:
                        if [man, person] not in couples:
                            couples.append([man, person])
                else:
                    if [men[0], person] not in couples:
                        couples.append([men[0], person])

                men = []
                     
            else:
                counterFather += 1
                # Save age of becoming first time FATHER to a list
                ageFirstFather.append(minYear - int(person.cpr[4:6]))
                
                
                for child in person.children:
                # ana alternative could be to create another list with only class of mothers(maybe the loop is faster?)
                    for mother in data:
                        if child in mother.children:
                            if int(mother.cpr[-1]) % 2 == 0 and mother not in women:
                                women.append(mother)
                if len(women) > 1:
                    countMoreWomen += 1
                    for woman in women:
                        if [person, woman] not in couples:
                            couples.append([person, woman])
                else:
                    if [person, women[0]] not in couples:
                        couples.append([person, women[0]])  
                women = []
                
                
            # Find common parent for children
            for cprnumber in person.children:
                if cprnumber in cprChildren:
                    childWithTwoParents.append(cprnumber)
                cprChildren.append(cprnumber)
            
        else:
            # Count people who don't have children
            if (int(person.cpr[-1]) % 2) == 0:
                counterFemale += 1
            else:
                counterMale += 1
                   
                
                

# we must re-do this with couples[]
# Calculate the age difference between parents
for cprnumber in childWithTwoParents:
    temp = 0
    for person in data:
        for cprchildren in person.children:
            if cprchildren == cprnumber:
                temp = abs(100 -int(person.cpr[4:6]) - temp)
    ageDifference.append(temp)

# Count people with at least one grandparent    
for cprnumber in cprChildren:
    for person in data:
        # se un figlio è presente anche come persona in cpr
        if person.cpr == cprnumber and len(person.children) > 0:
                countGrandparent += 1



# Do tall people marry (or at least get children together)?
# Do fat people marry or at least get children together? (limits for obesity  taken from: https://en.wikipedia.org/wiki/Classification_of_obesity)

(counterTT, counterTN, counterTS, counterNN, counterNS, counterSS) = (0, 0, 0, 0, 0 ,0)
(counterFF, counterFN, counterFU, counterNwNw, counterNU, counterUU) = (0, 0, 0, 0, 0 ,0)
flagTallSons = False
counterTallSon = 0
nonBiological = list()

for couple in couples:# check if transforming to a set makes the iteration quicker.
    # couple(male, female)
    heightEval = list()
    tallParents = list()
    fatEval = list()
    bloodParents = list()  
    
    
    for parent in couple:
        
        # save blood type of the couple temporarely
        bloodParents.append(parent.bloodType.replace('+','').replace('-',''))
        possibleBloodType = PossibleBlood(bloodParents)
    
        
        # Height couple evaluation
        if int(parent.height) <= 150:
            heightEval.append("short")   
        elif (int(parent.height) >150 and int(parent.height) <= 180):
            heightEval.append('normal')
        elif int(parent.height) > 180:
            heightEval.append('tall')
            tallParents.append(parent)
        
        # weight couple evaluation
        BMI = int(parent.weight)/((int(parent.height)/100)**2)
        
        if BMI <= 18.5:
            fatEval.append('underweight')
        if BMI > 18.5 and BMI <= 25:
            fatEval.append('normal weight')
        if BMI > 25:
            fatEval.append('fat')

            
    # evaluate blood type of children given the parents: search for non-biological sons
    for biologicalSon in couple[0].children:
        for son in data:
            if biologicalSon == son.cpr:
                if son.bloodType.replace('+','').replace('-','') not in possibleBloodType:
                    nonBiological.append(son.cpr)
                    print(son.bloodType.replace('+','').replace('-',''), possibleBloodType,bloodParents)
                
            
    # Do tall parents get tall children? Tall/tall couples who also have tall children        
    if len(tallParents) == 2:
        Tallchildren = tallParents[0].children 
        
        for child in Tallchildren:
            for person in data:
                if child == person.cpr:
                    if int(person.height) > 180:
                        flagTallSons = True
            if flagTallSons:
                counterTallSon += 1
                break
                
    # count couples based on height   
    if "tall" in heightEval:
        
        if "normal" in heightEval:
            counterTN += 1
        elif "short" in heightEval:
            counterTS += 1
        else:
            counterTT += 1
    
    elif "normal" in heightEval:
        
        if "short" in heightEval:
            counterNS += 1
        else:
            counterNN += 1
            
    else:
        counterSS += 1
     
    # count couples based on BMI
    if 'fat' in fatEval:
        
        if "normal weight" in fatEval:
            counterFN += 1
        elif "underweight" in fatEval:
            counterFU += 1
        else:
            counterFF += 1
    
    elif "normal weight" in fatEval:
        
        if "underweight" in fatEval:
            counterNU += 1
        else:
            counterNwNw += 1
            
    else:
        counterUU += 1
        
print(counterTallSon, counterTT)
     


# In[185]:


# Calculate age distribution
print("\033[4m"'\033[1m' "AGE DISTRIBUTION" '\033[0m')
print('\033[1m' "Age(Years)", "\t","Percentage(%)" '\033[0m')
Distribution(age, 0, 100, 10)


# Calculate gender distribution for parents
print("\033[4m"'\033[1m' "GENDER DISTRIBUTION FOR PARENTS" '\033[0m')

print('\033[1m' "Gender", "Percentage(%)" '\033[0m', sep = "\t\t")
print("Male", Percent(counterMother,len(age)), sep = "\t\t")
print("Female", Percent(counterFather,len(age)),"\n", sep = "\t\t") 

# Distribution of age for first MOTHER
print("\033[4m"'\033[1m' "FIRST TIME MOTHER" '\033[0m')
print('\033[1m' "Age(Years)", "Percentage(%)" '\033[0m', sep = "\t")
Distribution(ageFirstMother, 0 ,100 , 10)

# Min Max Average of age for first time MOTHERS
print('\033[1m' "Average(Years):" '\033[0m', round(Average(ageFirstMother), 2), sep = "\t")
print('\033[1m' "Maximum(Years):" '\033[0m', max(ageFirstMother), sep = "\t")
print('\033[1m' "Minimum(Years):" '\033[0m', min(ageFirstMother), "\n", sep = "\t")


# Distribution of age for first FATHER
print("\033[4m"'\033[1m' "FIRST TIME FATHER" '\033[0m')
print('\033[1m' "Age(Years)", "Percentage(%)" '\033[0m', sep = "\t")
Distribution(ageFirstFather, 0 ,100 , 10)

# Min Max Average of age for first time FATHERS
print('\033[1m' "Average(Years):" '\033[0m', round(Average(ageFirstFather), 2), sep = "\t")
print('\033[1m' "Maximum(Years):" '\033[0m', max(ageFirstFather), sep = "\t")
print('\033[1m' "Minimum(Years):" '\033[0m', min(ageFirstFather), "\n", sep = "\t")


# Percentage of MEN/WOMAN without children
print("\033[4m"'\033[1m' "MEN/WOMEN WITHOUT CHILDREN" '\033[0m')
print('\033[1m' "Gender", "Percentage(%)"'\033[0m', sep = "\t\t")
print("Male", Percent(counterFemale,len(age)), sep = "\t\t")
print("Female", Percent(counterMale,len(age)), "\n", sep = "\t\t") 
# counterFemale and counterMale are quite misleading names, they don't describe that these people don't have children.

# Average age difference between parents
print("\033[4m"'\033[1m' f"Average age difference between parents(Years)\033[0m:   {Average(ageDifference)}\n")

# People with at least one grandparent that is still alive
print("\033[4m"'\033[1m' "People with at least one grandparent that is still alive" '\033[0m')
print("Count:", countGrandparent, sep = "\t\t")
print("Percentage(%):", Percent(countGrandparent,len(age)), "\n",sep = "\t\t")

# Is the firstborn child likely to be male or female?
print("\033[4m"'\033[1m' "FIRSTBORN GENDER DISTRIBUTION" '\033[0m')
print('\033[1m' "Gender", "Percentage(%)"'\033[0m', sep = "\t\t")
peopleWithChildren = counterMother + counterFather
print("Male", Percent(FirstbornMale,peopleWithChildren), sep = "\t\t")
print("Female", Percent(FirstbornFemale,peopleWithChildren), "\n", sep = "\t\t") 

# How many men/women have children with more than one women/men?
print("\033[4m"'\033[1m' "MEN/WOMEN WITH CHILDREN WITH MORE THAN ONE WOMEN/MEN" '\033[0m')
print('\033[1m' "Gender", "Percentage(%)"'\033[0m', sep = "\t\t")
print("Men", Percent(countMoreWomen,(counterMother + counterFemale)), sep = "\t\t")
print("Women", Percent(countMoreMen,(counterFather + counterMale)),'\n', sep = "\t\t") 

# Do tall people(couples) marry?
print("\033[4m"'\033[1m' "COUPLES HEIGHT DISTRIBUTION" '\033[0m')
print('\033[1m' "Heights", "Percentage(%)"'\033[0m', sep = "\t\t")
print("Tall/Tall", Percent(counterTT,len(couples)), sep = "\t\t")
print("Tall/Normal", Percent(counterTN,len(couples)), sep = "\t\t")
print("Tall/Short", Percent(counterTS,len(couples)), sep = "\t\t")
print("Normal/Normal", Percent(counterNN,len(couples)), sep = "\t\t")
print("Normal/Short", Percent(counterNS,len(couples)), sep = "\t\t")
print("Short/Short", Percent(counterSS,len(couples)), "\n", sep = "\t\t")

# Do tall parents get tall children?
print("The", Percent(counterTallSon,counterTT),"% of couples over the total amount of tall/tall couples get at least one tall child.\n")

# Do fat people marry?
print("\033[4m"'\033[1m' "COUPLES WEIGHT DISTRIBUTION" '\033[0m')
print('\033[1m' "Weights", "Percentage(%)"'\033[0m', sep = "\t\t\t\t\t\t")
print("Overweight-obese/Overweight-obese", Percent(counterFF,len(couples)), sep = "\t\t")
print("Overweight-obese/Normal weight   ", Percent(counterFN,len(couples)), sep = "\t\t")
print("Overweight-obese/Underweight     ", Percent(counterFU,len(couples)), sep = "\t\t")
print("Normal weight/Normal weight      ", Percent(counterNwNw,len(couples)), sep = "\t\t")
print("Normal weight/Underweight        ", Percent(counterNU,len(couples)), sep = "\t\t")
print("Underweight/Underweight          ", Percent(counterUU,len(couples)), "\n", sep = "\t\t")

# Are there any non biological sons/daughters?
print("There are {0} non-biological sons/daughters.".format(len(nonBiological)),"\nThey correspond to these cpr numbers:",nonBiological, "\n")


# In[173]:


for person in data:
    if person.cpr == '030629-9882':
        print(person.bloodType)


# In[ ]:



