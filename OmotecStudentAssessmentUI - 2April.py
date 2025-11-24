import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os

# Constants
CSV_FILE_PATH = 'C:\\Users\\OMOLP091\\Downloads\\STUDENT_ASSESSMENT\\Final Culmination_AI_Blocks_1.csv'
USERNAME = "omotec"
PASSWORD = "omotec"

# Updated column headers
COLUMNS = [
    'Quiz Name', 'Course Name', 'Name', 'E-mail', 'Test Date',
    'Marks', 'Total Mark', 'Grade Range', 'Percentage', 'Passing Status'
]

# Create file with headers if missing
def create_csv_file():
    if not os.path.isfile(CSV_FILE_PATH):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE_PATH, index=False)

# Insert data into CSV
def insert_data(*args):
    df = pd.read_csv(CSV_FILE_PATH)
    new_data = dict(zip(COLUMNS, args))
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE_PATH, index=False)

# Fetch data
def fetch_data():
    if os.path.isfile(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    return pd.DataFrame(columns=COLUMNS)

# Login Screen
def login_screen():
    # Custom header with title and logo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC INTERNAL</h2>", unsafe_allow_html=True)
    with col2:
        image_path = "C:/Users/OMOLP091/Pictures/NEW LOGO - OMOTEC.png"
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.warning("Logo image not found at the specified path.")

    st.markdown("🔐 STUDENT ASSESSMENT LOGIN")
    #st.title("🔐 STUDENT ASSESSMENT LOGIN")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "Student Assessment Form"
        else:
            st.error("Invalid credentials")

# Assessment Form
def assessment_form():
    # Custom header with title and logo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC INTERNAL</h2>", unsafe_allow_html=True)
    with col2:
        image_path = "C:/Users/OMOLP091/Pictures/NEW LOGO - OMOTEC.png"
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.warning("Logo image not found at the specified path.")

    st.markdown("### 📝 STUDENT ASSESSMENT FORM")
    create_csv_file()

    quiz_name = st.text_input("Quiz Name")
    course_name = st.text_input("Course Name")
    name = st.text_input("Student Name")
    email = st.text_input("E-mail")
    test_date = st.date_input("Test Date")
    marks = st.number_input("Marks", min_value=0)
    total_mark = st.number_input("Total Mark", min_value=1)
    grade_range = st.text_input("Grade Range")
    percentage = (marks / total_mark) * 100 if total_mark > 0 else 0
    passing_status = st.selectbox("Passing Status", ["Pass", "Fail"])

    if st.button("Submit"):
        if name and email:
            insert_data(
                quiz_name, course_name, name, email, str(test_date),
                marks, total_mark, grade_range, percentage, passing_status
            )
            st.success("✅ Data submitted successfully!")
        else:
            st.error("Please fill in all required fields.")


# Table Display Page
def show_assessments():
    # Custom header with title and logo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC INTERNAL</h2>", unsafe_allow_html=True)
    with col2:
        image_path = "C:/Users/OMOLP091/Pictures/NEW LOGO - OMOTEC.png"
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.warning("Logo image not found at the specified path.")

    st.markdown("📊 SHOW STUDENT ASSESSMENTS MASTER SHEET")
    #st.title("📊 SHOW STUDENT ASSESSMENTS MASTER SHEET")
    df = fetch_data()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No data found.")

    df = fetch_data()

    if df.empty:
        st.warning("No data to display.")
        return
    
    
# Display Chart Page
def display_chart():
    # Custom header with title and logo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC INTERNAL</h2>", unsafe_allow_html=True)
    with col2:
        image_path = "C:/Users/OMOLP091/Pictures/NEW LOGO - OMOTEC.png"
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.warning("Logo image not found at the specified path.")

    st.markdown("📈 DISPLAY STUDENT ASSESSMENTS")
    #st.title("📈 DISPLAY STUDENT ASSESSMENTS")
    df = fetch_data()

    if df.empty:
        st.warning("No data to display.")
        return

    st.sidebar.markdown("### Filter Options")
    filters = {}
    for col in df.columns:
        options = ['All'] + sorted(df[col].dropna().astype(str).unique())
        selected = st.sidebar.selectbox(f"Filter by {col}", options, key=col)
        if selected != 'All':
            filters[col] = selected

    filtered_df = df.copy()
    for col, value in filters.items():
        filtered_df = filtered_df[filtered_df[col].astype(str) == value]

    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button("📥 Download Filtered Data (CSV)", csv_buffer.getvalue(), file_name="filtered_data.csv", mime="text/csv")

    numeric_cols = ['Quiz Name', 'Course Name','Student Name','E-mail','Test Date','Marks','Total Mark','Grade Range','Percentage','Passing Status']
    available_cols = [col for col in numeric_cols if col in filtered_df.columns]

    if not available_cols:
        st.warning("No numeric columns available for charting.")
        return

    selected_x = st.selectbox("X-Axis", available_cols)
    selected_y = st.selectbox("Y-Axis", available_cols, index=1 if len(available_cols) > 1 else 0)

    chart_types = [
        "Line Plot", "Bar Plot", "Box Plot", "Violin Plot", "Strip Plot",
        "Swarm Plot", "Histogram", "KDE Plot", "Heatmap (Correlation)", "Joint Plot"
    ]
    selected_chart = st.selectbox("Select Chart Type", chart_types)

    try:
        if selected_chart == "Line Plot":
            fig, ax = plt.subplots()
            sns.lineplot(data=filtered_df, x=selected_x, y=selected_y, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Bar Plot":
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x=selected_x, y=selected_y, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Box Plot":
            fig, ax = plt.subplots()
            sns.boxplot(data=filtered_df, x=selected_x, y=selected_y, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Violin Plot":
            fig, ax = plt.subplots()
            sns.violinplot(data=filtered_df, x=selected_x, y=selected_y, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Strip Plot":
            fig, ax = plt.subplots()
            sns.stripplot(data=filtered_df, x=selected_x, y=selected_y, jitter=True, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Swarm Plot":
            fig, ax = plt.subplots()
            sns.swarmplot(data=filtered_df, x=selected_x, y=selected_y, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Histogram":
            fig, ax = plt.subplots()
            sns.histplot(data=filtered_df[selected_x], kde=False, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "KDE Plot":
            fig, ax = plt.subplots()
            sns.kdeplot(data=filtered_df[selected_x], ax=ax, fill=True)
            st.pyplot(fig)

        elif selected_chart == "Heatmap (Correlation)":
            corr = filtered_df[available_cols].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Joint Plot":
            fig = sns.jointplot(data=filtered_df, x=selected_x, y=selected_y, kind="scatter")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error generating {selected_chart}: {e}")

# Navigation
def sidebar_navigation():
    pages = {
        "Student Assessment Form": assessment_form,
        "Show Assessments": show_assessments,
        "Display Student Assessments": display_chart
    }

    choice = st.sidebar.radio("📚 Navigation", list(pages.keys()))
    st.session_state.page = choice
    pages[choice]()

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

# App launch
if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_navigation()