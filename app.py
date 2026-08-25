import streamlit as st
import pandas as pd
import data

data.init_db()

st.title("Expenses")

df = data.fetch_expenses()
display_df = df.copy()
display_df["date"] = pd.to_datetime(display_df["date"])
st.dataframe(
    display_df,
    hide_index=True,
    column_config={"date": st.column_config.DateColumn("Date", format="MMM DD")},
)

st.subheader("Manage expenses")

action = st.radio("Action", ["Add", "Update", "Delete"], horizontal=True)

if action == "Add":
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add")

    if submitted:
        data.add_expense(str(date), category, amount)
        st.rerun()

elif action == "Update":
    expense_id = st.selectbox("Select expense id", df["id"])
    selected_row = df[df["id"] == expense_id].iloc[0]

    with st.form("expense_form"):
        new_amount = st.number_input("Amount", min_value=0.0, step=1.0, value=float(selected_row["amount"]))
        new_amount_paid = st.number_input(
            "Amount Paid", min_value=0.0, step=1.0, value=float(selected_row["amount_paid"])
        )
        submitted = st.form_submit_button("Update")

    if submitted:
        data.update_expense(expense_id, new_amount, new_amount_paid)
        st.rerun()

elif action == "Delete":
    expense_id = st.selectbox("Select expense id", df["id"])

    with st.form("expense_form"):
        submitted = st.form_submit_button("Delete")

    if submitted:
        data.delete_expense(expense_id)
        st.rerun()
