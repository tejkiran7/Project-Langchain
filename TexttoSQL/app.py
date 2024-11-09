from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
        """
        You are an expert in converting English questions to SQL queries!
        The SQL database has the name STUDENT and the following columns: NAME, CLASS, SECTION and MARKS.

        For example:

        Example 1 - How many entries of records are present? 
        The SQL query will be: SELECT COUNT(*) FROM STUDENT;

        Example 2 - Tell me all the students studying in Data Science class? 
        The SQL query will be: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

        Please provide only the SQL query in your response without any explanation or extra text. Do not include backticks or the word "SQL" in the output.
        """
]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)