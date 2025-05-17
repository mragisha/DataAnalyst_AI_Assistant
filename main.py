import streamlit as st
import os
import sqlite3
from langchain_groq import ChatGroq 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def get_sql_query_from_text(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name STUDENT and has the following columns - NAME, COURSE, 
                    SECTION and MARKS. For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
                    Example 2 - Tell me all the students studying in Data Science COURSE?, 
                        the SQL command will be something like this SELECT * FROM STUDENT 
                        where COURSE="Data Science"; 
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please
                                                       """)
    model = "llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key=os.environ["GROQ_API_KEY"],
        model_name=model
    )

    chian = groq_sys_prompt | llm | StrOutputParser()

    #invoke chain
    sql_query = chian.invoke({"user_query" : user_query})

    return sql_query

def get_data_from_database(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        return conn.execute(sql_query).fetchall()
    

def main():
    st.set_page_config(page_title="Text to SQL Chat")
    st.title("🗂️ Text to SQL Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask something about the student database...")

    if user_query:
        # Display user message
        st.chat_message("user").markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        try:
            # Convert to SQL and fetch results
            sql_query = get_sql_query_from_text(user_query)
            result = get_data_from_database(sql_query)

            # Format result
            if result:
                result_str = "\n".join(str(row) for row in result)
            else:
                result_str = "No records found."

            # Show SQL used (optional)
            assistant_message = f"**SQL:** `{sql_query}`\n\n**Result:**\n{result_str}"
        except Exception as e:
            assistant_message = f"⚠️ Error: {str(e)}"

        # Display assistant message
        st.chat_message("assistant").markdown(assistant_message)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

if __name__ == "__main__":
    main()