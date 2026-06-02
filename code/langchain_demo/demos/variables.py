from model import model
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

# system = SystemMessagePromptTemplate.from_template(template="You are an expert in French cuisine.")
system = SystemMessagePromptTemplate.from_template(template="You are an expert in {cuisine} cuisine.")
# human = HumanMessagePromptTemplate.from_template(template="Create an easy breakfast meal. ")
human = HumanMessagePromptTemplate.from_template(template="Create an easy {mealtime} meal. ")

prompt = (system + human)

# I.
# chain = prompt | model
# result = chain.invoke({})
# result = chain.invoke({"cuisine":"southern","mealtime":"dinner"})

# II.
parser = StrOutputParser()
chain = prompt | model | parser
result = chain.invoke({"cuisine":"southern","mealtime":"dinner"})

print(result)

