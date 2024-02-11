# !/usr/bin/python

import typer

from typing import List, Union

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI

from utils.query_data import query_data


model: ChatOpenAI = ChatOpenAI(model_name="gpt-4-0125-preview")

messages: List[Union[SystemMessage, HumanMessage]] = [
    SystemMessage(
        content="You are Chino, a chatbot based on ChatGPT. 'Chino' means 'intelligence' in Japanese."
    ),
]


def get_response(prompt: str) -> None:
    messages.append(HumanMessage(content=prompt))
    response: BaseMessage = model.invoke(messages)
    messages.append(SystemMessage(content=response.content))
    print(f"\n Chino: {response.content}\n-------------------\n")


def run_query(prompt: str) -> None:
    global model, messages

    query_text, query_sources = query_data(prompt)
    messages.append(HumanMessage(content=query_text))
    response: BaseMessage = model.invoke(messages)
    messages.append(SystemMessage(content=response.content))
    print(f"\nChino: {response.content}\n\nSources: {query_sources})\n-------------------\n")


def run_conversation(prompt: str, query: bool) -> None:
    global model, messages

    if prompt:
        if query or prompt.lower().startswith("\\query:"):
            run_query(prompt)
            return
        get_response(prompt)
        return

    while True:
        prompt: str = input("You: ")
        if prompt == "quit":
            break
        elif query or prompt.lower().startswith("\\query:"):
            run_query(prompt)
            continue
        get_response(prompt)


def main(
        prompt: str = typer.Option(None, '-p', '--prompt', help="Prompt for ChatGPT"),
        query: bool = typer.Option(False, '-q', '--query', help="Query for your data")
) -> None:
    run_conversation(prompt, query)


if __name__ == "__main__":
    typer.run(main)
