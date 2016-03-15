import feedparser
import re

#==============================================================================
# 描述：统计一个URL中的单词信息
# 输入：URL
# 输出：title和wc={word:count}
#==============================================================================
# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
  return d.feed.title,wc

def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
  return [word.lower() for word in words if word!='']


apcount={} #统计所有文章中的词频 {word:num}
wordcounts={} #统计每个URL中的词频 {title:{word:num}}
feedlist=[line for line in file('feedlist.txt')] #URL列表
for feedurl in feedlist:
  try:
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
      apcount.setdefault(word,0)
      if count>1:
        apcount[word]+=1
  except:
    print 'Failed to parse feed %s' % feedurl

wordlist=[] #将词频总数除以文章总数，获得频率,获取频率在0.1到0.5之间的单词
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>0.1 and frac<0.5:
    wordlist.append(w)

out=file('blogdata1.txt','w')  #存储一个单词频度矩阵   横：URL文章  纵：单词  内容：单词频度
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)  #纵
out.write('\n')
for blog,wc in wordcounts.items():  
  out.write(blog)   #横
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])  #用制表符隔开元素
    else: out.write('\t0')
  out.write('\n')
