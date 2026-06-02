from model import model
from langchain_core.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

system = SystemMessagePromptTemplate.from_template(template="You are an expert in {cuisine} cuisine. Provide a single recipe.")
human = HumanMessagePromptTemplate.from_template(template="Create an easy {mealtime} meal. ")

parser = StrOutputParser()
chain = (system + human) | model | parser

def get_recipe(cuisine: str, mealtime: str):
    result = chain.invoke({
        "cuisine":cuisine,
        "mealtime":mealtime
    })
    return result


# Note:
# This conditional block allows for direct testing of this logic before integrating with the Recipe Suggesiont API.
if __name__ == "__main__":
    result = get_recipe("southern", "dinner")
    print(result)
