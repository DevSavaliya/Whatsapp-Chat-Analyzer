import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns


# =========================
# SIDEBAR
# =========================

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file"
)


# =========================
# IF FILE IS UPLOADED
# =========================

if uploaded_file is not None:

    # =========================
    # READ FILE
    # =========================

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Process WhatsApp data
    df = preprocessor.preprocess(data)


    # =========================
    # SHOW COMPLETE DATAFRAME
    # =========================

    st.dataframe(
        df,
        height=500,
        use_container_width=True
    )


    # =========================
    # USER SELECTION
    # =========================

    user_list = df['user'].unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()

    user_list.insert(
        0,
        "Overall"
    )

    selected_user = st.sidebar.selectbox(
        "Show Analysis wrt",
        user_list
    )


    # =========================
    # SHOW ANALYSIS
    # =========================

    if st.sidebar.button(
        "Show Analysis"
    ):

        # =========================
        # BASIC STATISTICS
        # =========================

        (
            num_messages,
            words,
            num_media_messages,
            num_links
        ) = helper.fetch_stats(
            selected_user,
            df
        )

        st.title(
            "Top Statistics"
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.header(
                "Total Messages"
            )

            st.title(
                num_messages
            )


        with col2:

            st.header(
                "Total Words"
            )

            st.title(
                words
            )


        with col3:

            st.header(
                "Media Shared"
            )

            st.title(
                num_media_messages
            )


        with col4:

            st.header(
                "Links Shared"
            )

            st.title(
                num_links
            )


        # =========================
        # MONTHLY TIMELINE
        # =========================

        st.title(
            "Monthly Timeline"
        )

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        if not timeline.empty:

            fig, ax = plt.subplots(
                figsize=(12, 5)
            )

            ax.plot(
                timeline['time'],
                timeline['message'],
                color='green',
                marker='o'
            )

            ax.set_xlabel(
                "Month"
            )

            ax.set_ylabel(
                "Number of Messages"
            )

            plt.xticks(
                rotation="vertical"
            )

            plt.tight_layout()

            st.pyplot(
                fig
            )

        else:

            st.info(
                "No monthly timeline data available."
            )


        # =========================
        # DAILY TIMELINE
        # =========================

        st.title(
            "Daily Timeline"
        )

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        if not daily_timeline.empty:

            fig, ax = plt.subplots(
                figsize=(12, 5)
            )

            ax.plot(
                daily_timeline['only_date'],
                daily_timeline['message'],
                color='black'
            )

            ax.set_xlabel(
                "Date"
            )

            ax.set_ylabel(
                "Number of Messages"
            )

            plt.xticks(
                rotation="vertical"
            )

            plt.tight_layout()

            st.pyplot(
                fig
            )

        else:

            st.info(
                "No daily timeline data available."
            )


        # =========================
        # ACTIVITY MAP
        # =========================

        st.title(
            "Activity Map"
        )

        col1, col2 = st.columns(2)


        # =========================
        # MOST BUSY DAY
        # =========================

        with col1:

            st.subheader(
                "Most Busy Day"
            )

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            if not busy_day.empty:

                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )

                ax.bar(
                    busy_day.index.tolist(),
                    busy_day.values.tolist()
                )

                ax.set_xlabel(
                    "Day"
                )

                ax.set_ylabel(
                    "Number of Messages"
                )

                plt.xticks(
                    rotation="vertical"
                )

                plt.tight_layout()

                st.pyplot(
                    fig
                )


        # =========================
        # MOST BUSY MONTH
        # =========================

        with col2:

            st.subheader(
                "Most Busy Month"
            )

            busy_month = helper.month_activity_map(
                selected_user,
                df
            )

            if not busy_month.empty:

                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )

                ax.bar(
                    busy_month.index.tolist(),
                    busy_month.values.tolist(),
                    color='orange'
                )

                ax.set_xlabel(
                    "Month"
                )

                ax.set_ylabel(
                    "Number of Messages"
                )

                plt.xticks(
                    rotation="vertical"
                )

                plt.tight_layout()

                st.pyplot(
                    fig
                )

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # =========================
        # MOST BUSY USERS
        # =========================

        if selected_user == "Overall":

            st.title(
                "Most Busy Users"
            )

            x, _ = helper.most_busy_users(
                df
            )

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            ax.bar(
                x.index.tolist(),
                x.values.tolist(),
                color="red"
            )

            plt.xticks(
                rotation="vertical"
            )

            ax.set_xlabel(
                "Users"
            )

            ax.set_ylabel(
                "Number of Messages"
            )

            plt.tight_layout()

            st.pyplot(
                fig
            )


        # =========================
        # WORDCLOUD
        # =========================

        st.title(
            "WordCloud"
        )

        df_wc = helper.create_wordcloud(
            selected_user,
            df
        )

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        ax.imshow(
            df_wc.to_array()
        )

        ax.axis(
            "off"
        )

        plt.tight_layout()

        st.pyplot(
            fig
        )


        # =========================
        # MOST COMMON WORDS
        # =========================

        st.title(
            "Most Common Words"
        )

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        if not most_common_df.empty:

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            ax.bar(
                most_common_df['word'].tolist(),
                most_common_df['frequency'].tolist(),
                color='orange'
            )

            plt.xticks(
                rotation="vertical"
            )

            ax.set_xlabel(
                "Words"
            )

            ax.set_ylabel(
                "Frequency"
            )

            plt.tight_layout()

            st.pyplot(
                fig
            )

        else:

            st.info(
                "No meaningful words found."
            )


        # =========================
        # EMOJI ANALYSIS
        # =========================

        st.title(
            "Emoji Analysis"
        )

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        emoji_df = emoji_df.head(
            10
        ).copy()


        if not emoji_df.empty:

            col1, col2 = st.columns(
                [2, 1]
            )


            # =========================
            # PIE CHART
            # =========================

            with col1:

                fig, ax = plt.subplots(
                    figsize=(8, 8)
                )

                emoji_font = FontProperties(
                    fname=r"C:\Windows\Fonts\seguiemj.ttf"
                )

                wedges, texts, autotexts = ax.pie(
                    emoji_df['count'],
                    labels=emoji_df['emoji'],
                    autopct='%1.1f%%',
                    startangle=90,
                    pctdistance=0.65,
                    labeldistance=1.08,
                    textprops={
                        'fontsize': 16
                    }
                )


                for text in texts:

                    text.set_fontproperties(
                        emoji_font
                    )

                    text.set_fontsize(
                        18
                    )


                for autotext in autotexts:

                    autotext.set_fontsize(
                        12
                    )


                ax.axis(
                    'equal'
                )

                plt.tight_layout()

                st.pyplot(
                    fig
                )


            # =========================
            # EMOJI TABLE
            # =========================

            with col2:

                st.subheader(
                    "Emoji Frequency"
                )

                emoji_table = emoji_df.copy()

                emoji_table.columns = [
                    "Emoji",
                    "Frequency"
                ]

                st.dataframe(
                    emoji_table,
                    height=400,
                    use_container_width=True
                )


        else:

            st.info(
                "No emojis found in this chat."
            )