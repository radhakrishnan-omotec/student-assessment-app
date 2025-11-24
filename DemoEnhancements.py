import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os
import base64

# Constants
CSV_FILE_PATH = 'Final Culmination_AI_Blocks_1_AND_2.csv'
USERNAME = "omotec"
PASSWORD = "omotec"

# Column headers
COLUMNS = [
    'Quiz Name', 'Course Name', 'Name', 'E-mail', 'Test Date',
    'Marks', 'Total Mark', 'Grade Range', 'Percentage', 'Passing Status',
    'A) Pre-Assessment', 'B) Mid-Culmination', 'C) Final-Culmination'
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

    course_name = st.text_input("Course Name")
    quiz_name = st.text_input("Quiz Name")
    name = st.text_input("Student Name")
    email = st.text_input("E-mail")
    test_date = st.date_input("Test Date")
    marks = st.number_input("Marks", min_value=0)
    total_mark = st.number_input("Total Mark", min_value=1)
    grade_range = st.text_input("Grade Range")
    percentage = (marks / total_mark) * 100 if total_mark > 0 else 0
    passing_status = st.selectbox("Passing Status", ["Pass", "Fail"])
    pre_assessment = st.text_input("A) Pre-Assessment")
    mid_culmination = st.text_input("B) Mid-Culmination")
    final_culmination = st.text_input("C) Final-Culmination")

    if st.button("Submit"):
        if name and email:
            insert_data(
                quiz_name, course_name, name, email, str(test_date),
                marks, total_mark, grade_range, percentage, passing_status,
                pre_assessment, mid_culmination, final_culmination
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

    # CSV Upload Option
    st.markdown("### Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        if st.button("Display CSV"):
            uploaded_df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_df = uploaded_df
            st.session_state.uploaded_csv_name = uploaded_file.name
            st.markdown("### Uploaded CSV Data")
            st.dataframe(uploaded_df)

    st.markdown("---")
    st.markdown("### GENERATE REPORTS CSV")
    csv_files = []
    if os.path.isfile(CSV_FILE_PATH):
        csv_files.append(("Default CSV", CSV_FILE_PATH))
    if "uploaded_df" in st.session_state:
        csv_files.append(("Uploaded CSV", st.session_state.uploaded_csv_name))

    for name, path in csv_files:
        if st.button(f"Download {name}"):
            with open(path, "rb") as file:
                st.download_button(label=f"Download {name}", data=file, file_name=os.path.basename(path), mime="text/csv")

def display_chart():
    set_background_image("backs.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>OMOTEC ASSESSMENT PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

    st.markdown("📈 DISPLAY STUDENT ASSESSMENTS")
    default_df = fetch_data()

    st.sidebar.markdown("### Choose CSV Input")
    csv_options = ["Default CSV"]
    if "uploaded_df" in st.session_state:
        csv_options.append(f"Uploaded CSV: {st.session_state.uploaded_csv_name}")
    selected_csv = st.sidebar.selectbox("Select CSV to Display", csv_options)

    df = default_df if selected_csv == "Default CSV" else st.session_state.uploaded_df

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
        "Generate All Pie Charts", "Generate All Bar Graphs", "Pie Chart", "Bar Plot", "Box Plot", "Strip Plot", "Swarm Plot"
    ]
    selected_chart = st.selectbox("Select Chart Type", chart_types)

    try:
        if selected_chart == "Generate All Pie Charts":
            for col in available_cols:
                pie_data = filtered_df.groupby(selected_label_col)[col].sum()
                fig, ax = plt.subplots()
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

        elif selected_chart == "Generate All Bar Graphs":
            for col in available_cols:
                fig, ax = plt.subplots()
                sns.barplot(data=filtered_df, x=selected_label_col, y=col, ax=ax)
                plt.xticks(rotation=90)
                st.pyplot(fig)

        elif selected_chart == "Pie Chart":
            pie_data = filtered_df.groupby(selected_label_col)[selected_value_col].sum()
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        elif selected_chart == "Bar Plot":
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        elif selected_chart == "Box Plot":
            fig, ax = plt.subplots()
            sns.boxplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        elif selected_chart == "Strip Plot":
            fig, ax = plt.subplots()
            sns.stripplot(data=filtered_df, x=selected_label_col, y=selected_value_col, jitter=True, ax=ax)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        elif selected_chart == "Swarm Plot":
            fig, ax = plt.subplots()
            sns.swarmplot(data=filtered_df, x=selected_label_col, y=selected_value_col, ax=ax)
            plt.xticks(rotation=90)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error generating {selected_chart}: {e}")

# ===============================
# Enhanced New Page: Graph of Bloom's Taxonomy
# ===============================
def generate_blooms_taxonomy_graphs():
    st.markdown("## 📊 Graphs on Bloom's Taxonomy")

    # CSV selection sidebar
    st.sidebar.markdown("### Choose CSV Input")
    csv_options = ["Default CSV"]
    if "uploaded_df" in st.session_state:
        csv_options.append(f"Uploaded CSV: {st.session_state.uploaded_csv_name}")
    selected_csv = st.sidebar.selectbox("Select CSV to Display", csv_options)
    df = fetch_data() if selected_csv == "Default CSV" else st.session_state.uploaded_df

    if df.empty:
        st.warning("No data available for visualization.")
        return

    # Define Bloom's taxonomy axis mappings
    blooms_columns = [
        ('A) Pre-Assessment', 'Understand'),
        ('A) Pre-Assessment', 'Remember'),
        ('A) Pre-Assessment', 'Analyze'),
        ('A) Pre-Assessment', 'Apply'),
        ('A) Pre-Assessment', 'Create'),
        ('B) Mid-Culmination', 'Understand'),
        ('B) Mid-Culmination', 'Remember'),
        ('B) Mid-Culmination', 'Analyze'),
        ('B) Mid-Culmination', 'Apply'),
        ('B) Mid-Culmination', 'Create'),
        ('C) Final-Culmination', 'Understand'),
        ('C) Final-Culmination', 'Remember'),
        ('C) Final-Culmination', 'Analyze'),
        ('C) Final-Culmination', 'Apply'),
        ('C) Final-Culmination', 'Create'),
        ('Marks', 'Understand'),
        ('Marks', 'Remember'),
        ('Marks', 'Analyze'),
        ('Marks', 'Apply'),
        ('Marks', 'Create'),
        ('Percentage', 'Create')
    ]

    # Filter out columns not in the data or entirely empty
    valid_blooms = [
        (col, label) for col, label in blooms_columns
        if col in df.columns and df[col].dropna().apply(str).str.strip().ne('').any()
    ]

    if not valid_blooms:
        st.warning("No valid Bloom's taxonomy data found in the dataset.")
        return

    # Plot each graph vertically, one below the other
    for column, label in valid_blooms:
        st.markdown(f"<h3 style='font-size:26px;'>{label}</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x=df['Name'], y=df[column], ax=ax)
        ax.set_title(label)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        st.pyplot(fig)

    st.success(f"✅ Displayed {len(valid_blooms)} Bloom's taxonomy visualizations.")



# ===============================
# Enhanced New Page: Grade-wise Comparison
# ===============================
def generate_grade_comparison_graphs():
    st.markdown("## 📈 Graphs on Grade Comparison")

    # CSV selection sidebar
    st.sidebar.markdown("### Choose CSV Input")
    csv_options = ["Default CSV"]
    if "uploaded_df" in st.session_state:
        csv_options.append(f"Uploaded CSV: {st.session_state.uploaded_csv_name}")
    selected_csv = st.sidebar.selectbox("Select CSV to Display", csv_options)
    df = fetch_data() if selected_csv == "Default CSV" else st.session_state.uploaded_df

    if df.empty:
        st.warning("No data available for visualization.")
        return

    grade_col = 'Grade Range'
    if grade_col not in df.columns:
        st.error(f"Column '{grade_col}' not found in data.")
        return

    unique_grades = sorted(df[grade_col].dropna().unique())

    # Automatically select all numeric columns except 'Grade Range'
    numeric_cols = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if col != grade_col]

    if not numeric_cols:
        st.warning("No numeric columns found for comparison.")
        return

    st.markdown(f"### Found {len(numeric_cols)} Numeric Columns for Grade-wise Comparison:")
    st.markdown(", ".join(numeric_cols))

    # Create subplots in horizontal layout
    fig, axs = plt.subplots(1, len(numeric_cols), figsize=(7 * len(numeric_cols), 5))
    if len(numeric_cols) == 1:
        axs = [axs]  # Make it iterable if only 1 plot

    for i, metric in enumerate(numeric_cols):
        sns.barplot(data=df, x=grade_col, y=metric, ax=axs[i])
        axs[i].set_title(f'{metric} by Grade', fontsize=20)
        axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=45)

    st.pyplot(fig)

    st.markdown("### 🧾 Grades Included in Chart:")
    st.markdown(", ".join(str(g) for g in unique_grades))


# ===============================
# Enhanced Sidebar Navigation
# ===============================
def sidebar_navigation():
    pages = {
        "Student Assessment Form": assessment_form,
        "Show Assessments & Report Downloads": show_assessments,
        "Display Student Assessments": display_chart,
        "Graphs on Bloom's Taxonomy": generate_blooms_taxonomy_graphs,
        "Graphs on Grade Comparison": generate_grade_comparison_graphs
    }
    choice = st.sidebar.radio("📚 Navigation", list(pages.keys()))
    st.session_state.page = choice
    pages[choice]()

# ===============================
# Auth Flow
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_navigation()