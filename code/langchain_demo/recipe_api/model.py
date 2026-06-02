from pprint import pprint
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
  model="gpt-4o",
  #openai_api_key=""
)


# Note:
# This block allows for direct testing of the model logic while supporting reuse of this `model` configuration in other scripts.
if __name__ == "__main__":
  result = model.invoke("I would like a simple breakfast recipe")
  pprint(result)