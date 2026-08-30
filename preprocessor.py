import re
import pandas as pd


def preprocess(data):

    # Supports common WhatsApp export formats:
    # 17/08/25, 04:30 PM -
    # 17/08/2025, 04:30 PM -
    # 17/08/25, 16:30 -
    # 17/08/2025, 16:30 -
    # 17.08.25, 16:30 -
    # 17.08.2025, 16:30 -

    pattern = (
        r'\d{1,2}[\/\.]\d{1,2}[\/\.]\d{2,4}'
        r',\s'
        r'\d{1,2}:\d{2}'
        r'(?:\s?[apAP][mM])?'
        r'\s-\s'
    )

    messages = re.split(
        pattern,
        data
    )[1:]

    dates = re.findall(
        pattern,
        data
    )

    # If no WhatsApp messages were detected
    if len(messages) == 0 or len(dates) == 0:

        return pd.DataFrame(
            columns=[
                'date',
                'user',
                'message',
                'only_date',
                'year',
                'month_num',
                'month',
                'day',
                'day_name',
                'hour',
                'minute',
                'period'
            ]
        )

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # =========================
    # CONVERT DATE
    # =========================

    df['message_date'] = (
        df['message_date']
        .astype(str)
        .str.replace(
            ' - ',
            '',
            regex=False
        )
    )

    # Try automatic date parsing
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        dayfirst=True,
        errors='coerce'
    )

    # Remove invalid dates
    df = df.dropna(
        subset=['message_date']
    ).reset_index(
        drop=True
    )

    df.rename(
        columns={
            'message_date': 'date'
        },
        inplace=True
    )

    # =========================
    # SEPARATE USERS & MESSAGES
    # =========================

    users = []
    message_list = []

    for message in df['user_message']:

        entry = re.split(
            r'([\w\W]+?):\s',
            message,
            maxsplit=1
        )

        if len(entry) >= 3:

            users.append(
                entry[1]
            )

            message_list.append(
                entry[2]
            )

        else:

            users.append(
                'group_notification'
            )

            message_list.append(
                entry[0]
            )

    df['user'] = users
    df['message'] = message_list

    df.drop(
        columns=['user_message'],
        inplace=True
    )

    # =========================
    # DATE FEATURES
    # =========================

    df['only_date'] = (
        df['date'].dt.date
    )

    df['year'] = (
        df['date'].dt.year
    )

    df['month_num'] = (
        df['date'].dt.month
    )

    df['month'] = (
        df['date'].dt.month_name()
    )

    df['day'] = (
        df['date'].dt.day
    )

    df['day_name'] = (
        df['date'].dt.day_name()
    )

    df['hour'] = (
        df['date'].dt.hour
    )

    df['minute'] = (
        df['date'].dt.minute
    )

    # =========================
    # TIME PERIOD
    # =========================

    period = []

    for hour in df['hour']:

        if hour == 23:

            period.append(
                '23-00'
            )

        elif hour == 0:

            period.append(
                '00-01'
            )

        else:

            period.append(
                str(hour)
                + "-"
                + str(hour + 1)
            )

    df['period'] = period

    return df