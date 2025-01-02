import json
import pandas as pd
from collections import Counter

with open("output1.json") as f:
  data = json.load(f)

#data is a list of dictionaries with keys 'data' or 'error'

#store all the valid data (with data as a key instead of error) into a dictionary called newdata
newdata = {}

for i in range(len(data)):
   if 'data' in data[i]:
    newdata[i] = data[i]['data']

#print(newdata.keys())
#newdata has keys 0, 2, 4, 5, 7. each key stores a dictionary with keys ['videos', 'cursor', 'has_more', 'search_id']

#newdata[i]['videos'] is a list of videos stored in dictionaries. each dictionary has description:
#['hashtag_names', 'id', 'username', 'video_description', 'view_count', 'voice_to_text', 'comment_count', 'like_count', 'music_id', 'region_code', 'share_count', 'create_time']

#making a new dictionary "videos" to store all the videos (in dictionary format) from each key in newdata.

videos = {}
index = 0

for i in newdata:
   for j in newdata[i]['videos']:
      videos[index] = j
      index +=1

#print(len(videos))
#there are 394 total videos being analyzed.

#making a dictionary "users" to store each new username and add their total views, likes, and comments.
users = {}

for i in videos:
    name = videos[i]['username']
    if name not in users:
      users[name] = {'video_count':1}
      users[name]['like_count'] = videos[i]['like_count']
      users[name]['view_count'] = videos[i]['view_count']
      users[name]['comment_count'] = videos[i]['comment_count']
    else:
      users[name]['video_count'] +=1
      users[name]['like_count'] += videos[i]['like_count']
      users[name]['view_count'] += videos[i]['view_count']
      users[name]['comment_count'] += videos[i]['comment_count']

#print(len(users))
#there are 31 total users being analyzed.

#print(users)

#collecting all mentions in "videos" dictionary in a "mentions" list.
mentions = []

#sorting all mentions by username in a dictionary of "user_mentions."
user_mentions = {}

for i in videos:
    if "@" in videos[i]['video_description']:
        #check if the user posting has already mentioned people before
        if videos[i]['username'] not in user_mentions:
            #add a new user to the list of users who have mentioned other users.
            user_mentions[videos[i]['username']] = []
        x = videos[i]['video_description'].split()
        #iterate through the video description for mentions.
        for j in range(len(x)-1):
            if '@' in x[j]:
                #add all found mentions to the list of total mentions.
                mentions.append(x[j])
                #add all found mentions to the list of total mentions from that user.
                user_mentions[videos[i]['username']].append(x[j])

#print(len(mentions))
#there are 146 total mentions in the list of 394 videos.

#print(len(user_mentions))
#there are 18 total users who have mentioned other users.

#creating a sorted index to see which users mention the most other users.
user_mentions_df = []

for i in user_mentions:
    user_mentions_df.append((i, len(user_mentions[i]),user_mentions[i]))

user_mentions_df = pd.DataFrame(user_mentions_df, columns = ['user_account','mention_count','mentions_list'])

user_mentions_df = user_mentions_df.sort_values(by='mention_count', ascending=False)
print(user_mentions_df)

user_mentions_df.to_excel('users_mentioning_others.xlsx')

#maman__sereine mentions the most, followed by lifetaketwo.
#print(user_mentions['lifetaketwo'])

#creating a counter to find the most mentioned usernames.

freq = Counter(mentions)

#print(len(freq))
#there are 98 different usernames mentioned in the dataset.

#getting the top most mentioned usernames:
#for ht, c in freq.most_common(50):
   #print(ht, c)

freq_df = pd.DataFrame(list(freq.items()), columns=['mention', 'count'])
freq_df = freq_df.sort_values(by='count', ascending=False)
freq_df.to_excel('mention_counter.xlsx')

#getting the full username from some mentions that only have the first word.

edgecases = []
for i in videos:
    if "@" in videos[i]['video_description']:
        x = videos[i]['video_description'].split()
        for j in range(len(x)-1):
            if '@' in x[j]:
               if '@the' in x[j] or '@✨️' in x[j]:
                  newmention = []
                  newmention.append(x[j:j+4])
                  edgecases.append(newmention)

#for i in edgecases: print(i)

#for i in user_mentions:
#   if 'btokbeauty' in user_mentions[i]:
#      print(user_mentions[i])

#print(user_mentions['btokbeauty2'])

userdf = pd.DataFrame(users)
userdf = userdf.T

userdf = userdf.sort_values(by='view_count', ascending=False)
userdf.to_excel('tiktok_users.xlsx')

#getting the top 10 most viewed users
top10 = list(userdf.head(10).index)

#print(top10)

user_mentions_top10 = {}

for i in videos:
    for j in range(9):
       if top10[j] in videos[i]['video_description']:
          if videos[i]['username'] not in user_mentions_top10:
             user_mentions_top10[videos[i]['username']] = []
          x = videos[i]['video_description'].split()
          for k in range(len(x)-1):
             if top10[j] in x[k]:
                user_mentions_top10[videos[i]['username']].append(x[k])

#print(user_mentions_top10)
#no significant findings. the only mentions without the @ are used in hashtags from the same user.

#storing btokbeauty videos
btokbeauty_videos = []
for i in videos:
    if videos[i]['username'] == 'btokbeauty2':
        btokbeauty_videos.append(videos[i])

pd.DataFrame(btokbeauty_videos).to_excel('btokbeauty_videos.xlsx')


#storing all videos in a spreadsheet to read
all_videos = []
for i in videos:
    all_videos.append(videos[i])

all_videos = pd.DataFrame(all_videos)
all_videos.to_excel('all_tiktok_videos.xlsx')

#getting the top 10 most viewed users
top31 = list(userdf.head(31).index)

user_mentions_top31 = {}

for i in videos:
    for j in range(30):
       if top31[j] in videos[i]['video_description']:
          if videos[i]['username'] not in user_mentions_top31:
             user_mentions_top31[videos[i]['username']] = []
          x = videos[i]['video_description'].split()
          for k in range(len(x)-1):
             if top10[j] in x[k]:
                user_mentions_top31[videos[i]['username']].append(x[k])

print(user_mentions_top31)
#no significant findings. the only mentions without the @ are used in hashtags from the same user.

#checking if any of the top 10 out of sandy's top 50 accounts made it into the descriptions
#top50 = ['minimotleymomof2','lifetaketwo','thymeandtenderness','2bebetterpodcast','aberrywonderfullife','the.wicked.peach.life','theweddingguest','landladyadaogidi','mckennamotleymomof2']

#user_mentions_top50 = {}

#for i in videos:
    #for j in range(9):
       #if top50[j] in videos[i]['video_description']:
          #if videos[i]['username'] not in user_mentions_top50:
             #user_mentions_top50[videos[i]['username']] = []
          #x = videos[i]['video_description'].split()
          #for k in range(len(x)-1):
             #if top50[j] in x[k]:
                #user_mentions_top50[videos[i]['username']].append(x[k])



