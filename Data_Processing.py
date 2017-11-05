# Process the dataset and create a dictionary of tale-titles and tales and save it as a pickle

import pickle

tales = {}
with open("AesopTales.txt", "r") as f:
    previous = ""
    s = ""
    start = True
    title = ""
    for lines in f:
        l = lines.strip()
        if(start == True):
            title = l
            start = False
        else:
            if(l == ""):
                if(prev == ""):
                    tales[title] = s[0: (len(s) - 1)]
                    # print(title)
                    # print(s[0: (len(s) - 1)])
                    # print()
                    start = True
                    s = ""
                    title = ""
                else:
                    pass
            else:
                s = s + l + " "

        prev = l
'''
for i in tales:
    print(i)
    print(tales[i])
    print()
'''
tales['''The Frogs' Complaint Against the Sun'''] = '''ONCE UPON A TIME, when the Sun announced his intention to take a wife, the Frogs lifted up their voices in clamor to the sky.  Jupiter, disturbed by the noise of their croaking, inquired the cause of their complaint.  One of them said, "The Sun, now while he is single, parches up the marsh, and compels us to die miserably in our arid homes.  What will be our future condition if he should beget other suns?"'''

with open('processed_dataset.pickle', 'wb') as handle:
    pickle.dump(tales, handle, protocol=pickle.HIGHEST_PROTOCOL)
