# Agent Implementation

class Agent:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name} and I am your agent!"

    def perform_action(self, action):
        return f"Performing action: {action}"

# Example of creating an agent instance
if __name__ == '__main__':
    my_agent = Agent("Agent Smith")
    print(my_agent.greet())
    print(my_agent.perform_action("Walk"))
