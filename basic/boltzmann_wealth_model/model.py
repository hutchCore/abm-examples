"""
=========================
Boltzmann Wealth Model
=========================

A simple model of wealth distribution based on the Boltzmann-Gibbs distribution.
Agents move randomly on a grid, giving one unit of wealth 
to a random neighbor when they occupy the same cell. 

"""

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.data_collection import DataRecorder, DatasetConfig
from mesa.experimental.scenarios import Scenario

from agents import MoneyAgent


class BoltzmannScenario(Scenario):
    """Scenario parameters for the Boltzmann Wealth Model"""

    n: int = 100
    width: int = 10
    height: int = 10

class BoltzmannWealth(Model):
    """A simple model of an economy where agents exchange currency at random.
    
    All agents begin wiht one unit of currency, and each time-step agents can give
    a unit of currency to another agent in the same cell. Over time, this produces
    a highly skewed distribution of wealth. 

    Attributes:
        num_agents (int): Number of agents in the model
        grid (MultiGrid): The space in which agents move 
        running (bool): Whether the model should continue running
        datacollector (DataCollector): Collects and stores model data
    
    """

    def __init__(self, scenario: BoltzmannScenario = BoltzmannScenario):
        """Initialize the model
        
        Args: 
            scenario: BoltmannScenario object containing model parameters.
        """
        super().__init__(scenario=scenario)

        self.num_agents = scenario.n
        self.grid = OrthogonalMooreGrid(
            (scenario.width, scenario.height), random=self.random
        )

        # Register what data to record
        self.recorder = DataRecorder(self)
        self.data_registry.track_agents(self.agents, "agent_data", "wealth").record(
                self.recorder
            )
        self.data_registry.track_model(self, "model_data", "gini").record(
                self.recorder, configuration=DatasetConfig(start_time=4, interval=2)
            )

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Gini": "gini"},
            agent_reporters={"Wealth": "wealth"},
        )

        # Create agents
        MoneyAgent.create_agents(
            self, 
            self.num_agents, 
            self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")      # Activate all agents in random order
        self.datacollector.collect(self)    # Collect data

    @property
    def gini(self):
        """Calculate the Gini coefficient for the model's current wealth distribution. 

        The Gini coefficient is a measure of inequality in distributions.
        - A Gini of 0 represents complete equality, where all agents have equal wealth.
        - A Gini of 1 represents maximal inequality, where one agent has all the wealth.
        """
        agent_wealths = [agent.wealth for agent in self.agents]
        x = sorted(agent_wealths)
        n = self.num_agents

        # Calculate the standard formula for Gini coefficient
        # Measuring how unevenly wealth is distributed. 
        # The weighting ensures that larger disparities between 
        # rich and poor agents contribute more to the inequality measure.
        #
        # 1. Loop through the sorted wealth values, returning the index (i) and wealth value (xi)
        # 2. Mutiply each wealth value by its "weight" - how far it is from the end of the sorted list.
        #    - Higher wealth values get larger weights
        # 3. Then sum all these weighted products
        # 4. The denominator (n * sum(x)) normailizes the calculation 
        #    by multiplying total wealth by number of agents.
        # The result (b) is a value between 0 and 1
        #    0 = perfect equality (everyone has the same wealth)
        #    1 = perfect inequality (one person has all the wealth)
        b = sum(xi * (n - i) for i, xi in enumerate(x)) / (n * sum(x))

        # This is the standard mathematical formula that converts 
        # the intermediate calculation into the final Gini coefficient
        return 1 + (1 / n) - 2 * b