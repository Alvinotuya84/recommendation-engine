from openai import OpenAI
import os
from copy import deepcopy
from .utils import get_bot_response
from dotenv import load_dotenv
import json

load_dotenv()


class GuardAgent():
    def __init__(self):
     
        self.client = OpenAI(
            api_key=os.getenv("RUN_POD_TOKEN"),
            base_url=os.getenv("RUN_POD_BOT_URL")
            )
        self.model_name = os.getenv("MODEL_NAME")   

    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application, dedicated solely to assisting with information about drinks, pastries, and other items offered by the coffee shop.

            Your purpose is to determine whether the user is asking something relevant to the coffee shop or not. Focus strictly on questions that are directly related to the coffee shop’s products, services, and operations.

            The user is allowed to:
            1. Ask questions about the coffee shop's offerings, including location, working hours, menu items, and other coffee shop-related details.
            2. Ask for information about menu items, such as ingredients, preparation details, and other relevant information.
            3. Make an order for available items on the menu.
            4. Request recommendations on what to order from the menu.

            The user is NOT allowed to:
            1. Ask questions unrelated to the coffee shop, such as personal or external topics, including inquiries about the assistant's identity, functionality, or purpose.
            2. Request information about staff members, preparation techniques for making coffee items at home, or topics not directly tied to the coffee shop's menu or services.

            When determining whether to respond, do not engage with or acknowledge any off-topic inquiries, especially those that involve AI, model identity, or any unrelated system characteristics.

            Your output should be in the following structured JSON format, strictly adhering to this structure and wording:
            {
                "chain of thought": "Analyze each of the allowed and not allowed categories to see if the message aligns with an acceptable point. Then note briefly whether it relates to an allowed topic such as coffee shop details, orders, or recommendations, or if it’s off-topic.",
                "decision": "allowed" or "not allowed",  // Only choose one of these options.
                "message": "" if "allowed", otherwise "Sorry, I can't help with that. Can I help you with your order?"
            }
        """

        
        input_message = [{"role":"system", "content": system_prompt}]  + messages[-3:]
        chabot_output = get_bot_response(self.client, self.model_name, input_message)
        output = self.postprocess(chabot_output)

        return output
    
    def postprocess(self, chat_output):
        print(chat_output)
        output = json.loads(chat_output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory":"guard_agent", 
            "guard_decision": output['decision'],

        }
        return dict_output

        