f = open("tagged_records.csv", "r")

text = f.read().replace('\r', '\n')

f.close()

fout = open("records.csv", "w")

fout.write(text)
fout.close()
