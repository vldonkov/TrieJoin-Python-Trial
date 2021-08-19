import sys
import pandas
import time
from helpers import Trie

def LFTJ(context, flag_position):
    # base case
    if len(context) == count_variables_free:
        if count_variables_free == 0:
            payload = LFTJ_bound(context, False)
            file.writelines([str(payload),'\n'])
        elif count_variables_free == count_variables:
            temp = list(map(str, context))
            temp = ','.join(temp)
            file.write(temp + '\n')
        else:
            payload = LFTJ_bound(context, False)
            temp = list(map(str, context + [payload]))
            temp = ','.join(temp)
            file.write(temp + '\n')
        return

    if flag_position:
        for t in tries:
            t.position(context)

    countNotNone = 0
    seekKey = -9999999999
    for t in tries:
        t.open()
        if t.key() is not None:
            countNotNone += 1
            if seekKey < t.key():
                seekKey = t.key()

    statusAtEnd = ''
    while statusAtEnd != 'seek() - atEnd' and statusAtEnd != 'next() - atEnd':
        matches = 0
        for t in tries:
            if t.key() is None:
                continue
            statusAtEnd = t.seek(seekKey)
            currentKey = t.key()
            if statusAtEnd == 'seek() - atEnd':
                break
            elif currentKey == seekKey:
                matches += 1
            else:
                seekKey = currentKey
                break
        if matches == countNotNone:
            LFTJ(context + [currentKey], False)
            for t in tries:
                statusAtEnd = t.next()
                if statusAtEnd == 'next() - atEnd':
                    break
                if t.key() is not None:
                    if seekKey < t.key():
                        seekKey = t.key()
            # if statusAtEnd != 'next() - atEnd':
            #     for t in tries:
            #         if t.key() is not None:
            #             if temp < t.key():
            #                 temp = t.key()

    for t in tries:
        t.up()


def LFTJ_bound(context, flag_position):
    # base case
    if len(context) == count_variables:
        prod_payload = 1
        for t in tries:
            prod_payload *= t.payload()
        return prod_payload

    if flag_position:
        for t in tries:
            t.position(context)

    countNotNone = 0
    seekKey = -9999999999
    for t in tries:
        t.open()
        if t.key() is not None:
            countNotNone += 1
            if seekKey < t.key():
                seekKey = t.key()

    sum_payload = 0
    statusAtEnd = ''
    while statusAtEnd != 'seek() - atEnd' and statusAtEnd != 'next() - atEnd':
        matches = 0
        for t in tries:
            if t.key() is None:
                continue
            statusAtEnd = t.seek(seekKey)
            currentKey = t.key()
            if statusAtEnd == 'seek() - atEnd':
                break
            elif currentKey == seekKey:
                matches += 1
            else:
                seekKey = currentKey
                break
        if matches == countNotNone:
            child_payload = LFTJ_bound(context + [currentKey], False)
            sum_payload += child_payload
            for t in tries:
                statusAtEnd = t.next()
                if statusAtEnd == 'next() - atEnd':
                    break
                if t.key() is not None:
                    if seekKey < t.key():
                        seekKey = t.key()

    for t in tries:
        t.up()

    return sum_payload

fileBench = open(rf"{sys.argv[2]}/benchmarking.txt","a")
fileBench.write('Query,Preprocessing Time (ms),Execution Time (ms)\n')

#################################################################################################
######################################## ego-Facebook ###########################################
#################################################################################################
tic1PathCountPre = time.perf_counter()

# read-in Facebook data
df_all = pandas.read_table(f'{sys.argv[1]}/snap/ego-Facebook.tbl', sep='|', header=None, names=['A', 'B'])
df_A = pandas.read_table(f'{sys.argv[1]}/snap/ego-Facebook-A.tbl', sep='|', header=None, names=['A'])
df_B = pandas.read_table(f'{sys.argv[1]}/snap/ego-Facebook-B.tbl', sep='|', header=None, names=['A'])

# sort in ascending order
df_all.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_A.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)
df_B.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)

# 1-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B']])
t3 = Trie()
for index, row in df_B.iterrows():
    t3.insert([None, row['A']])
tries = [t1, t2, t3]

# 1-path-count: the depth of the trie
count_variables = 2

# 1-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc1PathCountPre = time.perf_counter()
timeDiffPre = int((toc1PathCountPre - tic1PathCountPre)*1000)

# 1-path-count: execute query
tic1PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-1-path-count.txt","a")
LFTJ([], True)
file.close()
toc1PathCountExe = time.perf_counter()
timeDiffExe = int((toc1PathCountExe- tic1PathCountExe)*1000)
fileBench.writelines(['facebook-1-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic1PathFullPre = time.perf_counter()

# 1-path-full: the depth of the trie
count_variables = 2

# 1-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 2

toc1PathFullPre = time.perf_counter()
timeDiffPre = int((toc1PathFullPre - tic1PathFullPre)*1000)

# 1-path-full: execute query
tic1PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-1-path-full.txt","a")
LFTJ([], True)
file.close()
toc1PathFullExe = time.perf_counter()
timeDiffExe = int((toc1PathFullExe- tic1PathFullExe)*1000)
fileBench.writelines(['facebook-1-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathCountPre = time.perf_counter()

# 2-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None, None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B'], None])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([None, row['A'], row['B']])
t4 = Trie()
for index, row in df_B.iterrows():
    t4.insert([None, None, row['A']])
tries = [t1, t2, t3, t4]

# 2-path-count: the depth of the trie
count_variables = 3

# 2-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc2PathCountPre = time.perf_counter()
timeDiffPre = int((toc2PathCountPre - tic2PathCountPre)*1000)

# 2-path-count: execute query
tic2PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-2-path-count.txt","a")
LFTJ([], True)
file.close()
toc2PathCountExe = time.perf_counter()
timeDiffExe = int((toc2PathCountExe- tic2PathCountExe)*1000)
fileBench.writelines(['facebook-2-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathFullPre = time.perf_counter()

# 2-path-full: the depth of the trie
count_variables = 3

# 2-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

toc2PathFullPre = time.perf_counter()
timeDiffPre = int((toc2PathFullPre - tic2PathFullPre)*1000)

# 2-path-full: execute query
tic2PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-2-path-full.txt","a")
LFTJ([], True)
file.close()
toc2PathFullExe = time.perf_counter()
timeDiffExe = int((toc2PathFullExe- tic2PathFullExe)*1000)
fileBench.writelines(['facebook-2-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleCountPre = time.perf_counter()

# triangle-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_all.iterrows():
    t1.insert([row['A'], row['B'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([None, row['A'], row['B']])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([row['A'], None, row['B']])
tries = [t1, t2, t3]

# triangle-count: the depth of the trie
count_variables = 3

# triangle-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

tocTriangleCountPre = time.perf_counter()
timeDiffPre = int((tocTriangleCountPre - ticTriangleCountPre)*1000)

# triangle-count: execute query
ticTriangleCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-triangle-count.txt","a")
LFTJ([], True)
file.close()
tocTriangleCountExe = time.perf_counter()
timeDiffExe = int((tocTriangleCountExe - ticTriangleCountExe)*1000)
fileBench.writelines(['facebook-triangle-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleFullPre = time.perf_counter()

# triangle-full: the depth of the trie
count_variables = 3

# triangle-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

tocTriangleFullPre = time.perf_counter()
timeDiffPre = int((tocTriangleFullPre - ticTriangleFullPre)*1000)

# triangle-full: execute query
ticTriangleFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/facebook-triangle-full.txt","a")
LFTJ([], True)
file.close()
tocTriangleFullExe = time.perf_counter()
timeDiffExe = int((tocTriangleFullExe - ticTriangleFullExe)*1000)
fileBench.writelines(['facebook-triangle-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


#################################################################################################
######################################## ego-Twitter ############################################
#################################################################################################

tic1PathCountPre = time.perf_counter()

# read-in Twitter data
df_all = pandas.read_table(f'{sys.argv[1]}/snap/ego-Twitter.tbl', sep='|', header=None, names=['A', 'B'])
df_A = pandas.read_table(f'{sys.argv[1]}/snap/ego-Twitter-A.tbl', sep='|', header=None, names=['A'])
df_B = pandas.read_table(f'{sys.argv[1]}/snap/ego-Twitter-B.tbl', sep='|', header=None, names=['A'])

# sort in ascending order
df_all.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_A.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)
df_B.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)

# 1-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B']])
t3 = Trie()
for index, row in df_B.iterrows():
    t3.insert([None, row['A']])
tries = [t1, t2, t3]

# 1-path-count: the depth of the trie
count_variables = 2

# 1-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc1PathCountPre = time.perf_counter()
timeDiffPre = int((toc1PathCountPre - tic1PathCountPre)*1000)

# 1-path-count: execute query
tic1PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-1-path-count.txt","a")
LFTJ([], True)
file.close()
toc1PathCountExe = time.perf_counter()
timeDiffExe = int((toc1PathCountExe- tic1PathCountExe)*1000)
fileBench.writelines(['twitter-1-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic1PathFullPre = time.perf_counter()

# 1-path-full: the depth of the trie
count_variables = 2

# 1-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 2

toc1PathFullPre = time.perf_counter()
timeDiffPre = int((toc1PathFullPre - tic1PathFullPre)*1000)

# 1-path-full: execute query
tic1PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-1-path-full.txt","a")
LFTJ([], True)
file.close()
toc1PathFullExe = time.perf_counter()
timeDiffExe = int((toc1PathFullExe- tic1PathFullExe)*1000)
fileBench.writelines(['twitter-1-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathCountPre = time.perf_counter()

# 2-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None, None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B'], None])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([None, row['A'], row['B']])
t4 = Trie()
for index, row in df_B.iterrows():
    t4.insert([None, None, row['A']])
tries = [t1, t2, t3, t4]

# 2-path-count: the depth of the trie
count_variables = 3

# 2-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc2PathCountPre = time.perf_counter()
timeDiffPre = int((toc2PathCountPre - tic2PathCountPre)*1000)

# 2-path-count: execute query
tic2PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-2-path-count.txt","a")
LFTJ([], True)
file.close()
toc2PathCountExe = time.perf_counter()
timeDiffExe = int((toc2PathCountExe- tic2PathCountExe)*1000)
fileBench.writelines(['twitter-2-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathFullPre = time.perf_counter()

# 2-path-full: the depth of the trie
count_variables = 3

# 2-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

toc2PathFullPre = time.perf_counter()
timeDiffPre = int((toc2PathFullPre - tic2PathFullPre)*1000)

# 2-path-full: execute query
tic2PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-2-path-full.txt","a")
LFTJ([], True)
file.close()
toc2PathFullExe = time.perf_counter()
timeDiffExe = int((toc2PathFullExe- tic2PathFullExe)*1000)
fileBench.writelines(['twitter-2-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleCountPre = time.perf_counter()

# triangle-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_all.iterrows():
    t1.insert([row['A'], row['B'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([None, row['A'], row['B']])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([row['A'], None, row['B']])
tries = [t1, t2, t3]

# triangle-count: the depth of the trie
count_variables = 3

# triangle-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

tocTriangleCountPre = time.perf_counter()
timeDiffPre = int((tocTriangleCountPre - ticTriangleCountPre)*1000)

# triangle-count: execute query
ticTriangleCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-triangle-count.txt","a")
LFTJ([], True)
file.close()
tocTriangleCountExe = time.perf_counter()
timeDiffExe = int((tocTriangleCountExe - ticTriangleCountExe)*1000)
fileBench.writelines(['twitter-triangle-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleFullPre = time.perf_counter()

# triangle-full: the depth of the trie
count_variables = 3

# triangle-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

tocTriangleFullPre = time.perf_counter()
timeDiffPre = int((tocTriangleFullPre - ticTriangleFullPre)*1000)

# triangle-full: execute query
ticTriangleFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/twitter-triangle-full.txt","a")
LFTJ([], True)
file.close()
tocTriangleFullExe = time.perf_counter()
timeDiffExe = int((tocTriangleFullExe - ticTriangleFullExe)*1000)
fileBench.writelines(['twitter-triangle-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


#################################################################################################
######################################## wiki-Vote ##############################################
#################################################################################################

tic1PathCountPre = time.perf_counter()

# read-in wiki data
df_all = pandas.read_table(f'{sys.argv[1]}/snap/wiki-Vote.tbl', sep='|', header=None, names=['A', 'B'])
df_A = pandas.read_table(f'{sys.argv[1]}/snap/wiki-Vote-A.tbl', sep='|', header=None, names=['A'])
df_B = pandas.read_table(f'{sys.argv[1]}/snap/wiki-Vote-B.tbl', sep='|', header=None, names=['A'])

# sort in ascending order
df_all.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_A.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)
df_B.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)

# 1-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B']])
t3 = Trie()
for index, row in df_B.iterrows():
    t3.insert([None, row['A']])
tries = [t1, t2, t3]

# 1-path-count: the depth of the trie
count_variables = 2

# 1-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc1PathCountPre = time.perf_counter()
timeDiffPre = int((toc1PathCountPre - tic1PathCountPre)*1000)

# 1-path-count: execute query
tic1PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-1-path-count.txt","a")
LFTJ([], True)
file.close()
toc1PathCountExe = time.perf_counter()
timeDiffExe = int((toc1PathCountExe- tic1PathCountExe)*1000)
fileBench.writelines(['wiki-1-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic1PathFullPre = time.perf_counter()

# 1-path-full: the depth of the trie
count_variables = 2

# 1-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 2

toc1PathFullPre = time.perf_counter()
timeDiffPre = int((toc1PathFullPre - tic1PathFullPre)*1000)

# 1-path-full: execute query
tic1PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-1-path-full.txt","a")
LFTJ([], True)
file.close()
toc1PathFullExe = time.perf_counter()
timeDiffExe = int((toc1PathFullExe- tic1PathFullExe)*1000)
fileBench.writelines(['wiki-1-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathCountPre = time.perf_counter()

# 2-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None, None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B'], None])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([None, row['A'], row['B']])
t4 = Trie()
for index, row in df_B.iterrows():
    t4.insert([None, None, row['A']])
tries = [t1, t2, t3, t4]

# 2-path-count: the depth of the trie
count_variables = 3

# 2-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc2PathCountPre = time.perf_counter()
timeDiffPre = int((toc2PathCountPre - tic2PathCountPre)*1000)

# 2-path-count: execute query
tic2PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-2-path-count.txt","a")
LFTJ([], True)
file.close()
toc2PathCountExe = time.perf_counter()
timeDiffExe = int((toc2PathCountExe- tic2PathCountExe)*1000)
fileBench.writelines(['wiki-2-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathFullPre = time.perf_counter()

# 2-path-full: the depth of the trie
count_variables = 3

# 2-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

toc2PathFullPre = time.perf_counter()
timeDiffPre = int((toc2PathFullPre - tic2PathFullPre)*1000)

# 2-path-full: execute query
tic2PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-2-path-full.txt","a")
LFTJ([], True)
file.close()
toc2PathFullExe = time.perf_counter()
timeDiffExe = int((toc2PathFullExe- tic2PathFullExe)*1000)
fileBench.writelines(['wiki-2-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleCountPre = time.perf_counter()

# triangle-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_all.iterrows():
    t1.insert([row['A'], row['B'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([None, row['A'], row['B']])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([row['A'], None, row['B']])
tries = [t1, t2, t3]

# triangle-count: the depth of the trie
count_variables = 3

# triangle-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

tocTriangleCountPre = time.perf_counter()
timeDiffPre = int((tocTriangleCountPre - ticTriangleCountPre)*1000)

# triangle-count: execute query
ticTriangleCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-triangle-count.txt","a")
LFTJ([], True)
file.close()
tocTriangleCountExe = time.perf_counter()
timeDiffExe = int((tocTriangleCountExe - ticTriangleCountExe)*1000)
fileBench.writelines(['wiki-triangle-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleFullPre = time.perf_counter()

# triangle-full: the depth of the trie
count_variables = 3

# triangle-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

tocTriangleFullPre = time.perf_counter()
timeDiffPre = int((tocTriangleFullPre - ticTriangleFullPre)*1000)

# triangle-full: execute query
ticTriangleFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/wiki-triangle-full.txt","a")
LFTJ([], True)
file.close()
tocTriangleFullExe = time.perf_counter()
timeDiffExe = int((tocTriangleFullExe - ticTriangleFullExe)*1000)
fileBench.writelines(['wiki-triangle-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


#################################################################################################
######################################## email-Enron ############################################
#################################################################################################

tic1PathCountPre = time.perf_counter()

# read-in Enron data
df_all = pandas.read_table(f'{sys.argv[1]}/snap/email-Enron.tbl', sep='|', header=None, names=['A', 'B'])
df_A = pandas.read_table(f'{sys.argv[1]}/snap/email-Enron-A.tbl', sep='|', header=None, names=['A'])
df_B = pandas.read_table(f'{sys.argv[1]}/snap/email-Enron-B.tbl', sep='|', header=None, names=['A'])

# sort in ascending order
df_all.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_A.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)
df_B.sort_values(by=['A'], ascending=True, inplace=True, ignore_index=True)

# 1-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B']])
t3 = Trie()
for index, row in df_B.iterrows():
    t3.insert([None, row['A']])
tries = [t1, t2, t3]

# 1-path-count: the depth of the trie
count_variables = 2

# 1-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc1PathCountPre = time.perf_counter()
timeDiffPre = int((toc1PathCountPre - tic1PathCountPre)*1000)

# 1-path-count: execute query
tic1PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-1-path-count.txt","a")
LFTJ([], True)
file.close()
toc1PathCountExe = time.perf_counter()
timeDiffExe = int((toc1PathCountExe- tic1PathCountExe)*1000)
fileBench.writelines(['enron-1-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic1PathFullPre = time.perf_counter()

# 1-path-full: the depth of the trie
count_variables = 2

# 1-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 2

toc1PathFullPre = time.perf_counter()
timeDiffPre = int((toc1PathFullPre - tic1PathFullPre)*1000)

# 1-path-full: execute query
tic1PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-1-path-full.txt","a")
LFTJ([], True)
file.close()
toc1PathFullExe = time.perf_counter()
timeDiffExe = int((toc1PathFullExe- tic1PathFullExe)*1000)
fileBench.writelines(['enron-1-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathCountPre = time.perf_counter()

# 2-path-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_A.iterrows():
    t1.insert([row['A'], None, None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([row['A'], row['B'], None])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([None, row['A'], row['B']])
t4 = Trie()
for index, row in df_B.iterrows():
    t4.insert([None, None, row['A']])
tries = [t1, t2, t3, t4]

# 2-path-count: the depth of the trie
count_variables = 3

# 2-path-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

toc2PathCountPre = time.perf_counter()
timeDiffPre = int((toc2PathCountPre - tic2PathCountPre)*1000)

# 2-path-count: execute query
tic2PathCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-2-path-count.txt","a")
LFTJ([], True)
file.close()
toc2PathCountExe = time.perf_counter()
timeDiffExe = int((toc2PathCountExe- tic2PathCountExe)*1000)
fileBench.writelines(['enron-2-path-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

tic2PathFullPre = time.perf_counter()

# 2-path-full: the depth of the trie
count_variables = 3

# 2-path-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

toc2PathFullPre = time.perf_counter()
timeDiffPre = int((toc2PathFullPre - tic2PathFullPre)*1000)

# 2-path-full: execute query
tic2PathFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-2-path-full.txt","a")
LFTJ([], True)
file.close()
toc2PathFullExe = time.perf_counter()
timeDiffExe = int((toc2PathFullExe- tic2PathFullExe)*1000)
fileBench.writelines(['enron-2-path-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleCountPre = time.perf_counter()

# triangle-count: put each factor into a trie data structure
t1 = Trie()
for index, row in df_all.iterrows():
    t1.insert([row['A'], row['B'], None])
t2 = Trie()
for index, row in df_all.iterrows():
    t2.insert([None, row['A'], row['B']])
t3 = Trie()
for index, row in df_all.iterrows():
    t3.insert([row['A'], None, row['B']])
tries = [t1, t2, t3]

# triangle-count: the depth of the trie
count_variables = 3

# triangle-count: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

tocTriangleCountPre = time.perf_counter()
timeDiffPre = int((tocTriangleCountPre - ticTriangleCountPre)*1000)

# triangle-count: execute query
ticTriangleCountExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-triangle-count.txt","a")
LFTJ([], True)
file.close()
tocTriangleCountExe = time.perf_counter()
timeDiffExe = int((tocTriangleCountExe - ticTriangleCountExe)*1000)
fileBench.writelines(['enron-triangle-count,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

ticTriangleFullPre = time.perf_counter()

# triangle-full: the depth of the trie
count_variables = 3

# triangle-full: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

tocTriangleFullPre = time.perf_counter()
timeDiffPre = int((tocTriangleFullPre - ticTriangleFullPre)*1000)

# triangle-full: execute query
ticTriangleFullExe = time.perf_counter()
file = open(rf"{sys.argv[2]}/snap/enron-triangle-full.txt","a")
LFTJ([], True)
file.close()
tocTriangleFullExe = time.perf_counter()
timeDiffExe = int((tocTriangleFullExe - ticTriangleFullExe)*1000)
fileBench.writelines(['enron-triangle-full,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

fileBench.close()