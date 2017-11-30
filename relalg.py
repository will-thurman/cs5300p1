import itertools

def nest_AND(counter, tree, sentence, table):
    answer = counter
    skip = 'no'
    temp5 = []
    counter = counter - 1
    
    while skip != 'yes':
        if sentence[counter] == 'AND':
            table.append(temp5)
            sentence.pop()                   #get rid of AND

            counter = counter - 1
            if counter == 0:
                skip = 'yes'
        else:

            temp5.append(sentence.pop(counter))
            if counter == 0:
                skip = 'yes'
            else:
                counter = counter - 1


def WHERE(counter, tree, sentence, table):
    sentence.pop()                      #get rid of WHERE
    key = 'END'
    counter = counter - 1
    temp4 = []
     
    table = list(itertools.chain.from_iterable(table))

    skip = 'no'
    
    while skip == 'no':
        if sentence[counter] == 'AND':
            table.append(temp4)
            sentence.pop()                   #get rid of AND  
            counter2 = nest_AND(counter, tree, sentence, table)
            counter = counter2
        else:
            temp4.append(sentence.pop(counter))
            counter = counter - 1
            
        if counter == None:
            skip = 'yes'   

    
def nest_AS(counter, tree, sentence, table):
    key = 'WHERE'
    temp3 = []
    counter = counter - 1
    skip = 'no'

    while sentence[counter] != key or skip == 'no':
        if sentence[counter] == 'AS':
            table.append(temp3)
            sentence.pop()                   #get rid of AS
            counter = counter - 1
        else:
            temp3.append(sentence.pop(counter))
            counter = counter - 1

        if sentence[counter] == 'WHERE':
            skip = 'yes' 
    return counter
    
def FROM(counter, tree, sentence, table):
    key = 'WHERE'
    temp2 = []
    counter = counter - 1
    skip = 'no'
    
    while sentence[counter] != key or skip == 'no':
        if sentence[counter] == 'AS':
            table.append(temp2)
            sentence.pop()              #get rid of AS
            counter2 = nest_AS(counter, tree, sentence, table)    #call nested AS function
            counter = counter2                  #correcting counter due to nested AS function
        else:
            temp2.append(sentence.pop(counter))   #saves info if there is no nested AS
            counter = counter - 1

        if sentence[counter] == 'WHERE':
            skip = 'yes'
            
    WHERE(counter, tree, sentence, table)     #calls next checkpoint function WHERE
    
def SELECT(tree, sentence, table):
    #tree = []           #list for relational tree later on
    
    counter = len(sentence) - 1
    key = 'FROM'
    temp1 = []   #temporary list to store info

    while sentence[counter] != key:
        temp1.append(sentence.pop(counter))
        counter = counter - 1
		
    project = u'\u03A0'    #print unicode for PI
    #select = u'\u03C3' #print unicode for Sigma
    
    print(project,temp1,'(')
    
    tree.append(project)    #save output to tree list (will need to include list in othr functions
    tree.append('(')
    table = temp1
    #print('tree list : ', tree)
    #print('need to append the end )')
    
    sentence.pop()              #get rid of FROM
    FROM(counter, tree, sentence, table)

    
#def qury_print(sentence, tree, table):



    
def read_split():
    tree = []           #list for relational tree later on
    sentence = []       #input from user 
    table = []          #index table for
    
    line = open('test.txt')            #set up list for query 
    for word in line.read().split():
        sentence.append(word)

    x = len(sentence)
    sentence.reverse()         #reverse sentence for proper stack operations
        
    sentence.pop()              #fix for the weird select issue (no more odd symbols)
    sentence.append('SELECT')
    
    if sentence[x-1] == 'SELECT':
        sentence.pop()                #remove SELECT from list
        SELECT(tree, sentence, table)              #call SELECT function
    else:
        print('Your query is incorrect, please rewrite!')

    #qury_print(sentence, tree, table)
	    

read_split()

#print('table :', table)
#print('counter :', counter)
#print('sentence :', sentence)

