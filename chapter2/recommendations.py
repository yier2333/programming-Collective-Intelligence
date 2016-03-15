#==============================================================================
# 名称：用户偏好字典
# 描述：critics存储了一个复合的字典，里面的键是人名，值是一个字典（键值对分别是电影：评分）
# 简单描述：{人名：（电影名：评分）}
#==============================================================================
# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

#==============================================================================
# 描述：计算两个人的相似性（度量标准是欧氏距离）
# 输入：用户偏好字典/用户p1和用户p2的偏好信息
# 输出：p1和p2的相似性值
#==============================================================================
# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

#==============================================================================
# 描述：计算两个人的相似性（度量标准是皮尔逊距离）
# 输入：用户偏好字典/用户p1和用户p2的偏好信息
# 输出：p1和p2的相似性值
#==============================================================================
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)
  
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

#==============================================================================
# 描述：计算最相似的前n名用户（物品） 记住返回格式是list，其他函数返回几乎都是字典格式
# 输入：用户（物品）的偏好字典/当前用户（物品）p的偏好信息/n/相似性度量函数（默认值是皮尔逊相似性）
# 输出：p的前n个相似的用户（物品）{相似性值,用户名}({相似性值,物品名})
#==============================================================================
# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

#==============================================================================
# 描述：向当前用户推荐物品（用户之前没有评论过的物品）
# 输入：用户的偏好字典/当前用户p的偏好信息/相似性度量函数（默认值是皮尔逊相似性）
# 输出：推荐的物品{推荐的强度（大到小）：物品名称} 
#==============================================================================
# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

#==============================================================================
# 描述：将用户偏好字典转换成物品偏好字典{人：（电影：评分）}
# 输入：用户的偏好字典
# 输出：物品偏好字典{电影：（人：评分）} 
#==============================================================================
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result

#==============================================================================
# 描述：计算物品的相似性，返回最相相似的n个物品(一次性计算所有的物品之间的相似性)
# 输入：用户偏好字典（先要转换成物品偏好字典才能计算相似性)/n
# 输出：物品相似性字典{物品名：{相似性值：物品}}
#==============================================================================
def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result
  
#==============================================================================
# 描述：推荐物品
# 输入：用户偏好字典/物品相似性字典（前n个最相似的）/要进行推荐的用户p
# 输出：推荐给p的物品字典{推荐程度：物品名}
#==============================================================================
def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

#==============================================================================
# 描述：加载数据集MovieLens并且转换成标准的用户偏好字典格式
# 输入：数据集地址
# 输出：推荐给p的物品字典{推荐程度：物品名}
#==============================================================================
def loadMovieLens(path='/data/movielens'):
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
#==============================================================================
# 下面是自己写的一些程序 .集体智慧编程Ch2-3  得到的结果和基于物品的推荐结果相似
#==============================================================================
#==============================================================================
# 描述：计算用户的相似性，返回最相似的n个用户名（一次性计算所有用户之间的相似性）
# 输入：用户的偏好字典/n
# 输出：用户相似性字典{用户名：{相似性值：用户名}}
#==============================================================================
def calculateSimilarUsers(prefs,n=5):
  # Create a dictionary of users showing which other users they
  # are most similar to.
  result={}
  c=0
  for user in prefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar users to this one
    scores=topMatches(prefs,user,n=n,similarity=sim_distance)
    result[user]=scores
  return result
  
#==============================================================================
# 描述：推荐物品
# 输入：用户偏好字典/物品相似性字典（前n个最相似的）/要进行推荐的用户p
# 输出：推荐给p的物品字典{推荐程度：物品名}
#==============================================================================
def getRecommendedUsers(prefs,userMatch,user):
  userRatings=prefs[user]
  sameUser=userMatch[user]

  scores={}
  totalSim={}
  # Loop over others matched to this user
  for (similarity,other) in sameUser:
    otherRatings=prefs[other]
    
    # Loop over items of other
    for (item,rating) in otherRatings.items( ):

      # Ignore if this user has already rated this item
      if item in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item,0)
      scores[item]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item,0)
      totalSim[item]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings
  
print getRecommendedUsers(critics,calculateSimilarUsers(critics,n=5),'Toby')
