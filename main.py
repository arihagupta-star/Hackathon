# Main Chatbot Interface

class Chatbot:
    def __init__(self):
        self.name = "Chatbot"
        self.is_running = True

    def greet(self):
        return f"Hello! I am {self.name}. How can I assist you today?"

    def run(self):
        print(self.greet())
        while self.is_running:
            user_input = input("You: ")
            self.process_input(user_input)

    def process_input(self, user_input):
        if user_input.lower() in ["exit", "quit"]:
            self.is_running = False
            print("Goodbye!")
        else:
            print(f"Bot: You said '{user_input}'")

if __name__ == '__main__':
    chatbot = Chatbot()
    chatbot.run()