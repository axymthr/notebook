from model import model
from langchain_core.messages import HumanMessage, SystemMessage

system = SystemMessage("You are an expert in French cuisine.")
human = HumanMessage("I would like an easy breakfast recipe. ")
# I.
# result = model.invoke([system,human])

# II.
# prompt = (system + human)
# chain = prompt | model
# result = chain.invoke({})

# III.
result = ((system + human) | model).invoke({})
print(result)