import streamlit as st


def check_password():
    if st.session_state.get("authenticated"):
        return

    st.title("Login")
    password = st.text_input("Password", type="password")

    if password:
        if password == st.secrets.get("password"):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password")
            st.stop()
    else:
        st.stop()
