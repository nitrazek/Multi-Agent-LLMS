import os
from dotenv import load_dotenv
load_dotenv()
from modules.input_module.input_agent import input_agent

respone = input_agent.run()
print(respone)