#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import math
import sys


# In[2]:


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


# In[26]:


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


def PossibleDonor(relativeBlood):
    if relativeBlood == "O-":
        possibleRecipient = {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"}
    elif relativeBlood == "O+":
        possibleRecipient = {"O+", "A+", "B+", "AB+"}
    elif relativeBlood == "A-":
        possibleRecipient = {"A-", "A+", "AB-", "AB+"}
    elif relativeBlood == "A+":
        possibleRecipient = {"A+", "AB+"}
    elif relativeBlood == "B-":
        possibleRecipient = {"B-", "B+", "AB-", "AB+"}
    elif relativeBlood == "B+":
        possibleRecipient = {"B+", "AB+"}
    elif relativeBlood == "AB-":
        possibleRecipient = {"AB-", "AB+"}
    else:
        possibleRecipient = {"AB+"}
        
    return possibleRecipient


# In[4]:


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


# In[91]:


#Initialization

# Age of every person
age = list()
# Age of a male first time becoming a father
ageFirstFather = list()
# Age of a female first time becoming a mother
ageFirstMother = list()
# CPR of every children, no duplicates
cprChildren = list()
# Age difference between parents
ageDifferenceParents = list()
# Temporary list used to calculate men who had children with more than on woman
women = []
# Temporary list used to calculate women who had children with more than on man
men = []
# couple[0] = male and couple[1] = female, list of classes
couples = list()
# Count how many mothers
counterMother = 0
# Count how many fathers
counterFather = 0
# Count how many females in data who dont have children
counterFemale = 0
# Count how many males in data who dont have children
counterMale = 0
# Count how many children have at least one grandparent
countGrandparent = 0
# Count how many firstborn children are male
FirstbornMale = 0
# Count how many firstborn children are female
FirstbornFemale = 0
# Count how many 
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
                            couples.append([person, mother])
                else:
                    if [person, women[0]] not in couples:
                        couples.append([person, women[0]])  
                women = []
            
            # Save cpr for each child no duplicates
            for cprnumber in person.children:
                if cprnumber not in cprChildren:
                    cprChildren.append(cprnumber)
                    
            
        else:
            # Count people who don't have children
            if (int(person.cpr[-1]) % 2) == 0:
                counterFemale += 1
            else:
                counterMale += 1
                
                
                
                
# Calculate the age difference between parents                
for couple in couples:
    male = couple[0]
    female = couple[1]
    ageDifferenceParents.append(abs(int(male.cpr[4:6]) - int(female.cpr[4:6])))
    

# Count people with at least one grandparent    
for cprnumber in cprChildren:
    for person in data:
        # se un figlio è presente anche come persona in cpr
        if person.cpr == cprnumber and len(person.children) > 0:
                countGrandparent += 1



# Do tall people marry (or at least get children together)?
tall = 0
short = 0
normal = 0
(counterTT, counterTN, counterTS, counterNN, counterNS, counterSS) = (0, 0, 0, 0, 0 ,0)

for couple in couples:# check if transforming to a set makes the iteration quicker.
    # couple(male, female)
    heightEval = list()
    
    for parent in couple:
        if int(parent.height) <= 150:
            heightEval.append("short")   
        elif (int(parent.height) >150 and int(parent.height) <= 180):
            heightEval.append('normal')
        elif int(parent.height) > 180:
            heightEval.append('tall')
            
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



cprChildrenList = list()
for person in data:
    # If person has children
    if len(person.children) > 0:
        # Save list of children
        cprChildrenList.append(person.children)

# Initialize list of cousins
cousinNumber = list()


for children in cprChildrenList:
    t = list()
    for child in children:
        # For every person
        for person in data:
            # If person has children
            if len(person.children) > 0:
                # If child has children
                if child == person.cpr:
                    # Save how many children a child has
                    t.append(len(person.children))

    # If number of children of a child is more than 2              
    if len(t) >= 2:
        cousinNumber.append(t)
        
# Average cousin per child
print(Average([Average(i) for i in cousinNumber]))

# 16 and 17 Task
# Key = father cpr, value = son(s) cpr and common blood type, dictionary of fathers/sons/bloodtype that can donate blood to their sons
FatherSonDonateBlood = [[0]]
# Key = grandparent cpr, value = grandchild cpr and common blood type, dictionary of grandparent/grandchild/bloodtype
grandparent = [[0]]
# Number of sons that their father can doate blood to them
counterSon = 0
# Number of grandchildren that their grandparent can doate blood to them
counterGrandparents = 0
# just list of fathers
k = list()
# couples = (object male,object female)
for couple in couples:
    temp = list()
    
    male = couple[0]
    female = couple[1]
    #print(male.bloodType, male.cpr)
    bloodTypeMale = male.bloodType
    bloodTypeFemale = female.bloodType
    
    # 1st generation
    for child in (male.children):
        for person in data:
            # If person is the child
            if child == person.cpr and (int(person.cpr[-1]) % 2 != 0):
                # Compare fathers and sons bloodtype
                if person.bloodType in PossibleDonor(bloodTypeMale):
#                     k.append(male.cpr)   just list of fathers
                    if male.cpr not in FatherSonDonateBlood[-1]:
                        FatherSonDonateBlood.append([male.cpr, male.bloodType, person.cpr, person.bloodType])
                        counterSon += 1
                    else:
                        FatherSonDonateBlood[-1].append(person.cpr)
                        FatherSonDonateBlood[-1].append(person.bloodType)
                        counterSon += 1
                        
                    
                
                #If 1st generation person has children (2nd generation)
                if len(person.children) > 0:
                    for personsChild in person.children:
                        for person2 in data:
                            
                            temp2 = list()
                            # personsChild = grandchild
                            if (person2.cpr == personsChild):
                               # print(person2.cpr, person.cpr, parent.cpr)
                                for parent in couple:
                                    # Male grandparent
                                    if parent.bloodType in PossibleDonor(person2.bloodType):
                                        
                                        if person2.cpr not in grandparent[-1]:
                                            grandparent.append([person2.cpr, person2.bloodType, parent.cpr, parent.bloodType])
                                            counterGrandparents +=1


                                    
                        
                
FatherSonDonateBlood.pop(0)               
grandparent.pop(0)           


# In[92]:


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
print("\033[4m"'\033[1m' f"Average age difference between parents(Years)\033[0m:   {Average(ageDifferenceParents)}\n")

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

# Fathers who can donate blood to their sons
print("\033[4m"'\033[1m' "FATHERS WHO CAN DONATE BLOOD TO THEIR SONS" '\033[0m')
print('\033[1m' "Number of fathers:"'\033[0m', len(FatherSonDonateBlood), sep = "\t")
print('\033[1m' "Number of sons:"'\033[0m', counterSon, sep = "\t\t")

# Grandparents who can donate blood to their grandchild
print("\033[4m"'\033[1m' "GRADPARENTS WHO CAN DONATE BLOOD TO THEIR GRANDCHILD" '\033[0m')
print('\033[1m' "Number of fathers:"'\033[0m', len(grandparent), sep = "\t")
print('\033[1m' "Number of sons:"'\033[0m', counterGrandparents, sep = "\t\t")

