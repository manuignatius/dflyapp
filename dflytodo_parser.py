
f = open('test.txt', 'r')
lines = f.readlines()
f.close()

for i in lines:
#    print i
    if i.find("todo:") != -1:
        t = i.split()
        t.remove("todo:")
        print t
        for j in t:
            if j[0] == "@":
                print "People: " + j
                t.remove(j)
            if j[0] == "[":
                print "Due date: " + j
                t.remove(j)
        print t
