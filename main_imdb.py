import sys
import pandas
import time
from helpers import Trie, TrieSemiring

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
            print(context)
        else:
            payload = LFTJ_bound(context, False)
            if payload != 0:
                temp = list(map(str, context + [payload]))
                temp = ','.join(temp)
                file.write(temp + '\n')
                print(context, payload)
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

def LFTJ_semiring(context, flag_position):
    # base case
    if len(context) == count_variables_free:
        payloadSumPavgRating = LFTJ_bound_semiring(context, False, 'sumProduct', 'avgRating')
        payloadSumPnumVotes = int(LFTJ_bound_semiring(context, False, 'sumProduct', 'numVotes'))
        payloadMaxPavgRating = LFTJ_bound_semiring(context, False, 'maxProduct', 'avgRating')
        if payloadSumPavgRating != 0 and payloadSumPnumVotes != 0 and payloadMaxPavgRating != 0:
            temp = list(map(str, context + [payloadSumPavgRating] + [payloadSumPnumVotes] + [payloadMaxPavgRating]))
            temp = ','.join(temp)
            file.write(temp + '\n')
            print(context, payloadSumPavgRating,  payloadSumPnumVotes, payloadMaxPavgRating)
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
            LFTJ_semiring(context + [currentKey], False)
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

def LFTJ_bound_semiring(context, flag_position, semiRing, factorPayload):
    # base case
    if len(context) == count_variables:
        prod_payload = 1
        if factorPayload == "normal":
            for t in tries:
                prod_payload *= t.payload("normal")
        elif factorPayload == "avgRating":
            for t in tries:
                prod_payload *= t.payload("avgRating")
        else:
            for t in tries:
                prod_payload *= t.payload("numVotes")
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
            child_payload = LFTJ_bound_semiring(context + [currentKey], False, semiRing, factorPayload)
            if semiRing == "sumProduct":
                sum_payload += child_payload
            else:
                sum_payload = max(sum_payload, child_payload)
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


#################################################################################################
######################################### imdb ##################################################
#################################################################################################

ticQuery1Pre = time.perf_counter()

# read-in imdb data
df_name_basics = pandas.read_table(f'{sys.argv[1]}/imdb/name.basics.tbl', sep='|', header=None, names=['A', 'B', 'C', 'D'])
df_name_basics_knownFor = pandas.read_table(f'{sys.argv[1]}/imdb/name.basics_knownFor.tbl', sep='|', header=None, names=['A', 'B'])
df_name_basics_profession = pandas.read_table(f'{sys.argv[1]}/imdb/name.basics_profession.tbl', sep='|', header=None, names=['A', 'B'])
df_title_akas = pandas.read_table(f'{sys.argv[1]}/imdb/title.akas.tbl', sep='|', header=None, names=['A', 'B', 'C', 'D', 'E', 'F'])
df_title_akas_attributes = pandas.read_table(f'{sys.argv[1]}/imdb/title.akas_attributes.tbl', sep='|', header=None, names=['A', 'B', 'C'])
df_title_akas_types = pandas.read_table(f'{sys.argv[1]}/imdb/title.akas_types.tbl', sep='|', header=None, names=['A', 'B', 'C'])
df_title_basics = pandas.read_table(f'{sys.argv[1]}/imdb/title.basics.tbl', sep='|', header=None, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
df_title_basics_genres = pandas.read_table(f'{sys.argv[1]}/imdb/title.basics_genres.tbl', sep='|', header=None, names=['A', 'B'])
df_title_crew_directors = pandas.read_table(f'{sys.argv[1]}/imdb/title.crew_directors.tbl', sep='|', header=None, names=['A', 'B'])
df_title_crew_writers = pandas.read_table(f'{sys.argv[1]}/imdb/title.crew_writers.tbl', sep='|', header=None, names=['A', 'B'])
df_title_episode = pandas.read_table(f'{sys.argv[1]}/imdb/title.episode.tbl', sep='|', header=None, names=['A', 'B', 'C', 'D'])
df_title_principals = pandas.read_table(f'{sys.argv[1]}/imdb/title.principals.tbl', sep='|', header=None, names=['A', 'B', 'C', 'D', 'E', 'F'])
df_title_ratings = pandas.read_table(f'{sys.argv[1]}/imdb/title.ratings.tbl', sep='|', header=None, names=['A', 'B', 'C'])


# sort in ascending order
df_name_basics.sort_values(by=['A', 'B', 'C', 'D'], ascending=True, inplace=True, ignore_index=True)
df_name_basics_knownFor.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_name_basics_profession.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_title_akas.sort_values(by=['A', 'B', 'C', 'D', 'E', 'F'], ascending=True, inplace=True, ignore_index=True)
df_title_akas_attributes.sort_values(by=['A', 'B', 'C'], ascending=True, inplace=True, ignore_index=True)
df_title_akas_types.sort_values(by=['A', 'B', 'C'], ascending=True, inplace=True, ignore_index=True)
df_title_basics.sort_values(by=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], ascending=True, inplace=True, ignore_index=True)
df_title_basics_genres.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_title_crew_directors.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_title_crew_writers.sort_values(by=['A', 'B'], ascending=True, inplace=True, ignore_index=True)
df_title_episode.sort_values(by=['A', 'B', 'C', 'D'], ascending=True, inplace=True, ignore_index=True)
df_title_principals.sort_values(by=['A', 'B', 'C', 'D', 'E', 'F'], ascending=True, inplace=True, ignore_index=True)
df_title_ratings.sort_values(by=['A', 'B', 'C'], ascending=True, inplace=True, ignore_index=True)


# query1: put each factor into a trie data structure
t1 = Trie()
for index, row in df_title_akas.iterrows():
    t1.insert([row['A'], None, row['B'], row['C'], row['D'], row['E'], row['F'], None, None, None, None, None, None, None, None, None, None, None, None])
t2 = Trie()
for index, row in df_title_basics.iterrows():
    t2.insert([row['A'], None, None, None, None, None, None, row['B'], row['C'], row['D'], row['E'], row['F'], row['G'], row['H'], None, None, None, None, None])
t3 = Trie()
for index, row in df_title_basics_genres.iterrows():
    t3.insert([row['A'], None, None, None, None, None, None, None, None, None, None, None, None, None, row['B'], None, None, None, None])
t4 = Trie()
for index, row in df_title_crew_directors.iterrows():
    t4.insert([row['A'], row['B'], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
t5 = Trie()
for index, row in df_name_basics.iterrows():
    t5.insert([None, row['A'], None, None, None, None, None, None, None, None, None, None, None, None, None, row['B'], row['C'], row['D'], None])
t6 = Trie()
for index, row in df_name_basics_profession.iterrows():
    t6.insert([None, row['A'], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, row['B']])
tries = [t1, t2, t3, t4, t5, t6]

# query1: the depth of the trie
count_variables = 19

# query1: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 0

tocQuery1Pre = time.perf_counter()
timeDiffPre = int((tocQuery1Pre - ticQuery1Pre)*1000)

# query1: execute query
ticQuery1Exe = time.perf_counter()
file = open(rf"{sys.argv[2]}/imdb/query1.txt","a")
LFTJ([], True)
file.close()
tocQuery1Exe = time.perf_counter()
timeDiffExe = int((tocQuery1Exe - ticQuery1Exe)*1000)
fileBench.writelines(['query1,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


ticQuery2Pre = time.perf_counter()
df_title_principals.sort_values(by=['A', 'C', 'B', 'D', 'E', 'F'], ascending=True, inplace=True, ignore_index=True)

# query2: put each factor into a trie data structure
t1 = Trie()
for index, row in df_title_basics.iterrows():
    t1.insert([row['A'], None, row['B'], row['C'], row['D'], row['E'], row['F'], row['G'], row['H'], None, None, None, None, None, None, None, None, None])
t2 = Trie()
for index, row in df_title_principals.iterrows():
    t2.insert([row['A'], row['C'], None, None, None, None, None, None, None, row['B'], row['D'], row['E'], row['F'], None, None, None, None, None])
t3 = Trie()
for index, row in df_name_basics.iterrows():
    t3.insert([None, row['A'], None, None, None, None, None, None, None, None, None, None, None, row['B'], row['C'], row['D'], None, None])
t4 = Trie()
for index, row in df_title_ratings.iterrows():
    t4.insert([int(row['A']), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, row['B'], int(row['C'])])
tries = [t1, t2, t3, t4]

# query2: the depth of the trie
count_variables = 18

# query2: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 18

tocQuery2Pre = time.perf_counter()
timeDiffPre = int((tocQuery2Pre - ticQuery2Pre)*1000)

# query2: execute query
ticQuery2Exe = time.perf_counter()
file = open(rf"{sys.argv[2]}/imdb/query2.txt","a")
LFTJ([], True)
file.close()
tocQuery2Exe = time.perf_counter()
timeDiffExe = int((tocQuery2Exe - ticQuery2Exe)*1000)
fileBench.writelines(['query2,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


ticQuery3Pre = time.perf_counter()
df_title_basics.sort_values(by=['B', 'F', 'A', 'C', 'D', 'E', 'G', 'H'], ascending=True, inplace=True, ignore_index=True)
df_title_basics_genres.sort_values(by=['B', 'A'], ascending=True, inplace=True, ignore_index=True)

# query3: put each factor into a trie data structure
t1 = Trie()
for index, row in df_title_basics.iterrows():
    t1.insert([None, row['B'], row['F'], row['A'], row['C'], row['D'], row['E'], row['G'], row['H']])
t2 = Trie()
for index, row in df_title_basics_genres.iterrows():
    t2.insert([row['B'], None, None, row['A'], None, None, None, None, None])
tries = [t1, t2]

# query3: the depth of the trie
count_variables = 9

# query3: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 3

tocQuery3Pre = time.perf_counter()
timeDiffPre = int((tocQuery3Pre - ticQuery3Pre)*1000)

# query3: execute query
ticQuery3Exe = time.perf_counter()
file = open(rf"{sys.argv[2]}/imdb/query3.txt","a")
LFTJ([], True)
file.close()
tocQuery3Exe = time.perf_counter()
timeDiffExe = int((tocQuery3Exe - ticQuery3Exe)*1000)
fileBench.writelines(['query3,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


ticQuery4Pre = time.perf_counter()
df_title_basics.sort_values(by=['F', 'A', 'B', 'C', 'D', 'E', 'G', 'H'], ascending=True, inplace=True, ignore_index=True)
df_title_basics_genres.sort_values(by=['B', 'A'], ascending=True, inplace=True, ignore_index=True)
df_title_ratings.sort_values(by=['A', 'B', 'C'], ascending=True, inplace=True, ignore_index=True)

# query4: put each factor into a trie data structure
t1 = TrieSemiring("normal")
for index, row in df_title_basics.iterrows():
    t1.insert([None, row['F'], row['A'], row['B'], row['C'], row['D'], row['E'], row['G'], row['H'], None, None])
t2 = TrieSemiring("normal")
for index, row in df_title_basics_genres.iterrows():
    t2.insert([row['B'], None, row['A'], None, None, None, None, None, None, None, None])
t3 = TrieSemiring("special")
for index, row in df_title_ratings.iterrows():
    t3.insert([None, None, int(row['A']), None, None, None, None, None, None, row['B'], int(row['C'])])
tries = [t1, t2, t3]

# query4: the depth of the trie
count_variables = 11

# query4: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 2

tocQuery4Pre = time.perf_counter()
timeDiffPre = int((tocQuery4Pre - ticQuery4Pre)*1000)

# query4: execute query
ticQuery4Exe = time.perf_counter()
file = open(rf"{sys.argv[2]}/imdb/query4.txt","a")
LFTJ_semiring([], True)
file.close()
tocQuery4Exe = time.perf_counter()
timeDiffExe = int((tocQuery4Exe - ticQuery4Exe)*1000)
fileBench.writelines(['query4,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])


ticQuery5Pre = time.perf_counter()
df_title_basics.sort_values(by=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], ascending=True, inplace=True, ignore_index=True)
df_title_principals.sort_values(by=['A', 'B', 'C', 'D', 'E', 'F'], ascending=True, inplace=True, ignore_index=True)
df_name_basics.sort_values(by=['B', 'A', 'C', 'D'], ascending=True, inplace=True, ignore_index=True)
df_title_ratings.sort_values(by=['A', 'B', 'C'], ascending=True, inplace=True, ignore_index=True)

# query5: put each factor into a trie data structure
t1 = TrieSemiring("normal")
for index, row in df_title_basics.iterrows():
    t1.insert([None, row['A'], row['B'], row['C'], row['D'], row['E'], row['F'], row['G'], row['H'], None, None, None, None, None, None, None, None, None])
t2 = TrieSemiring("normal")
for index, row in df_title_principals.iterrows():
    t2.insert([None, row['A'], None, None, None, None, None, None, None, row['B'], row['C'], row['D'], row['E'], row['F'], None, None, None, None])
t3 = TrieSemiring("normal")
for index, row in df_name_basics.iterrows():
    t3.insert([row['B'], None, None, None, None, None, None, None, None, None, row['A'], None, None, None, row['C'], row['D'], None, None])
t4 = TrieSemiring("special")
for index, row in df_title_ratings.iterrows():
    t4.insert([None, int(row['A']), None, None, None, None, None, None, None, None, None, None, None, None, None, None, row['B'], int(row['C'])])
tries = [t1, t2, t3, t4]

# query5: the depth of the trie
count_variables = 18

# query5: the depth of the free variables in the trie (the rest are bound)
count_variables_free = 1

tocQuery5Pre = time.perf_counter()
timeDiffPre = int((tocQuery5Pre - ticQuery5Pre)*1000)

# query5: execute query
ticQuery5Exe = time.perf_counter()
file = open(rf"{sys.argv[2]}/imdb/query5.txt","a")
LFTJ_semiring([], True)
file.close()
tocQuery5Exe = time.perf_counter()
timeDiffExe = int((tocQuery5Exe - ticQuery5Exe)*1000)
fileBench.writelines(['query5,', str(timeDiffPre), ',', str(timeDiffExe), '\n'])

fileBench.close()