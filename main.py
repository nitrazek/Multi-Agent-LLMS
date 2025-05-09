import os
from dotenv import load_dotenv
load_dotenv()
from modules.input_module.input_agent import agent

respone = agent.run("What is the latitude and longitude of the Eiffel Tower?")
print(respone)