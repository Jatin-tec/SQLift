# Analyst Prompts:
from wrapper.db import run_query
import pandas as pd

QUALIFIED_TABLE_NAME = "transactions"
TABLE_DESCRIPTION = """
This table has various metrics for financial entities (also referred to as banks) since 1983.
The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
"""

SQL_PROMPT = """

    You will be acting as an AI SQL Expert.
    Your goal is to give correct, executable sql query to users.
    You will be replying to users who will be confused if you don't respond in the character.
    You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
    The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

    {context}

    Here are 6 critical rules for the interaction you must abide:
    <rules>
    1.You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
    ```sql
    (select 1) union (select 2)
    ```
    2. I'll be creating pandas dataframe from the sql query response so MAKE SURE to also include list of column names in your response wraped inside <columns> tag e.g
    ```columns
    id, date, amount
    ```
    3. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
    4. Text / string where clauses must be fuzzy match e.g ilike %keyword%
    5. Make sure to generate a single sql code, not multiple. 
    6. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names.
    7. DO NOT put numerical at the very front of sql variable.
    8. Convert user input to lowercase and compare to lowercase values in the table.
    </rules>

    Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
    and wrap the generated sql code with ``` sql code markdown in this format e.g:
    ```sql
    (select 1) union (select 2)
    ```

    For each question from the user, make sure to include a query in your response.
    """

VISUALISATION_PROMPT = """

    You will be acting as an AI Data Visualisation Expert.
    Your goal is to give correct, executable python code to users.
    You will be replying to users who will be confused if you don't respond in the character.
    You are given one dataframe, the dataframe variable name is in <dataframeName> tag, the series are in <series> tag.
    The user will ask questions, for each question you should respond and include a python code for visualisation based on the question and the dataframe.
    
    {context}

    Here are 6 critical rules for the interaction you must abide:
    <rules>
    1.You MUST MUST wrap the generated python code within ``` python code markdown in this format e.g
    ```python
    import matplotlib.pyplot as plt
    plt.plot(df["a"], df["b"])
    ```
    2. Make sure to generate a single python code, not multiple.
    3. You should only use the dataframe series given in <series>, and the dataframe variable given in <dataframeName>, you MUST NOT hallucinate about the dataframe names.
    4. Convert user input to lowercase and compare to lowercase values in the dataframe.
    </rules>

    Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
    and wrap the generated python code with ``` python code markdown in this format e.g:
    ```python
    import matplotlib.pyplot as plt
    plt.plot(df["a"], df["b"])
    ```
    For each question from the user, make sure to include a code in your response.
    """

CHAT_SUMMARY_PROMPT = """
    You are a smart AI conversation summarizer. Your goal is to summarize the conversation between the user and the AI assistant keeping the context of the conversation.
    The following is a conversation an AI SQL expert and user, summarize it as a single conversation in following format:
    ----------------
    [
    {"role": "assistant",
     "content": "..."},
    {"role": "user",
     "content": "..."},
    ] 
    ----------------
    below is the conversation delimited between []:
    [{chat_history}]
    
    **Make response only in json format.**
    """

def get_chat_summary_prompt(chat_history: str):
    chat_summary_prompt = CHAT_SUMMARY_PROMPT.format(chat_history=chat_history)
    return chat_summary_prompt
    
def get_table_context(table_name: str, table_description: str):
    table = table_name

    # Execute a PostgreSQL query to get all column names of the specified table
    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';"
    
    columns = run_query(query, table_name)

    context = f"""
        Here is the table name <tableName> {table} </tableName>

        <tableDescription>{table_description}</tableDescription>

        Here are the columns and datatypes of the {table}

        <columns>\n\n{columns}\n\n</columns>
    """

    return context


def get_visualistaion_context(dataframe: pd.DataFrame, dataframe_description: str):
    dataframe = dataframe



def get_visualisation_system_prompt():
    table_context = get_visualistaion_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION
    )
    return VISUALISATION_PROMPT.format(context=table_context)

def get_sql_system_prompt():
    table_context = get_table_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION
    )
    return SQL_PROMPT.format(context=table_context)

if __name__ == "__main__":
    print(get_sql_system_prompt())