f = open("error.txt",encoding="utf-8")
e_set=set()

# something wrong.Q2577283#Q753110
for line in f.readlines():
    if line.startswith("Q"):
        e_set.add(line.replace("\n",""))
    elif line.startswith("something"):
        e_set.add(line.split("wrong.")[1].replace("\n","").split("#")[0])
        e_set.add(line.split("wrong.")[1].replace("\n","").split("#")[1])

print(e_set)
print(len(e_set))
