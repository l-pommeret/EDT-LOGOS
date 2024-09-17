import os, glob, json


allcalendars=[]

listejson=glob.glob('calendars-*.json')
listejson.sort()

for filename in listejson:
   print(filename)
   with open(os.path.join(os.getcwd(), filename), 'r') as f:
      allcalendars+= json.load(f)


with open("merged.json","w", encoding='utf8') as newcaljson:
         newcaljson.write("[\n")
         for i in range(len(allcalendars)):
             dico=(allcalendars[i])
             ligne="   "+json.dumps(dico,ensure_ascii=False)
             if i+1< len(allcalendars):
                 ligne=ligne+" ,\n"
             newcaljson.write(ligne)
         newcaljson.write("\n]\n")

