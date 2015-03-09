from pprint import pprint
f = open('records.csv', 'r')

i = 0 

master = dict() #indexed by record
record = dict() #indexed by tag
keyDict = dict() #maps tags to indexs

for line in f: 
    if i == 0:
        j = 0 
        for tag in line.split(','): 
            tag = tag.strip()
            cat = tag.split('.')[0]
            record[cat] = 0
            keyDict[j] = cat
            j+=1
        print keyDict
        print record

    else: 
        j = 0
        index = None 
        for val in line.split(','):
            if j == 0:
                index = val 
                master[index] = record.copy()
            else:
                if val != "":
                    print index, j, val
                    master[index][keyDict[j]] += 1
            j+=1
    i+=1

f.close()

pprint(master)
