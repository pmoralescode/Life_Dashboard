import streamlit as st
import pandas as pd
import altair as alt
import data
import auth

st.set_page_config(page_icon="🏠")

auth.check_password()

data.init_db()

st.title("Home")

events_df = data.fetch_events()
grocery_df = data.fetch_grocery_items()
expenses_df = data.fetch_expenses()
notes_df = data.fetch_notes()

today = pd.Timestamp.now().normalize()
upcoming = events_df.copy()
upcoming["date_parsed"] = pd.to_datetime(upcoming["date"])
upcoming = upcoming[upcoming["date_parsed"] >= today].sort_values("date_parsed")

st.subheader("Next Event")

if upcoming.empty:
    st.info("No upcoming events.")
else:
    next_event = upcoming.iloc[0]
    days_until = (next_event["date_parsed"] - today).days
    when_label = "Today" if days_until == 0 else "Tomorrow" if days_until == 1 else f"In {days_until} days"
    color = data.PERSON_COLORS.get(next_event["person"], "#888888")
    date_label = next_event["date_parsed"].strftime("%b %d")

    st.markdown(
        f"""
        <div style="background-color:{color}; color:white; padding:24px; border-radius:12px;">
            <div style="font-size:14px; opacity:0.85;">📅 {next_event['person']}</div>
            <div style="font-size:30px; font-weight:700; margin-top:4px;">{next_event['title']}</div>
            <div style="font-size:16px; margin-top:6px;">{date_label} — {when_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("This Month's Spending")

expenses_df["date_parsed"] = pd.to_datetime(expenses_df["date"])
this_month = expenses_df[
    (expenses_df["date_parsed"].dt.year == today.year) & (expenses_df["date_parsed"].dt.month == today.month)
]

if this_month.empty:
    st.write("No expenses logged this month yet.")
else:
    by_description = this_month.groupby("description", as_index=False)["amount"].sum()
    pie_chart = (
        alt.Chart(by_description)
        .mark_arc()
        .encode(theta="amount", color="description", tooltip=["description", "amount"])
    )
    st.altair_chart(pie_chart, use_container_width=True)

st.subheader("Grocery")

items_needed = int((grocery_df["checked"] == 0).sum()) if not grocery_df.empty else 0
st.metric("Items Needed", items_needed)

st.subheader("Notes")

if notes_df.empty:
    st.write("No notes yet.")
else:
    for _, row in notes_df.sort_values("created_at", ascending=False).head(5).iterrows():
        bg_color = data.PERSON_LIGHT_COLORS.get(row["person"], "#F0F0F0")
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:10px 14px; border-radius:8px; margin-bottom:6px;">
                <strong>{row['person']}</strong> ({data.format_timestamp(row['created_at'])}): {row['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )
