#This file is the master function for routing tasks to the appropriate agents based on the round robin algorithm. It imports the necessary functions from the round_robin module and uses them to determine which agent should handle each task.


from nolimitai.config.config import Config


class Router:
    def __init__(self, config: Config):
        self.config = config
        self.services = self.config.get_avalited_service()
        self.agent_index = 0

    def get_next_provider(self):
        """
        Returns the next provider in a round-robin fashion.
        """
        
        pass