import streamlit as st
import preprocessor
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')

# Styling
plt.style.use('dark_background')
sns.set_theme(style='darkgrid')

# Color Palette
dark_color = '#6C5DD3'
secondary_color = '#434343'
background_color = '#0e0e10'

# Streamlit Page Config
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide",
    page_icon="💬"
)

# Sidebar
st.sidebar.title('📊 WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('📎 Choose a WhatsApp chat file')

# Main Title
st.markdown(
    "<h1 style='text-align: center; color: white;'>WhatsApp Chat Analyzer</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess_chat(data)

    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis for', user_list)

    if st.sidebar.button('Analyze'):
        st.markdown(f"<h2 style='color:{dark_color};'>Stats for: {selected_user}</h2>", unsafe_allow_html=True)

        # Top Stats
        total_messages, total_words, media_shared, links_shared = helpers.extract_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", total_messages)
        col2.metric("Words", total_words)
        col3.metric("Media", media_shared)
        col4.metric("Links", links_shared)

        st.markdown("---")

        # Monthly Timeline
        st.subheader("Monthly Timeline")
        timeline = helpers.monthly_timeline(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(timeline['date'], timeline['messages'], color=dark_color, linewidth=2)
            ax.set_xlabel("Month")
            ax.set_ylabel("Messages")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Daily Timeline
        st.subheader("Daily Timeline")
        daily_timeline = helpers.daily_timeline(selected_user, df)
        with col2:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color=dark_color, linewidth=2)
            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.markdown("---")
        st.subheader("Activity Breakdown")

        # Activity Graphs
        daily_activity, monthly_activity = helpers.activity(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Most Active Days**")
            fig, ax = plt.subplots()
            ax.bar(daily_activity.index, daily_activity.values, color=dark_color)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.markdown("**Most Active Months**")
            fig, ax = plt.subplots()
            ax.bar(monthly_activity.index, monthly_activity.values, color=dark_color)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Weekly Heatmap
        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helpers.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, cmap="mako", ax=ax, cbar=False, linewidths=0.5, linecolor='#2D2D2D')
        st.pyplot(fig)

        # Most Busy Users
        if selected_user == 'Overall':
            st.markdown("---")
            st.subheader("Most Active Users")
            msg_count, msg_percentage_df = helpers.most_busy_stats(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(msg_count.index, msg_count.values, color=dark_color)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(msg_percentage_df.style.background_gradient(cmap='Blues'))

        # Word Cloud
        st.markdown("---")
        st.subheader("Word Cloud")
        df_wc = helpers.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

        # Most Common Words
        st.subheader("Most Common Words")
        most_common_words_df = helpers.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_words_df)
        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_common_words_df['messages'], most_common_words_df['count'], color=dark_color)
            ax.set_xlabel("Count")
            st.pyplot(fig)

        # Emoji Analysis
        st.markdown("---")
        st.subheader("Most Common Emojis")
        df_emojis = helpers.emoji_count(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_emojis)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                df_emojis['count'].head(),
                labels=df_emojis['emojis'].head(),
                autopct="%0.2f",
                colors=['#6C5DD3', '#434343', '#5A5A5A', '#2D2D2D', '#1F1F1F']
            )
            st.pyplot(fig)

else:
    st.markdown("### 👈 Please upload a WhatsApp chat file to begin analysis.")
