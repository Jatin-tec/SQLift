import time
import openai
import os
import pdb
from Wrapper.prompts import get_sql_system_prompt
from dotenv import load_dotenv
import json
from Wrapper.prompts import get_chat_summary_prompt

class LLMWrapper:
    """Wrapper class for the LLM API."""
    def __init__(self, max_tokens=3000, model="gpt-3.5-turbo", max_try=2, temprature=0):
        self.max_tokens = max_tokens
        self.model = model
        self.temperature = temprature
        self.max_try = max_try
        self.history = False

        load_dotenv(".env")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        print("Initialized LLMWrapper")

    def _send_request(self, system_prompt="", user_prompt=""):
        for _ in range(self.max_try):
            try:
                if self.history:
                    chat_history = self.history
                    try:
                        GENERAL_CHAT_PROMPT = [
                            {"role": "system", "content": system_prompt}, 
                            *chat_history,
                            {"role": "user", "content": user_prompt}
                        ]
                        
                    # handle token limit exceeded error
                    except openai.error.InvalidRequestError as e:                        
                        CHAT_HISTORY_PROMPT = [{"role": "system", "content": get_chat_summary_prompt(chat_history)}]

                        chat_summary = response = openai.ChatCompletion.create(
                            model=self.model,
                            messages=CHAT_HISTORY_PROMPT,
                            max_tokens=2000,
                            temperature=self.temperature,
                            stream=False,
                        )

                        chat_summary = chat_summary.choices[0].message["content"]

                        GENERAL_CHAT_PROMPT = [
                            {"role": "system", "content": system_prompt}, 
                            *json.loads(chat_summary),
                            {"role": "user", "content": user_prompt}
                        ]                

                    print(GENERAL_CHAT_PROMPT, "printing general chat prompt")

                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=GENERAL_CHAT_PROMPT,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        stream=True,
                    )
                    return response 
                
                else:
                    CHAT_PROMPT = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=CHAT_PROMPT,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        stream=True,
                    )
                    return response

            except openai.error.RateLimitError as e:
                self._handle_rate_limit()
                return self._send_request(CHAT_PROMPT)
            
            except openai.error.InvalidRequestError as e:
                if len(prompt) > self.max_tokens:
                    print("Prompt too long. Truncating...")
                    prompt = prompt[:self.max_tokens]
                    return self._send_request(prompt)
                print("Invalid request:", e)
                return {'error': 'invalid_request'}
            
            except Exception as e:
                print("Unhandled exception:", e)
                return {'error': 'unknown'}

    def _handle_rate_limit(self):
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(60) 

    def generate_response(self, user_input, system_prompt=get_sql_system_prompt()):
        """Generates a response based on the user input."""
        response = self._send_request(system_prompt=system_prompt, user_prompt=user_input)
        return response

    def reset_history(self):
        self.history = False


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
