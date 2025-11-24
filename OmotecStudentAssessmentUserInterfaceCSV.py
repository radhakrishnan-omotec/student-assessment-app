import streamlit as st
import pandas as pd
import os

# Define the CSV file path
CSV_FILE_PATH = 'C:\\Users\\OMOLP091\\Downloads\\STUDENT_ASSESSMENT\\sample_student_assessment.csv'

# Function to create a CSV file with headers if it doesn't exist
def create_csv_file():
    if not os.path.isfile(CSV_FILE_PATH):
        df = pd.DataFrame(columns=['Student ID', 'Category', 'Grade', 'Pre Assessment', 'Mid Assessment', 'Post Assessment', 'Final Culmination'])
        df.to_csv(CSV_FILE_PATH, index=False)

# Function to insert data into the CSV file
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
    # Create a DataFrame for the new data
    new_data_df = pd.DataFrame([new_data])
    # Concatenate the new data with the existing DataFrame
    df = pd.concat([df, new_data_df], ignore_index=True)
    df.to_csv(CSV_FILE_PATH, index=False)

# Function to fetch data from the CSV file
def fetch_data():
    if os.path.isfile(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    return pd.DataFrame(columns=['Student ID', 'Category', 'Grade', 'Pre Assessment', 'Mid Assessment', 'Post Assessment', 'Final Culmination'])

# Streamlit UI
def main():
    st.title("STUDENT ASSESSMENT SHEET")

    # Create CSV file if it doesn't exist
    create_csv_file()

    # Input fields
    student_id = st.text_input("Student ID")
    category = st.selectbox("Category", ["PRIMARY", "SECONDARY"])
    grade = st.text_input("Grade")
    
    pre_assessment = st.selectbox("Pre Assessment", list(range(1, 11)))
    mid_assessment = st.selectbox("Mid Assessment", list(range(1, 11)))

    # Conditional display of assessment fields based on category
    if category == "PRIMARY":
        post_assessment = st.selectbox("Post Assessment", list(range(1, 11)))
        final_culmination = None  # Not applicable for PRIMARY
    else:  # SECONDARY
        post_assessment = None  # Not applicable for SECONDARY
        final_culmination = st.selectbox("Final Culmination", list(range(1, 11)))

    # Submit button
    if st.button("SUBMIT"):
        if student_id and category and grade:
            insert_data(student_id, category, grade, pre_assessment, mid_assessment, post_assessment, final_culmination)
            st.success("Data submitted successfully!")
        else:
            st.error("Please fill in all fields.")

    # Display data
    if st.button("Show Assessments"):
        data = fetch_data()
        
        if not data.empty:
            st.write("### Stored Assessments")
            st.dataframe(data)
        else:
            st.write("No data found.")

if __name__ == "__main__":
    main()