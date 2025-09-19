import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

# Login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state['logged_in'] = True
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")
else:
    st.title("Employee Management System")
    menu = ["Add Employee", "View Employees"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Employee":
        st.subheader("Add Employee")
        name = st.text_input("Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
        salary = st.number_input("Salary", min_value=0.0)
        if st.button("Add"):
            data = {"name": name, "email": email, "department": department, "salary": salary}
            res = requests.post(f"{BASE_URL}/employees", json=data)
            if res.status_code == 201:
                st.success("Employee added successfully!")

    if choice == "View Employees":
        res = requests.get(f"{BASE_URL}/employees")
        employees = res.json()
        df = pd.DataFrame(employees)
        st.dataframe(df)
        st.download_button("Export CSV", df.to_csv(index=False), "employees.csv")
