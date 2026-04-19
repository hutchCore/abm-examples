from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from agents import SchellingAgent
from mesa.experimental.scenarios import Scenario


class SchellingScenario(Scenario):
    """
    Scenario for the Schelling Model. 

    Args:
        width: Width of the grid
        height: Height of the grid
        density: Initial chance for a cell to be populated (0-1)
        minority_pc: Chance for an agent to be in minority class (0-1)
        homophily: minimum number of similar neighbors needed ofr happiness
        radius: Search radius for checking neighbor similarity
        rng: Seed for reproducibility
    """

    height: int = 20
    width: int = 20
    density: float = 0.8
    minority_pc: float = 0.5
    homophily: float = 0.4
    radius: int = 1

class Schelling(Model):
    """
    Model class for the Schelling Segregation Model
    """

    def __init__(self, scenario: SchellingScenario = SchellingScenario):
        """
        Create a new Schelling Model

        Args:
            scenario: SchellingScenario containing model parameters.
        """
        super().__init__(scenario=scenario)

        # Model parameters
        self.density = scenario.density
        self.minority_pc = scenario.minority_pc

        # Initialize grid
        self.grid = OrthogonalMooreGrid(
            (scenario.width, scenario.height), random=self.random, capacity=1
        )

        # Track happiness
        self.happy = 0

        # Set up data collection
        # when the collector runs, call this function with the model m and return the current number of agents.”
        self.datacollector = DataCollector(

            model_reporters={
                "happy": "happy",           # record the model's `happy` attribute
                "pct_happy": lambda m: (
                    (m.happy / len(m.agents)) * 100 if len(m.agents) > 0 else 0
                ),
                "population": lambda m: len(m.agents),
                "minority_pc": lambda m: (
                    sum(1 for agent in m.agents if agent.type == 1)
                    / len(m.agents)
                    * 100
                    if len(m.agents) > 0
                    else 0
                ),
            },

            agent_reporters={"agent_type": "type"}
        )

        # Create agents and place them on the grid
        for cell in self.grid.all_cells:
            # Decide whether to place an agent in the current cell
            if self.random.random() < self.density:
                # Decide what type of agent to place in the cell
                agent_type = 1 if self.random.random() < scenario.minority_pc else 0
                SchellingAgent(
                    self,
                    cell,
                    agent_type,
                    homophily=scenario.homophily,
                    radius=scenario.radius,
                )

        # Collect initial state
        self.agents.do("assign_state")
        self.datacollector.collect(self)


    def step(self):
        """
        Run one step of the model.
        """
        self.happy = 0                               # Reset counter of happy agents
        self.agents.shuffle_do("step")               # Activate all agents in random order
        self.agents.do("assign_state")               # Determine if agent is happy and move if not
        self.datacollector.collect(self)             # Collect data
        self.running = self.happy < len(self.agents) # Keep running until all agents are happy
        