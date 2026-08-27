from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import emoji


extract = URLExtract()


# =========================
# BASIC STATISTICS
# =========================

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    # Number of messages
    num_messages = df.shape[0]

    # Number of words
    words = []

    for message in df['message']:

        words.extend(
            message.split()
        )

    # Number of media messages
    num_media_messages = df[
        df['message'] == '<Media omitted>\n'
    ].shape[0]

    # Number of links
    links = []

    for message in df['message']:

        links.extend(
            extract.find_urls(
                message
            )
        )

    return (
        num_messages,
        len(words),
        num_media_messages,
        len(links)
    )


# =========================
# MOST BUSY USERS
# =========================

def most_busy_users(df):

    # Remove group notifications
    temp = df[
        df['user'] != 'group_notification'
    ]

    x = temp[
        'user'
    ].value_counts().head()

    user_percentage = round(
        (
            temp['user'].value_counts()
            / temp.shape[0]
        ) * 100,
        2
    ).reset_index()

    user_percentage = user_percentage.rename(
        columns={
            'index': 'name',
            'user': 'percent'
        }
    )

    return (
        x,
        user_percentage
    )


# =========================
# MONTHLY TIMELINE
# =========================

def monthly_timeline(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    timeline = (
        df.groupby(
            [
                'year',
                'month_num',
                'month'
            ]
        )
        .count()['message']
        .reset_index()
    )

    # Sort chronologically
    timeline = timeline.sort_values(
        [
            'year',
            'month_num'
        ]
    )

    # Create labels
    timeline['time'] = (
        timeline['month'].str[:3]
        + "-"
        + timeline['year'].astype(str)
    )

    return timeline


# =========================
# DAILY TIMELINE
# =========================

def daily_timeline(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    daily = (
        df.groupby(
            'only_date'
        )
        .count()['message']
        .reset_index()
    )

    daily = daily.sort_values(
        'only_date'
    )

    return daily


# =========================
# MOST BUSY DAY
# =========================

def week_activity_map(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    busy_day = (
        df['day_name']
        .value_counts()
    )

    # Keep normal week order
    day_order = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    busy_day = busy_day.reindex(
        day_order
    ).fillna(0)

    return busy_day


# =========================
# MOST BUSY MONTH
# =========================

def month_activity_map(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    busy_month = (
        df['month']
        .value_counts()
    )

    # Normal month order
    month_order = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    busy_month = busy_month.reindex(
        month_order
    ).fillna(0)

    return busy_month


# =========================
# WORDCLOUD
# =========================

def create_wordcloud(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    # Remove group notifications
    df = df[
        df['user'] != 'group_notification'
    ]

    # Remove media messages
    df = df[
        df['message'] != '<Media omitted>\n'
    ]

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    text = df[
        'message'
    ].str.cat(
        sep=" "
    )

    # Prevent error when there is no text
    if not text.strip():

        text = "No Messages"

    df_wc = wc.generate(
        text
    )

    return df_wc


# =========================
# MOST COMMON WORDS
# =========================

def most_common_words(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    # Remove group notifications
    temp = df[
        df['user'] != 'group_notification'
    ]

    # Remove media messages
    temp = temp[
        temp['message'] != '<Media omitted>\n'
    ]


    # =========================
    # STOPWORDS
    # =========================

    stop_words = {

        'a', 'an', 'the', 'and', 'or',
        'but', 'if', 'then', 'than',
        'this', 'that', 'these',
        'those', 'is', 'am', 'are',
        'was', 'were', 'be', 'been',
        'being',

        'to', 'of', 'in', 'on',
        'at', 'for', 'from', 'with',
        'by', 'about', 'as', 'into',
        'through', 'during', 'before',
        'after', 'above', 'below',
        'up', 'down', 'out', 'off',
        'over', 'under', 'again',
        'further', 'once',

        'i', 'me', 'my', 'mine',
        'myself', 'we', 'us',
        'our', 'ours', 'you',
        'your', 'yours', 'yourself',

        'he', 'him', 'his',
        'she', 'her', 'hers',
        'it', 'its', 'they',
        'them', 'their', 'theirs',

        'what', 'which', 'who',
        'whom', 'whose', 'when',
        'where', 'why', 'how',

        'all', 'any', 'both',
        'each', 'few', 'more',
        'most', 'other', 'some',
        'such', 'no', 'nor',
        'not', 'only', 'own',
        'same', 'so', 'too',
        'very',

        'can', 'will', 'just',
        'should', 'now', 'do',
        'does', 'did', 'doing',

        'have', 'has', 'had',
        'having',

        'get', 'got', 'getting',

        'would', 'could',
        'might', 'must',
        'shall',

        'also', 'there',
        'here', 'yes',
        'okay', 'ok'
    }


    words = []


    for message in temp['message']:

        message = message.lower()

        message_words = re.findall(
            r"[a-zA-Z]+(?:'[a-zA-Z]+)?",
            message
        )

        for word in message_words:

            if (
                word not in stop_words
                and len(word) > 2
            ):

                words.append(
                    word
                )


    common_words = Counter(
        words
    ).most_common(20)


    most_common_df = pd.DataFrame(
        common_words,
        columns=[
            'word',
            'frequency'
        ]
    )

    return most_common_df


# =========================
# EMOJI ANALYSIS
# =========================

def emoji_helper(
    selected_user,
    df
):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    emojis = []


    for message in df['message']:

        found_emojis = emoji.emoji_list(
            message
        )

        for item in found_emojis:

            emojis.append(
                item['emoji']
            )


    emoji_counts = Counter(
        emojis
    )


    emoji_df = pd.DataFrame(
        emoji_counts.most_common(),
        columns=[
            'emoji',
            'count'
        ]
    )

    return emoji_df

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
