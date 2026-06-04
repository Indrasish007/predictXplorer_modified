import streamlit as st
import preprocessor
import helper
import sidebar

# Render Custom Sidebar
sidebar.render(current_page="whatsapp")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Global Animations & CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ── Keyframe Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 5px rgba(135,206,235,0.3); }
    50%       { box-shadow: 0 0 20px rgba(135,206,235,0.9), 0 0 40px rgba(135,206,235,0.4); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.5); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes rotateIn {
    from { opacity: 0; transform: rotate(-10deg) scale(0.8); }
    to   { opacity: 1; transform: rotate(0deg) scale(1); }
}
@keyframes barFill {
    from { width: 0; }
    to   { width: 100%; }
}
@keyframes borderPulse {
    0%, 100% { border-color: rgba(135,206,235,0.3); }
    50%       { border-color: rgba(135,206,235,1); }
}

/* ── Base ── */
* { font-family: 'Inter', sans-serif; }
.main { background-color: #0a0a0f; }

/* ── Page Title ── */
h1 {
    color: #87CEEB;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 2.8em;
    font-weight: 700;
    animation: fadeInUp 0.8s ease-out;
    background: linear-gradient(135deg, #87CEEB 0%, #ffffff 50%, #87CEEB 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite, fadeInUp 0.8s ease-out;
}
h2 { color: #87CEEB; animation: fadeInLeft 0.6s ease-out; }
h3 { color: #aad4f0; }

/* ── Nav Buttons ── */
.stButton>button {
    background: linear-gradient(135deg, #87CEEB, #5ba8cc);
    color: #0a0a0f;
    font-size: 1em;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease-out;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #357ABD, #1a5a9a);
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(135,206,235,0.4);
}
.stButton>button:active { transform: translateY(0px); }

/* ── Stat Cards ── */
.stat-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(135,206,235,0.3);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    animation: fadeInUp 0.7s ease-out, borderPulse 3s ease-in-out infinite;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: default;
}
.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 35px rgba(135,206,235,0.3);
}
.stat-icon { font-size: 2.2em; margin-bottom: 8px; display: block; animation: float 3s ease-in-out infinite; }
.stat-value {
    font-size: 2.4em;
    font-weight: 700;
    color: #87CEEB;
    animation: countUp 0.8s ease-out;
    display: block;
}
.stat-label { color: #8899aa; font-size: 0.9em; margin-top: 4px; display: block; }

/* ── Section Headers ── */
.section-header {
    background: linear-gradient(90deg, rgba(135,206,235,0.15) 0%, transparent 100%);
    border-left: 4px solid #87CEEB;
    border-radius: 0 8px 8px 0;
    padding: 10px 18px;
    margin: 20px 0 12px 0;
    animation: fadeInLeft 0.5s ease-out;
}
.section-header h2 {
    margin: 0;
    font-size: 1.4em;
    font-weight: 600;
    color: #87CEEB !important;
    -webkit-text-fill-color: #87CEEB !important;
    background: none;
    animation: none;
}

/* ── Sentiment Meter ── */
.sentiment-card {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2f4a 100%);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(135,206,235,0.2);
    animation: fadeInUp 0.9s ease-out;
    margin: 12px 0;
}
.sentiment-score {
    font-size: 3em;
    font-weight: 800;
    text-align: center;
    animation: countUp 1s ease-out;
}
.sentiment-bar-wrap {
    background: rgba(255,255,255,0.1);
    border-radius: 50px;
    height: 16px;
    overflow: hidden;
    margin: 10px 0;
}
.sentiment-bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 1.5s ease;
}
.emoji-chip {
    display: inline-block;
    background: rgba(135,206,235,0.12);
    border: 1px solid rgba(135,206,235,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    margin: 4px;
    font-size: 1.1em;
    animation: fadeInUp 0.5s ease-out;
    transition: transform 0.2s;
}
.emoji-chip:hover { transform: scale(1.15); }

/* ── Success / Info overrides ── */
[data-testid="stAlert"] { border-radius: 12px; animation: fadeInUp 0.4s ease; }
[data-testid="stAppViewContainer"] { padding-top: 0.5rem; }

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💬 WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8899aa;font-size:1.1em;margin-top:-10px;'>Upload your chat export to unlock deep insights & emoji sentiment</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Choose a WhatsApp chat export (.txt)", type=['txt'])

try:
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        try:
            data = bytes_data.decode("utf-8")
        except UnicodeDecodeError:
            data = bytes_data.decode("latin-1")

        df = preprocessor.preprocess(data)

        # Animated success banner
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d2b0d,#1a3d1a);border:1px solid #2ecc71;
                    border-radius:12px;padding:14px 20px;animation:fadeInUp 0.5s ease-out;margin:10px 0;">
            <span style="color:#2ecc71;font-size:1.1em;font-weight:600;">
                ✅ Parsed <strong style="color:#7fff7f">{len(df):,}</strong> messages from
                <strong style="color:#7fff7f">{df['users'].nunique()-1}</strong> participants
            </span>
        </div>
        """, unsafe_allow_html=True)

        user_list = df["users"].unique().tolist()
        if "group_notification" in user_list:
            user_list.remove("group_notification")
        user_list = [u for u in user_list if u.strip()]
        user_list.sort()
        user_list.insert(0, "Overall")

        st.sidebar.markdown("<h2 style='color:#87CEEB'>⚙️ Analysis</h2>", unsafe_allow_html=True)
        selected_user = st.sidebar.selectbox("Analyse chat for", user_list)

        if st.sidebar.button('🔍 Show Analysis', use_container_width=True):

            # ── 1. TOP STATS ──────────────────────────────────────────────────
            num_msgs, words, media, num_links = helper.fetch_stats(selected_user, df)

            st.markdown("""<div class="section-header"><h2>📊 Top Statistics</h2></div>""",
                        unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            cards = [
                (c1, "💬", f"{num_msgs:,}", "Total Messages"),
                (c2, "📝", f"{words:,}", "Total Words"),
                (c3, "🖼️", f"{media:,}", "Media Shared"),
                (c4, "🔗", f"{num_links:,}", "Links Shared"),
            ]
            for col, icon, value, label in cards:
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <span class="stat-icon">{icon}</span>
                        <span class="stat-value">{value}</span>
                        <span class="stat-label">{label}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── 2. EMOJI SENTIMENT ANALYSIS ───────────────────────────────────
            st.markdown("""<div class="section-header"><h2>🎭 Emoji Sentiment Analysis</h2></div>""",
                        unsafe_allow_html=True)

            sentiment = helper.emoji_sentiment_analysis(selected_user, df)

            if sentiment['total'] == 0:
                st.info("😶 No emojis found in the selected chat. Try selecting 'Overall'.")
            else:
                score = sentiment['score']
                # Map score (-1 to 1) to percentage (0 to 100)
                score_pct = int((score + 1) / 2 * 100)

                # Color by sentiment
                if score > 0.15:
                    bar_color = "linear-gradient(90deg,#27ae60,#2ecc71)"
                    score_color = "#2ecc71"
                elif score > -0.15:
                    bar_color = "linear-gradient(90deg,#f39c12,#f1c40f)"
                    score_color = "#f1c40f"
                else:
                    bar_color = "linear-gradient(90deg,#c0392b,#e74c3c)"
                    score_color = "#e74c3c"

                scol1, scol2 = st.columns([1.2, 1])

                with scol1:
                    top_pos_html = "".join(
                        f'<span class="emoji-chip">{e} \u00d7{c}</span>'
                        for e, c in sentiment["top_positive"]
                    ) or '<span style="color:#8899aa">None found</span>'
                    top_neg_html = "".join(
                        f'<span class="emoji-chip">{e} \u00d7{c}</span>'
                        for e, c in sentiment["top_negative"]
                    ) or '<span style="color:#8899aa">None found</span>'
                    card_html = (
                        f'<div class="sentiment-card">'
                        f'<div style="text-align:center;margin-bottom:16px;">'
                        f'<span class="sentiment-score" style="color:{score_color}">{sentiment["label"]}</span>'
                        f'<p style="color:#8899aa;margin:4px 0;">Sentiment Score: '
                        f'<strong style="color:{score_color}">{score:+.3f}</strong>'
                        f'&nbsp;(scale: &minus;1.0 to +1.0)</p>'
                        f'</div>'
                        f'<p style="color:#aaa;margin:6px 0 2px;">Sentiment Meter</p>'
                        f'<div class="sentiment-bar-wrap">'
                        f'<div class="sentiment-bar-fill" style="width:{score_pct}%;background:{bar_color};"></div>'
                        f'</div>'
                        f'<div style="display:flex;justify-content:space-between;margin-top:12px;">'
                        f'<div style="text-align:center;flex:1;padding:8px;background:rgba(46,204,113,0.1);border-radius:10px;margin:4px;">'
                        f'<div style="font-size:1.5em;">\U0001f604</div>'
                        f'<div style="color:#2ecc71;font-size:1.3em;font-weight:700;">{sentiment["positive"]}</div>'
                        f'<div style="color:#8899aa;font-size:0.8em;">Positive</div>'
                        f'</div>'
                        f'<div style="text-align:center;flex:1;padding:8px;background:rgba(241,196,15,0.1);border-radius:10px;margin:4px;">'
                        f'<div style="font-size:1.5em;">\U0001f610</div>'
                        f'<div style="color:#f1c40f;font-size:1.3em;font-weight:700;">{sentiment["neutral"]}</div>'
                        f'<div style="color:#8899aa;font-size:0.8em;">Neutral</div>'
                        f'</div>'
                        f'<div style="text-align:center;flex:1;padding:8px;background:rgba(231,76,60,0.1);border-radius:10px;margin:4px;">'
                        f'<div style="font-size:1.5em;">\U0001f622</div>'
                        f'<div style="color:#e74c3c;font-size:1.3em;font-weight:700;">{sentiment["negative"]}</div>'
                        f'<div style="color:#8899aa;font-size:0.8em;">Negative</div>'
                        f'</div>'
                        f'</div>'
                        f'<div style="margin-top:16px;">'
                        f'<p style="color:#7fff7f;margin:4px 0;">\U0001f3c6 Top Positive Emojis:</p>'
                        f'{top_pos_html}'
                        f'</div>'
                        f'<div style="margin-top:10px;">'
                        f'<p style="color:#ff7f7f;margin:4px 0;">\U0001f53b Top Negative Emojis:</p>'
                        f'{top_neg_html}'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

                with scol2:
                    # Donut chart for sentiment breakdown
                    pie_data = {
                        'Positive': sentiment['positive'],
                        'Neutral': sentiment['neutral'],
                        'Negative': sentiment['negative'],
                    }
                    fig_pie = go.Figure(go.Pie(
                        labels=list(pie_data.keys()),
                        values=list(pie_data.values()),
                        hole=0.55,
                        marker=dict(colors=['#2ecc71', '#f1c40f', '#e74c3c'],
                                    line=dict(color='#0a0a0f', width=3)),
                        textinfo='label+percent',
                        textfont=dict(color='white', size=13),
                    ))
                    fig_pie.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        showlegend=False,
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=300,
                        annotations=[dict(
                            text=f"<b>{sentiment['total']}</b><br>emojis",
                            x=0.5, y=0.5, font_size=16, showarrow=False,
                            font=dict(color='#87CEEB')
                        )],
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            # ── 3. EMOJI FREQUENCY ────────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>🔢 Top Emojis Used</h2></div>""",
                        unsafe_allow_html=True)

            emoji_df = helper.emoji_frequency(selected_user, df, top_n=15)
            if emoji_df.empty:
                st.info("No emojis found.")
            else:
                fig_emoji = px.bar(
                    emoji_df, x='emoji', y='count',
                    text='count',
                    color='count',
                    color_continuous_scale=['#1a2f4a', '#87CEEB', '#ffffff'],
                )
                fig_emoji.update_traces(textposition='outside', textfont=dict(color='white', size=13))
                fig_emoji.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(13,27,42,0.8)',
                    font=dict(color='white'),
                    xaxis=dict(title='Emoji', tickfont=dict(size=18)),
                    yaxis=dict(title='Count', gridcolor='rgba(135,206,235,0.1)'),
                    coloraxis_showscale=False,
                    margin=dict(t=20, b=10),
                    height=380,
                )
                st.plotly_chart(fig_emoji, use_container_width=True)

            # ── 4. EMOJI PER USER (Overall only) ──────────────────────────────
            if selected_user == "Overall":
                st.markdown("""<div class="section-header"><h2>👤 Emoji Usage by Person</h2></div>""",
                            unsafe_allow_html=True)
                epu = helper.emoji_per_user(df)
                if not epu.empty:
                    fig_epu = px.bar(
                        epu, x='emoji_count', y='user', orientation='h',
                        text='emoji_count',
                        color='emoji_count',
                        color_continuous_scale=['#1a2f4a', '#87CEEB'],
                    )
                    fig_epu.update_traces(textposition='outside', textfont=dict(color='white'))
                    fig_epu.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(13,27,42,0.8)',
                        font=dict(color='white'),
                        yaxis=dict(title='', autorange='reversed'),
                        xaxis=dict(title='Emoji Count', gridcolor='rgba(135,206,235,0.1)'),
                        coloraxis_showscale=False,
                        margin=dict(t=10, b=10),
                        height=max(250, len(epu) * 40),
                    )
                    st.plotly_chart(fig_epu, use_container_width=True)

            # ── 5. EMOJI USAGE TIMELINE ───────────────────────────────────────
            emoji_tl = helper.emoji_timeline(selected_user, df)
            if not emoji_tl.empty:
                st.markdown("""<div class="section-header"><h2>📅 Emoji Activity Over Time</h2></div>""",
                            unsafe_allow_html=True)
                fig_etl = px.area(
                    emoji_tl, x='time', y='emoji_count',
                    color_discrete_sequence=['#87CEEB'],
                )
                fig_etl.update_traces(fill='tozeroy',
                                      fillcolor='rgba(135,206,235,0.15)',
                                      line=dict(color='#87CEEB', width=2))
                fig_etl.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(13,27,42,0.8)',
                    font=dict(color='white'),
                    xaxis=dict(title='Month', tickangle=45,
                               gridcolor='rgba(135,206,235,0.1)'),
                    yaxis=dict(title='Emojis Used',
                               gridcolor='rgba(135,206,235,0.1)'),
                    margin=dict(t=10, b=60),
                    height=320,
                )
                st.plotly_chart(fig_etl, use_container_width=True)

            # ── 6. TIMELINES ──────────────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>📆 Monthly Message Timeline</h2></div>""",
                        unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            fig_mt = px.line(timeline, x='time', y='message',
                             markers=True,
                             color_discrete_sequence=['#87CEEB'])
            fig_mt.update_traces(line=dict(width=2.5),
                                  marker=dict(size=7, color='white',
                                              line=dict(color='#87CEEB', width=2)))
            fig_mt.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,27,42,0.8)',
                font=dict(color='white'),
                xaxis=dict(tickangle=45, gridcolor='rgba(135,206,235,0.1)'),
                yaxis=dict(gridcolor='rgba(135,206,235,0.1)'),
                margin=dict(t=10, b=60), height=320,
            )
            st.plotly_chart(fig_mt, use_container_width=True)

            st.markdown("""<div class="section-header"><h2>📅 Daily Message Timeline</h2></div>""",
                        unsafe_allow_html=True)
            daily_tl = helper.daily_timeline(selected_user, df)
            fig_dt = px.bar(daily_tl, x='specific_date', y='message',
                            color_discrete_sequence=['#2ecc71'])
            fig_dt.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,27,42,0.8)',
                font=dict(color='white'),
                xaxis=dict(tickangle=45, gridcolor='rgba(135,206,235,0.1)'),
                yaxis=dict(gridcolor='rgba(135,206,235,0.1)'),
                margin=dict(t=10, b=60), height=320,
            )
            st.plotly_chart(fig_dt, use_container_width=True)

            # ── 7. ACTIVITY MAP ───────────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>🗓️ Activity Map</h2></div>""",
                        unsafe_allow_html=True)
            ac1, ac2 = st.columns(2)
            with ac1:
                busy_day = helper.week_activity_map(selected_user, df)
                fig_bd = px.bar(x=busy_day.index, y=busy_day.values,
                                labels={'x': 'Day', 'y': 'Messages'},
                                title="Most Busy Day",
                                color=busy_day.values,
                                color_continuous_scale=['#1a2f4a', '#87CEEB'])
                fig_bd.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,27,42,0.8)',
                    font=dict(color='white'), coloraxis_showscale=False,
                    title_font=dict(color='#87CEEB'), margin=dict(t=40,b=10), height=280,
                )
                st.plotly_chart(fig_bd, use_container_width=True)

            with ac2:
                busy_month = helper.month_activity_map(selected_user, df)
                fig_bm = px.bar(x=busy_month.index, y=busy_month.values,
                                labels={'x': 'Month', 'y': 'Messages'},
                                title="Most Busy Month",
                                color=busy_month.values,
                                color_continuous_scale=['#1a2f4a', '#e74c3c'])
                fig_bm.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,27,42,0.8)',
                    font=dict(color='white'), coloraxis_showscale=False,
                    title_font=dict(color='#e74c3c'), margin=dict(t=40,b=10), height=280,
                )
                st.plotly_chart(fig_bm, use_container_width=True)

            # ── 8. HEATMAP ────────────────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>🌡️ Weekly Activity Heatmap</h2></div>""",
                        unsafe_allow_html=True)
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig_hm, ax = plt.subplots(figsize=(12, 4),
                                       facecolor='#0d1b2a')
            ax.set_facecolor('#0d1b2a')
            sns.heatmap(user_heatmap, ax=ax, cmap='YlOrRd',
                        linewidths=0.5, linecolor='#0d1b2a')
            ax.tick_params(colors='white', labelsize=9)
            plt.tight_layout()
            st.pyplot(fig_hm, use_container_width=True)
            plt.close(fig_hm)

            # ── 9. BUSY USERS (Overall only) ──────────────────────────────────
            if selected_user == "Overall":
                st.markdown("""<div class="section-header"><h2>👥 Most Active Members</h2></div>""",
                            unsafe_allow_html=True)
                x, new_df = helper.most_busy_user(df)
                uc1, uc2 = st.columns(2)
                with uc1:
                    fig_pie2 = px.pie(
                        values=x.values, names=x.index,
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        hole=0.4,
                    )
                    fig_pie2.update_traces(textfont=dict(color='white', size=11))
                    fig_pie2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        margin=dict(t=10, b=10), height=300,
                        legend=dict(font=dict(color='white')),
                    )
                    st.plotly_chart(fig_pie2, use_container_width=True)
                with uc2:
                    st.markdown("<p style='color:#87CEEB;font-weight:600;'>Chat Participation %</p>",
                                unsafe_allow_html=True)
                    st.dataframe(new_df, use_container_width=True, height=280)

            # ── 10. WORD CLOUD ────────────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>☁️ Word Cloud</h2></div>""",
                        unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc is not None:
                fig_wc, ax = plt.subplots(figsize=(10, 5), facecolor='#0d1b2a')
                ax.imshow(df_wc)
                ax.axis('off')
                plt.tight_layout(pad=0)
                st.pyplot(fig_wc, use_container_width=True)
                plt.close(fig_wc)
            else:
                st.info("Not enough text to generate a word cloud.")

            # ── 11. MOST COMMON WORDS ─────────────────────────────────────────
            st.markdown("""<div class="section-header"><h2>🔤 Most Common Words</h2></div>""",
                        unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)
            if not most_common_df.empty:
                fig_words = px.bar(
                    most_common_df, x=1, y=0, orientation='h',
                    labels={'1': 'Count', '0': 'Word'},
                    color=1,
                    color_continuous_scale=['#1a2f4a', '#87CEEB', '#ffffff'],
                    text=1,
                )
                fig_words.update_traces(textposition='outside',
                                         textfont=dict(color='white'))
                fig_words.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(13,27,42,0.8)',
                    font=dict(color='white'),
                    yaxis=dict(autorange='reversed',
                               gridcolor='rgba(135,206,235,0.1)'),
                    xaxis=dict(gridcolor='rgba(135,206,235,0.1)'),
                    coloraxis_showscale=False,
                    margin=dict(t=10, b=10),
                    height=480,
                )
                st.plotly_chart(fig_words, use_container_width=True)

except UnicodeDecodeError:
    st.error("❌ Could not read the file encoding. Try saving the chat export as UTF-8 and re-uploading.")
except ValueError as e:
    st.error(f"❌ Could not parse the chat file: {e}")
    st.info("""
    **Supported export formats:**
    - **Android**: `DD/MM/YY, HH:MM - Name: Message`
    - **Android 12h**: `DD/MM/YY, HH:MM AM/PM - Name: Message`
    - **iOS**: `[DD/MM/YY, HH:MM:SS] Name: Message`

    **How to export:** WhatsApp → Open Chat → ⋮ Menu → More → Export Chat → Without Media
    """)
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    import traceback
    st.code(traceback.format_exc(), language='python')