from urlextract import URLExtract
from  wordcloud import  WordCloud
from collections import Counter
import pandas as pd
import emoji


extract = URLExtract()

f=open('stop_hinglish.txt', 'r')
stop_words=f.read()


def extract_stats(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    # Total messages
    total_messages = df['messages'].shape[0]

    # Total words
    total_words = []
    for message in df['messages']:
        total_words.extend(message.split())

    # Media shared
    media_shared = len(df[df['messages']=='<Media omitted>\n'])

    # Links shared
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return total_messages, len(total_words), media_shared, len(links)



def most_busy_stats(df):
    msg_count = df['users'].value_counts().head()
    msg_percentage_df= round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percentage'})

    return msg_count, msg_percentage_df


def create_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    # create wc
    wc=WordCloud(height=500, width=500,min_font_size=10, background_color='white')
    df_wc= wc.generate(df['messages'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp["messages"] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['messages', 'count'])
    return most_common_words_df


def emoji_count(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    emojis = []
    for message in df["messages"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emojis', 'count'])

    return emojis_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_name']).count()["messages"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))
    timeline['date'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline_daily = df.groupby('only_date').count()['messages'].reset_index()

    return timeline_daily


def activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts(), df['month_name'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap
