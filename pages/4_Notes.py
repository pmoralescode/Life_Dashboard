import streamlit as st
import pandas as pd
import data
import auth

st.set_page_config(page_icon="📝")

auth.check_password()

data.init_db()

st.title("Notes")

notes_df = data.fetch_notes()

with st.form("add_note_form"):
    note_text = st.text_input("Note")
    note_person = st.selectbox("From", ["Paul", "Camila"])
    submitted = st.form_submit_button("Add")

if submitted and note_text:
    data.add_note(note_text, note_person, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))
    st.rerun()

st.subheader("All Notes")

if notes_df.empty:
    st.write("No notes yet.")
else:
    for _, row in notes_df.sort_values("created_at", ascending=False).iterrows():
        col1, col2 = st.columns([5, 1])
        col1.write(f"**{row['person']}** ({data.format_timestamp(row['created_at'])}): {row['text']}")
        if col2.button("Delete", key=f"note_del_{row['id']}"):
            data.delete_note(row["id"])
            st.rerun()
