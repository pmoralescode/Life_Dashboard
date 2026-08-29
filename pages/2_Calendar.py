import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import data
import auth

st.set_page_config(page_icon="📅", layout="wide")

auth.check_password()

PERSON_COLORS = data.PERSON_COLORS

data.init_db()

st.title("Calendar")

events_df = data.fetch_events()

calendar_events = []
for _, row in events_df.iterrows():
    row_end = row["date"] if pd.isna(row["end_date"]) else row["end_date"]
    end_exclusive = (pd.to_datetime(row_end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    calendar_events.append({
        "id": str(row["id"]),
        "title": row["title"],
        "start": row["date"],
        "end": end_exclusive,
        "color": PERSON_COLORS.get(row["person"], "#888888"),
        "extendedProps": {"person": row["person"]},
    })

calendar_key = f"calendar_{len(events_df)}"
state = calendar(events=calendar_events, options={"initialView": "dayGridMonth"}, key=calendar_key)

if state.get("callback") == "dateClick":
    st.session_state["selected_date"] = state["dateClick"]["date"][:10]
    st.session_state.pop("selected_event_id", None)

elif state.get("callback") == "eventClick":
    st.session_state["selected_event_id"] = int(state["eventClick"]["event"]["id"])
    st.session_state.pop("selected_date", None)

if "selected_date" in st.session_state:
    selected_date = st.session_state["selected_date"]
    st.subheader(f"Events on {selected_date}")

    event_end = events_df["end_date"].fillna(events_df["date"])
    day_events = events_df[(events_df["date"] <= selected_date) & (event_end >= selected_date)]
    if day_events.empty:
        st.write("No events yet.")
    else:
        st.dataframe(day_events, hide_index=True)

    with st.form("add_event_form"):
        title = st.text_input("Title")
        end_date = st.date_input("End date", value=pd.to_datetime(selected_date))
        person = st.selectbox("Person", ["Paul", "Camila"])
        submitted = st.form_submit_button("Add event")

    if submitted:
        data.add_event(selected_date, title, person, end_date=str(end_date))
        del st.session_state["selected_date"]
        st.rerun()

elif "selected_event_id" in st.session_state:
    event_id = st.session_state["selected_event_id"]
    matching = events_df[events_df["id"] == event_id]

    if matching.empty:
        del st.session_state["selected_event_id"]
        st.rerun()

    selected_row = matching.iloc[0]

    st.subheader(selected_row["title"])
    st.write(f"Person: {selected_row['person']}")

    person_options = ["Paul", "Camila"]
    current_person_index = (
        person_options.index(selected_row["person"]) if selected_row["person"] in person_options else 0
    )

    current_end_date = selected_row["date"] if pd.isna(selected_row["end_date"]) else selected_row["end_date"]

    with st.form("update_event_form"):
        new_title = st.text_input("Title", value=selected_row["title"])
        new_date = st.date_input("Date", value=pd.to_datetime(selected_row["date"]))
        new_end_date = st.date_input("End date", value=pd.to_datetime(current_end_date))
        new_person = st.selectbox("Person", person_options, index=current_person_index)
        col1, col2 = st.columns(2)
        update_clicked = col1.form_submit_button("Update")
        delete_clicked = col2.form_submit_button("Delete")

    if update_clicked:
        data.update_event(event_id, str(new_date), new_title, new_person, end_date=str(new_end_date))
        del st.session_state["selected_event_id"]
        st.rerun()

    if delete_clicked:
        data.delete_event(event_id)
        del st.session_state["selected_event_id"]
        st.rerun()

else:
    st.info("Click a date to add an event, or click an existing event to view/edit it.")
