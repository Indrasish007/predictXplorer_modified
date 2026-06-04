import re
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# ─── Emoji Sentiment Mapping ──────────────────────────────────────────────────
# Categorises emojis into positive / negative / neutral sentiment buckets

POSITIVE_EMOJIS = set([
    '😀','😁','😂','🤣','😃','😄','😅','😆','😊','🙂','🥰','😍','🤩','😘',
    '😗','😙','😚','😋','😛','😜','🤪','🤗','🥳','🎉','🎊','✨','🌟','⭐',
    '💫','🙌','👍','❤️','💕','💞','💓','💗','💖','💘','💝','💪','🔥','👏',
    '🥹','😺','🐱','🌈','🌺','🌸','🌻','🌼','🌹','💐','🎶','🎵','😻','🥰',
    '🤸','💃','🕺','🎯','🏆','🎖️','🥇','👑','✅','💯','🆗','🤙','🫶','❤',
    '🧡','💛','💚','💙','💜','🖤','🩷','🩶','🩵','🤍','🤎','♥','🫀',
    '🎈','🎀','🎁','🪅','🥂','🍾','🎂','🍰','🧁','🍭','🍬','🍫','🍩',
    '😇','🤠','🥸','😸','😹','😼','🐶','🐱','🦊','🐣','🐥','🦋','🌊',
    '🏖️','🏝️','🗺️','🌅','🌄','🌠','🎆','🎇','🧨','🎏','🎐',
])

NEGATIVE_EMOJIS = set([
    '😢','😭','😰','😥','😓','😟','😕','🙁','☹️','😣','😖','😫','😩',
    '🥺','😤','😠','😡','🤬','😈','👿','💀','☠️','😱','😨','😧','😦',
    '😮','😯','😲','💔','😞','😔','😒','🙄','😑','😐','🤮','🤢','🤕',
    '😷','🤒','🤧','🥵','🥶','😵','😴','😪','🤥','😬','😵‍💫','🫠',
    '👎','💩','🤡','👹','👺','💣','🔥','⚡','😿','😾','🙀','🐍','🦂',
    '😑','💢','🔞','⛔','🚫','❌','❎','🆘','‼️','⁉️','🔴',
])

NEUTRAL_EMOJIS = set([
    '🤔','🤨','🧐','🤷','🤦','😐','😶','🙃','🤐','🤫','🤭','😏',
    '🫤','🫥','🫢','👀','👁️','🤞','🤙','🫱','🫲','👋','🫡','🤚',
    '✋','🖐️','🖖','☝️','🤟','🤘','🤙','💁','🙋','🧏',
    '⚠️','ℹ️','🔵','🟡','🟠','🟢','🟣','⚫','⚪','🔶','🔷',
    '📱','💻','📸','📷','📹','🎥','🎬','📺','📻','⌚','📞',
])


def _get_filtered_df(selected_user: str, df: pd.DataFrame) -> pd.DataFrame:
    """Filter by user if not 'Overall'."""
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df.copy()


# ── Existing functions (preserved + improved) ─────────────────────────────────

def fetch_stats(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    num_messeges = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    links = []
    url_pattern = r'https?://\S+|www\.\S+'
    for message in df['message']:
        links.extend(re.findall(url_pattern, message))

    media = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]

    return num_messeges, len(words), media, len(links)


def most_busy_user(df):
    x = df['users'].value_counts().head()
    df = round(((df['users'].value_counts()) / df.shape[0]) * 100, 2) \
         .reset_index().rename(columns={'users': 'Name', 'count': 'Percent'})
    return x, df


def create_wordcloud(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    temp = df[df['users'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]
    if temp.empty or temp['message'].str.cat(sep=' ').strip() == '':
        return None
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(temp['message'].str.cat(sep=' '))


def most_common_words(selected_user, df):
    try:
        with open('bengali_stop_words.txt', 'r', encoding='utf-8') as f:
            stop_words = set(f.read().split())
    except FileNotFoundError:
        stop_words = set()

    df = _get_filtered_df(selected_user, df)
    temp = df[df['users'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def monthly_timeline(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    return df.groupby('specific_date').count()['message'].reset_index()


def week_activity_map(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    df = _get_filtered_df(selected_user, df)
    return df.pivot_table(index='day_name', columns='period',
                          values='message', aggfunc='count').fillna(0)


# ── NEW: Emoji Analysis Functions ─────────────────────────────────────────────

def extract_all_emojis(selected_user: str, df: pd.DataFrame) -> list:
    """Return a flat list of every emoji found in messages."""
    df = _get_filtered_df(selected_user, df)
    temp = df[df['users'] != 'group_notification']
    all_emojis = []
    for msg in temp['message']:
        all_emojis.extend([e['emoji'] for e in emoji.emoji_list(msg)])
    return all_emojis


def emoji_frequency(selected_user: str, df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Return a DataFrame of the top N most-used emojis with counts."""
    all_emojis = extract_all_emojis(selected_user, df)
    if not all_emojis:
        return pd.DataFrame(columns=['emoji', 'count'])
    counts = Counter(all_emojis).most_common(top_n)
    return pd.DataFrame(counts, columns=['emoji', 'count'])


def emoji_per_user(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return a DataFrame: user → emoji_count (for Overall only)."""
    real = df[df['users'] != 'group_notification']
    rows = []
    for user, grp in real.groupby('users'):
        cnt = sum(len(emoji.emoji_list(m)) for m in grp['message'])
        rows.append({'user': user, 'emoji_count': cnt})
    result = pd.DataFrame(rows).sort_values('emoji_count', ascending=False).head(top_n)
    return result.reset_index(drop=True)


def emoji_sentiment_analysis(selected_user: str, df: pd.DataFrame) -> dict:
    """
    Classify each emoji as positive / negative / neutral and return counts + score.

    Returns:
        {
          'positive': int,
          'negative': int,
          'neutral':  int,
          'unknown':  int,
          'total':    int,
          'score':    float,   # -1.0 (very negative) to +1.0 (very positive)
          'label':    str,     # 'Very Positive' | 'Positive' | 'Neutral' | 'Negative' | 'Very Negative'
          'top_positive': list[tuple(emoji, count)],
          'top_negative': list[tuple(emoji, count)],
        }
    """
    all_emojis = extract_all_emojis(selected_user, df)

    pos = neg = neu = unk = 0
    pos_counts: Counter = Counter()
    neg_counts: Counter = Counter()

    for e in all_emojis:
        if e in POSITIVE_EMOJIS:
            pos += 1
            pos_counts[e] += 1
        elif e in NEGATIVE_EMOJIS:
            neg += 1
            neg_counts[e] += 1
        elif e in NEUTRAL_EMOJIS:
            neu += 1
        else:
            unk += 1

    total = pos + neg + neu + unk
    scored = pos - neg
    score = scored / max(total, 1)

    if score > 0.3:
        label = '😄 Very Positive'
    elif score > 0.05:
        label = '🙂 Positive'
    elif score > -0.05:
        label = '😐 Neutral'
    elif score > -0.3:
        label = '😟 Negative'
    else:
        label = '😢 Very Negative'

    return {
        'positive': pos,
        'negative': neg,
        'neutral': neu,
        'unknown': unk,
        'total': total,
        'score': round(score, 3),
        'label': label,
        'top_positive': pos_counts.most_common(5),
        'top_negative': neg_counts.most_common(5),
    }


def emoji_timeline(selected_user: str, df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly emoji usage count over time."""
    df = _get_filtered_df(selected_user, df)
    temp = df[df['users'] != 'group_notification'].copy()
    temp['emoji_count'] = temp['message'].apply(
        lambda m: len(emoji.emoji_list(m))
    )
    timeline = temp.groupby(['year', 'month', 'month_num'])['emoji_count'].sum().reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline[timeline['emoji_count'] > 0]