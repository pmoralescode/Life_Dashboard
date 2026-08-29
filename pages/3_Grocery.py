import streamlit as st
import data
import auth

st.set_page_config(page_icon="🛒")

auth.check_password()

data.init_db()

st.title("Grocery List")

items_df = data.fetch_grocery_items()

with st.form("add_item_form"):
    item = st.text_input("Item")
    person = st.selectbox("Added by", ["Paul", "Camila"])
    store = st.selectbox("Store", ["Trader Joes", "Costco", "Supermarket", "Mall", "Amazon"])
    submitted = st.form_submit_button("Add")

if submitted and item:
    data.add_grocery_item(item, person, store)
    st.rerun()

st.subheader("List")

if items_df.empty:
    st.write("Nothing on the list yet.")
else:
    unchecked = items_df[items_df["checked"] == 0]
    checked = items_df[items_df["checked"] == 1]

    def render_row(row, is_bought):
        col1, col2, col3 = st.columns([0.5, 4.5, 1])
        is_checked = col1.checkbox("", value=is_bought, key=f"grocery_{row['id']}", label_visibility="collapsed")
        bg_color = data.PERSON_LIGHT_COLORS.get(row["person"], "#F0F0F0")
        col2.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:8px 12px; border-radius:8px;">
                {row['item']} — {row['store']} <span style="opacity:0.7;">({row['person']})</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if is_checked != is_bought:
            data.toggle_grocery_item(row["id"], is_checked)
            st.rerun()
        if col3.button("Delete", key=f"del_{row['id']}"):
            data.delete_grocery_item(row["id"])
            st.rerun()

    for _, row in unchecked.iterrows():
        render_row(row, is_bought=False)

    if not checked.empty:
        st.caption("Bought")
        for _, row in checked.iterrows():
            render_row(row, is_bought=True)
