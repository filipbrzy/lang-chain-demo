from langchain_openai import ChatOpenAI

# LLM Model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000,
    timeout=30
)

response = llm.invoke("Explain LangChain in one sentence.")
print(response.content)