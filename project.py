# LIBRARIES

import re



# CLASS

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



# FUNCTIONS

def Percent(x,total):
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



# OPENNING/READING

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
        isbloodType = re.search(r'\:\s(\w(\+|\-)?)', line)
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



# PROCESSING

#Initialization
age = list()
ageFirstFather = list()
ageFirstMother = list()
cprChildren = list()
childWithTwoParents = list()
ageDifference = list()

counterMother = 0
counterFather = 0
counterFemale = 0
counterMale = 0
countGrandparent = 0

for person in data:
        # Save age to a list
        age.append(100 -int(person.cpr[4:6]))
        
        # Only person with children
        if len(person.children) > 0:
            
            # Find earliest born child    
            minYear = 100 
            for birthdate in person.children:
                if int(birthdate[4:6]) < minYear:
                    minYear = int(birthdate[4:6])
            
            
            # Count female/male parent
            if (int(person.cpr[-1]) % 2) == 0:
                counterMother += 1
                # Save age of becoming first time MOTHER to a list
                ageFirstMother.append(minYear - int(person.cpr[4:6]))
            else:
                counterFather += 1
                # Save age of becoming first time FATHER to a list
                ageFirstFather.append(minYear - int(person.cpr[4:6]))
                
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
        if person.cpr == cprnumber:
            if len(person.children) > 0:
                countGrandparent += 1



# OUTPUT

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


# Average age difference between parents
print("\033[4m"'\033[1m' f"Average age difference between parents(Years)\033[0m:   {Average(ageDifference)}\n")

# People with at least one grandparent that is still alive
print("\033[4m"'\033[1m' "People with at least one grandparent that is still alive" '\033[0m')
print("Count:", countGrandparent, sep = "\t\t")
print("Percentage(%):", Percent(countGrandparent,len(age)), sep = "\t\t")