import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from commands import (
    chrome_click_on_link,
    chrome_get_the_links_on_the_page,
    chrome_open_url,
    chrome_read_the_page,
    computer_applescript_action,
    read_file,
    write_file,
    list_directory,
    run_shell_command
)

load_dotenv()

def get_llm(model_name=None, provider=None):
    temperature = 0
    if provider == "ollama":
        base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/v1"
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_base=base_url,
            openai_api_key="ollama" # Ollama doesn't need a real key but ChatOpenAI expects one
        )
    elif provider == "lm_studio":
        base_url = os.environ.get("LM_STUDIO_HOST", "http://localhost:1234") + "/v1"
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_base=base_url,
            openai_api_key="lm_studio"
        )
    else:
        # Default to OpenAI
        return ChatOpenAI(
            model=model_name or "gpt-3.5-turbo",
            temperature=temperature,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

def get_agent(model_name=None, provider=None):
    llm = get_llm(model_name, provider)

    tools = [
        computer_applescript_action,
        chrome_open_url,
        chrome_get_the_links_on_the_page,
        chrome_read_the_page,
        chrome_click_on_link,
        read_file,
        write_file,
        list_directory,
        run_shell_command
    ]

    system_message = """You are a development-task-automation powerhouse.
    You can carry out any task a user would be able to carry out on their Mac.
    You have tools to interact with the file system, run shell commands, use the browser, and execute AppleScript.
    Be precise and helpful. For development tasks, prefer using shell commands and file tools when appropriate.
    When asked to perform a development task, think about the steps needed:
    1. List files or read existing code to understand context.
    2. Plan changes or execution.
    3. Use shell commands to run tests, build projects, or execute scripts.
    4. Use file tools to modify code.
    5. Verify results.
    """

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True,
        agent_kwargs={"prefix": system_message}
    )
    return agent

if __name__ == "__main__":
    # Test agent with default settings
    agent = get_agent()
    agent.run("What is 5 x 5?")
