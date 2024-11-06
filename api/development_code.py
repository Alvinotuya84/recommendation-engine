
from agents import(GuardAgent)
import os
def main():
    pass

if __name__ == "__main__":
    guard_agent = GuardAgent()


    messages = []
    while True:
        # os.system('clear')

        print("\n\n Print messages................................")
        for message in messages:
            print(f"{message['role']} : {message['content']}")


      ## get user input
            
        prompt = input("User: ")
        messages.append({"role":"user", "content":prompt})
        guard_agent_response= guard_agent.get_response(messages)
        print("Guard Agent Output:", guard_agent_response)
        messages.append(guard_agent_response)