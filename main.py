from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    # Initialize the ChatAnthropic model with API key from environment
    llm = ChatAnthropic(
        model="claude-3-7-sonnet-20250219",
        temperature=0.5,
        max_tokens=128,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    print("Welcome to the Dummy Chat Bot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        messages = [
            ("system", "You are a helpful assistant."),
            ("human", user_input)
        ]
        response = llm.invoke(messages)
        print("Bot:", response.content)

if __name__ == "__main__":
    main()
