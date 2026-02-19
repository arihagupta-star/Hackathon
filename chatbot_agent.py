# Chatbot Agent Implementation

class ChatbotAgent:
    def __init__(self, name):
        self.name = name

    def respond(self, user_input):
        # Simple response logic
        if 'hello' in user_input.lower():
            return f"Hello! I'm {self.name}, how can I assist you today?"
        return "I'm sorry, I didn't understand that."

if __name__ == '__main__':
    agent = ChatbotAgent('Agent007')
    while True:
        user_input = input('You: ')
        response = agent.respond(user_input)
        print(f'{agent.name}: {response}')