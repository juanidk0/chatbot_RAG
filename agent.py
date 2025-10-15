# agent.py
import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, Tool, AgentExecutor, create_openai_tools_agent
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate,  ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


load_dotenv()

# =========================================
# CONFIGURATION
# =========================================
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")
CHROMA_PATH = os.getenv("CHROMA_PATH", "company_db")


# =========================================
# INITIALIZATION
# =========================================
def init_vectorstore():
    """Load the persisted Chroma vector store."""
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

def init_agent():
    """Initialize the agent with tools, retriever, and memory."""
    # LLM
    llm = ChatOpenAI(model=MODEL)

    # Vector store + retriever
    vectorstore = init_vectorstore()
    retriever = vectorstore.as_retriever()

    # RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    # Tools
    tools = [
        Tool(
            name="CompanyKnowledge",
            func=lambda q: rag_chain.invoke(q),
            description="Use this to answer questions about company data and strategy."
        ),
        Tool(
            name="WebSearch",
            func=DuckDuckGoSearchRun().run,
            description="Use this to perform a web search or find recent news related to the company."
        )
    ]

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an AI strategist working at ColumbusAI Solutions.
Your mission is to analyze company data, propose innovative AI-based products,
and stay updated with the latest AI trends.

You have access to two tools:
1. 'CompanyKnowledge' — retrieves internal information from the company's data.
2. 'WebSearch' — searches the web for recent or external information.

If you receive a query about a person, event, or fact not found in internal data,
you **must** use the WebSearch tool before answering.
If both tools return nothing, respond with:
"I don't have reliable information on that yet."
the responses should no be too verbose, Just answer with accurate data, and avoid things
like "Great Question, Excellent question", or emojis
Always reason clearly, use tools first, and only synthesize insights afterward."""
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Agent + memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,

    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,

    )

    return executor


# Initialize just once
AGENT_EXECUTOR = init_agent()

def run_agent(query: str):
    if query.lower() == 'reset':
        AGENT_EXECUTOR.memory.clear()
    result = AGENT_EXECUTOR.invoke({"input": query})
    return result.get("output", "")

