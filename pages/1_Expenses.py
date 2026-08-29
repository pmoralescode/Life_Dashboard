import streamlit as st
import pandas as pd
import data
import auth

st.set_page_config(page_icon="💰")

auth.check_password()

data.init_db()

st.title("Expenses")

df = data.fetch_expenses()
display_df = df.drop(columns=["id"]).copy()
display_df["date"] = pd.to_datetime(display_df["date"])
display_df["amount"] = display_df["amount"].round(2)
display_df["amount_paid"] = display_df["amount_paid"].round(2)
display_df["remaining"] = (display_df["amount"] - display_df["amount_paid"]).round(2)


def highlight_unpaid(row):
    if row["amount_paid"] < row["amount"]:
        return ["background-color: #FDE2E2"] * len(row)
    return [""] * len(row)


def format_amount(x):
    if x == int(x):
        return str(int(x))
    return f"{x:.2f}".rstrip("0").rstrip(".")


styled = display_df.style.apply(highlight_unpaid, axis=1).format(
    {"amount": format_amount, "amount_paid": format_amount, "remaining": format_amount}
)

st.dataframe(
    styled,
    hide_index=True,
    column_config={
        "date": st.column_config.DateColumn("Date", format="MMM DD"),
        "description": st.column_config.Column("Description"),
        "amount": st.column_config.Column("Amount"),
        "amount_paid": st.column_config.Column("Amount Paid"),
        "remaining": st.column_config.Column("Remaining"),
    },
)

st.subheader("Manage expenses")

action = st.radio("Action", ["Add", "Update", "Delete", "Clear All"], horizontal=True)

if action == "Add":
    with st.form("expense_form"):
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add")

    if submitted:
        data.add_expense(str(date), description, amount)
        st.rerun()

elif action == "Update":
    expense_labels = {
        row["id"]: f"{row['description']} - {pd.to_datetime(row['date']).strftime('%b %d')}" for _, row in df.iterrows()
    }
    expense_id = st.selectbox("Select expense", options=list(expense_labels.keys()), format_func=lambda i: expense_labels[i])
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
    expense_labels = {
        row["id"]: f"{row['description']} - {pd.to_datetime(row['date']).strftime('%b %d')}" for _, row in df.iterrows()
    }
    expense_id = st.selectbox("Select expense", options=list(expense_labels.keys()), format_func=lambda i: expense_labels[i])

    with st.form("expense_form"):
        submitted = st.form_submit_button("Delete")

    if submitted:
        data.delete_expense(expense_id)
        st.rerun()

elif action == "Clear All":
    st.warning(f"This will permanently delete all {len(df)} expense(s). This cannot be undone.")
    confirm_text = st.text_input('Type "delete" to confirm')

    if st.button("Clear All Expenses", disabled=(confirm_text != "delete")):
        data.clear_expenses()
        st.rerun()