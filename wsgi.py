from Wrapper.prompts import get_sql_system_prompt
from Wrapper.main import LLMWrapper
from Wrapper.db import run_query
import re
import pandas as pd

messages = [{"role": "system", "content": get_sql_system_prompt()}]

if __name__ == "__main__":
    wrapper = LLMWrapper()

    index = 0
    while True:
        user_input = input("User: ")    
        response = wrapper.generate_response(system_prompt=get_sql_system_prompt(), user_input=user_input)

        response_msg = ""
        for r in response:
            if r["choices"][0]["delta"] == {}:
                break
            msg = r["choices"][0]["delta"]["content"]
            response_msg += msg
            print(msg, end="", flush=True)

            message = {"role": "assistant", "content": response}

        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response_msg, re.DOTALL)


        if sql_match:
            sql = sql_match.group(1)
            res = run_query(sql, "transactions")
            message["result"] = pd.DataFrame(res)

        print(f"\n sql match: {message['result'].columns}")
        # wrapper.history = True
        # index += 1