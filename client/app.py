import re
import streamlit as st
import pandas as pd
from wrapper.main import LLMWrapper
from wrapper.db import run_query
from client.utils.htmlTemplate import css
from client.utils.htmlTemplate import bot_template, user_template
from database.get_columns import fetch_columns

def get_conversation(question):
    st.session_state.chat_history.append({"role": "user", "content": question})
    response = st.session_state.sql_agent.generate_response(user_input=question)
    return response

def get_analyst_conversation(question):
    st.session_state.visual_history.append({"role": "user", "content": question})
    response = st.session_state.analyst.generate_response(user_input=question)
    return response

def extract_column_names(sql_query):
    if 'SELECT *' in sql_query.upper():
        return fetch_columns()
    
    pattern = r'SELECT\s+(.*?)\s+FROM'
    match = re.search(pattern, sql_query, re.IGNORECASE)

    if match:
        columns = match.group(1).split(',')
        return [column.strip() for column in columns]
    else:
        return []

def handel_user_input(response):
    res_box = st.empty()
    response_msg = []

    for r in response:
            if r["choices"][0]["delta"] == {}:
                break
            msg = r["choices"][0]["delta"]["content"]
            response_msg.append(msg)
            result = "".join(response_msg)
            res_box.markdown(bot_template.replace("{{MSG}}", result), unsafe_allow_html=True)

    sql_match = re.search(r"```sql\n(.*)\n```", message["content"], re.DOTALL)            

    st.session_state.chat_history.append(
        {"role": "assistant", "content": "".join(response_msg)},
        {"role": "user", "content": question},
        )

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
            # Parse the response for a SQL query and execute if available
            sql_match = re.search(r"```sql\n(.*)\n```", message["content"], re.DOTALL)
            if sql_match:
                sql = sql_match.group(1)
                res = run_query(sql, "transactions")
                columns = extract_column_names(sql)

                df = pd.DataFrame(res)
                
                if columns:
                    df = pd.DataFrame(res, columns=columns)
                st.dataframe(df, use_container_width=True)

    st.session_state.sql_agent.history = st.session_state.chat_history

def main():
    st.set_page_config(page_title="SQLift", page_icon=":mailbox_with_mail:", layout="wide")
    st.write(css, unsafe_allow_html=True)
    st.header("SQLift :mag_right:")

    platform = st.sidebar.selectbox(label="Select type", options=["Table", "Plot"])

    if platform == "Table":
        question = st.text_input("Search your table:")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "sql_agent" not in st.session_state:
            st.session_state.sql_agent = LLMWrapper(agent="sql_agent")

        if "chat_index" not in st.session_state:
            st.session_state.chat_index = 0
        
        if st.button("Send"):
            with st.spinner("Searching..."):
                if question:
                    conversation = get_conversation(question)
                    handel_user_input(conversation)

    elif platform == "Plot":
        question = st.text_input("Visualize your table:")

        if "visual_history" not in st.session_state:
            st.session_state.visual_history = []

        if "analyst" not in st.session_state:
            st.session_state.analyst = LLMWrapper(agent="analyst_agent")

        if st.button("Send"):
            with st.spinner("Searching..."):
                if question:
                    conversation = get_analyst_conversation(question)
                    handel_user_input(conversation)