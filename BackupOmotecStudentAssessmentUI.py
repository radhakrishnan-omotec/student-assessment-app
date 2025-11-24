import streamlit as st
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Constants
CSV_FILE_PATH = 'C:\\Users\\OMOLP091\\Downloads\\STUDENT_ASSESSMENT\\sample_student_assessment.csv'
USERNAME = "omotec"
PASSWORD = "omotec"

# Create file with headers if missing
def create_csv_file():
    if not os.path.isfile(CSV_FILE_PATH):
        df = pd.DataFrame(columns=['Student ID', 'Category', 'Grade', 'Pre Assessment', 'Mid Assessment', 'Post Assessment', 'Final Culmination'])
        df.to_csv(CSV_FILE_PATH, index=False)

def insert_data(student_id, category, grade, pre_assessment, mid_assessment, post_assessment, final_culmination):
    df = pd.read_csv(CSV_FILE_PATH)
    new_data = {
        'Student ID': student_id,
        'Category': category,
        'Grade': grade,
        'Pre Assessment': pre_assessment,
        'Mid Assessment': mid_assessment,
        'Post Assessment': post_assessment,
        'Final Culmination': final_culmination
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(CSV_FILE_PATH, index=False)

def fetch_data():
    if os.path.isfile(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    return pd.DataFrame(columns=['Student ID', 'Category', 'Grade', 'Pre Assessment', 'Mid Assessment', 'Post Assessment', 'Final Culmination'])

# Login Screen
def login_screen():
    st.title("🔐 STUDENT ASSESSMENT LOGIN")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "Student Assessment Form"
        else:
            st.error("Invalid credentials")

# Assessment Input Page
def assessment_form():
    st.title("📝 STUDENT ASSESSMENT FORM")
    create_csv_file()

    student_id = st.text_input("Student ID")
    category = st.selectbox("Category", ["PRIMARY", "SECONDARY"])
    grade = st.text_input("Grade")
    pre_assessment = st.selectbox("Pre Assessment", list(range(1, 11)))
    mid_assessment = st.selectbox("Mid Assessment", list(range(1, 11)))

    post_assessment, final_culmination = None, None
    if category == "PRIMARY":
        post_assessment = st.selectbox("Post Assessment", list(range(1, 11)))
    else:
        final_culmination = st.selectbox("Final Culmination", list(range(1, 11)))

    if st.button("Submit"):
        if student_id and grade:
            insert_data(student_id, category, grade, pre_assessment, mid_assessment, post_assessment, final_culmination)
            st.success("✅ Data submitted successfully!")
        else:
            st.error("Please fill in all required fields.")

# Table Display Page
def show_assessments():
    st.title("📊 SHOW STUDENT ASSESSMENTS")
    df = fetch_data()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No data found.")

# Display chart Page
def display_chart():
    st.title("📈 DISPLAY STUDENT ASSESSMENTS")
    df = fetch_data()

    if df.empty:
        st.warning("No data to display.")
        return

    # Sidebar Filters
    st.sidebar.markdown("### Filter Options")
    student_id = st.sidebar.selectbox("Student ID", ['All'] + sorted(df['Student ID'].dropna().unique()))
    category = st.sidebar.selectbox("Category", ['All'] + sorted(df['Category'].dropna().unique()))
    grade = st.sidebar.selectbox("Grade", ['All'] + sorted(df['Grade'].dropna().unique()))

    # Filter logic
    filtered_df = df.copy()
    if student_id != 'All':
        filtered_df = filtered_df[filtered_df['Student ID'] == student_id]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if grade != 'All':
        filtered_df = filtered_df[filtered_df['Grade'] == grade]

    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # Download CSV
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button("📥 Download Filtered Data (CSV)", csv_buffer.getvalue(), file_name="filtered_data.csv", mime="text/csv")

    # Numeric columns
    numeric_cols = ['Student ID', 'Category', 'Grade', 'Pre Assessment', 'Mid Assessment', 'Post Assessment', 'Final Culmination']
    available_cols = [col for col in numeric_cols if col in filtered_df.columns]

    st.subheader("📊 Seaborn Chart Gallery")

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
        

# Sidebar for Navigation
def sidebar_navigation():
    pages = {
        "Student Assessment Form": assessment_form,
        "Show Assessments": show_assessments,
        "Display Student Assessments": display_chart
    }

    choice = st.sidebar.radio("📚 Navigation", list(pages.keys()))
    st.session_state.page = choice
    pages[choice]()

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Main Routing
if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_navigation()