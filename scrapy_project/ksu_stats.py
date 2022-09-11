import json
import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from operator import itemgetter

#import the json file from out crawler and parse it
filename = 'C:/Users/kevin/PycharmProjects/Information Retrieval/venv/src/ksuScrapy/scrapy_project/ksu1000.json'
input = open(filename)
data = json.load(input)
input.close()
print('****************KSU scrapy webpage statistics****************')

#compute the average length of webpages in tokens
page_count = 0
doc_len = 0
for entry in data:
    page_count += 1
    doc_len += len(entry['body'].split())
avg_len = doc_len/page_count
print('average doc len:',avg_len)

#find the top 10 email adresses
email_freq = {}
for entry in data:
    for e in entry['emails']:
        if e not in email_freq:
            email_freq[e] = 0
        email_freq[e] += 1
top_10 = sorted(email_freq.items(), key = itemgetter(1), reverse=True)[:10]
print('most frequent emails:')
for e in top_10:
    print('\t',e)

#calculate the percentage of scraped webpages which contain at least one email
email_count = 0
for entry in data:
    if len(entry['emails']) > 0:
        email_count += 1
email_percent = email_count/page_count
print('percent webpages with emails:',email_percent)

#generate word frequencies before removing stopwords/punctuation
table = '{0:>4}{1:>16}{2:>16}{3:>16}{4:>16}{5:>16}{6:>16}{7:>16}'
print(table.format('rank','term','freq.','perc.','rank','term','freq.','perc.'))
print('-'*116)

word_freq = {}
for entry in data:
    for token in entry['body'].split():
        if token not in word_freq:
            word_freq[token] = 0
        word_freq[token] += 1
top_30 = sorted(word_freq.items(), key = itemgetter(1), reverse=True)[:30]
sorted_freq = sorted(word_freq.values(),reverse = True)

out = '{0:>4}{1:>16}{2:>16}{3:>16.3f}{4:>16}{5:>16}{6:>16}{7:>16.3f}'
for i in range(15):
     freq1 = top_30[i][1]
     freq2 = top_30[i+15][1]
     print(out.format(i+1,top_30[i][0],freq1,freq1/doc_len,i+16,top_30[i+15][0],freq2,freq2/doc_len))
     i += 1
#generate word frequencies after removing stopwords/punctuation
print('\n',table.format('rank','term','freq.','perc.','rank','term','freq.','perc.'))
print('-'*116)

word_freq = {}
stop_words = set(stopwords.words('english'))
for entry in data:
    body = re.sub(r'[^a-zA-Z 0-9]','',entry['body'])
    filter = [w for w in body.split() if not w.lower() in stop_words]
    for token in filter:
        if token not in word_freq:
            word_freq[token] = 0
        word_freq[token] += 1
top_30 = sorted(word_freq.items(), key = itemgetter(1), reverse=True)[:30]

for i in range(15):
     freq1 = top_30[i][1]
     freq2 = top_30[i+15][1]
     print(out.format(i+1,top_30[i][0],freq1,freq1/doc_len,i+16,top_30[i+15][0],freq2,freq2/doc_len))
     i += 1

#plot the word distribution (rank & frequency) before removing stopwords/punctuation
i = 1
x = []
y = []
for v in sorted_freq:
    x.append(i)
    y.append(v)
    i += 1

plt.plot(x,y)
plt.xlim(-50,1000)
plt.ylim(-500,16000)
plt.xlabel('rank')
plt.ylabel('frequency')
plt.title('word distribution')
plt.show()
plt.plot(np.log(x),np.log(y))
plt.xlim(0,8)
plt.ylim(0,10)
plt.savefig('word_dist1.png')
plt.xlabel('log rank')
plt.ylabel('log frequency')
plt.title('log distribution')
plt.show()
plt.savefig('word_dist2.png')