import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os
import base64

# Constants
CSV_FILE_PATH = 'C:\\Users\\OMOLP091\\Downloads\\STUDENT_ASSESSMENT\\Final Culmination_AI_Blocks_1.csv'
USERNAME = "omotec"
PASSWORD = "omotec"

# Column headers
COLUMNS = [
    'Quiz Name', 'Course Name', 'Name', 'E-mail', 'Test Date',
    'Marks', 'Total Mark', 'Grade Range', 'Percentage', 'Passing Status'
]

def create_csv_file():
    if not os.path.isfile(CSV_FILE_PATH):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE_PATH, index=False)

def insert_data(*args):
    df = pd.read_csv(CSV_FILE_PATH)
    new_data = dict(zip(COLUMNS, args))
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE_PATH, index=False)

def fetch_data():
    if os.path.isfile(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    return pd.DataFrame(columns=COLUMNS)

def set_background_image(image_file_path):
    if os.path.exists(image_file_path):
        with open(image_file_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Background image not found.")

def login_screen():
    set_background_image("back.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC ASSESSMENT PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

    st.markdown("📚 STUDENT ASSESSMENT LOGIN")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "Student Assessment Form"
        else:
            st.error("Invalid credentials")

def assessment_form():
    set_background_image("backs.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC ASSESSMENT PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

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

def show_assessments():
    set_background_image("back.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC ASSESSMENT PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

    st.markdown("📊 SHOW STUDENT ASSESSMENTS MASTER SHEET")
    df = fetch_data()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No data found.")

def display_chart():
    set_background_image("backs.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC ASSESSMENT PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

    st.markdown("📈 DISPLAY STUDENT ASSESSMENTS")
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

    available_cols = [col for col in df.columns if df[col].dtype != 'O']
    if not available_cols:
        st.warning("No numeric columns available for charting.")
        return

    selected_label_col = st.selectbox("Pie Chart Labels (Categorical)", [col for col in df.columns if df[col].dtype == 'O'])
    selected_value_col = st.selectbox("Pie Chart Values (Numeric)", available_cols)

    chart_types = [
        "Pie Chart", "Bar Plot", "Box Plot", "Violin Plot", "Strip Plot",
        "Swarm Plot", "Histogram", "KDE Plot", "Heatmap (Correlation)", "Joint Plot"
    ]
    selected_chart = st.selectbox("Select Chart Type", chart_types)

    try:
        if selected_chart == "Pie Chart":
            pie_data = filtered_df.groupby(selected_label_col)[selected_value_col].sum()
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        elif selected_chart == "Bar Plot":
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Box Plot":
            fig, ax = plt.subplots()
            sns.boxplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Violin Plot":
            fig, ax = plt.subplots()
            sns.violinplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Strip Plot":
            fig, ax = plt.subplots()
            sns.stripplot(data=filtered_df, x=selected_label_col, y=selected_value_col, jitter=True, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Swarm Plot":
            fig, ax = plt.subplots()
            sns.swarmplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Histogram":
            fig, ax = plt.subplots()
            sns.histplot(data=filtered_df[selected_value_col], kde=False, ax=ax)
            st.pyplot(fig)

        elif selected_chart == "KDE Plot":
            fig, ax = plt.subplots()
            sns.kdeplot(data=filtered_df[selected_value_col], ax=ax, fill=True)
            st.pyplot(fig)

        elif selected_chart == "Heatmap (Correlation)":
            corr = filtered_df.select_dtypes(include='number').corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

        elif selected_chart == "Joint Plot":
            fig = sns.jointplot(data=filtered_df, x=selected_label_col, y=selected_value_col, kind="scatter")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error generating {selected_chart}: {e}")

def sidebar_navigation():
    pages = {
        "Student Assessment Form": assessment_form,
        "Show Assessments": show_assessments,
        "Display Student Assessments": display_chart
    }
    choice = st.sidebar.radio("📚 Navigation", list(pages.keys()))
    st.session_state.page = choice
    pages[choice]()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_navigation()