import os
import solara
from model import Schelling, SchellingScenario
from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component
)
from mesa.visualization.components import AgentPortrayalStyle


def get_happy_agents(model):
    """
    Display a text count of how many happy agents there are.
    """
    return solara.Markdown(f"**Happy agents: {model.happy}**")


path = os.path.dirname(os.path.abspath(__file__))


def agent_portrayal(agent):

    # Defualt agent style
    style = AgentPortrayalStyle(
        x = agent.cell.coordinate[0],
        y = agent.cell.coordinate[1],
        marker=os.path.join(path, "resources", "orange_happy.png"),
        size=50
    )
    if agent.type == 0:
        if agent.happy:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "blue_happy.png")
                )
            )
        else:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "blue_unhappy.png")
                ),
                ("size", 50),
                ("zorder", 2),
            )
    else:
        if not agent.happy:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "orange_unhappy.png")
                ),
                ("size", 50),
                ("zorder", 2),
            )
    
    return style

model_params = {
    "rng": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    # Note: floating-point numbers are: the initial slider value, the min, the max, and the increment size.
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1), 
    "minority_pc": Slider("Fraction minority", 0.2, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily", 0.4, 0.0, 1.0, 0.125),
    "width": 20, 
    "height": 20,
}

# Note: Models with images as markers are very performance intensive.
model1 = Schelling(scenario=SchellingScenario())
renderer = SpaceRenderer(model1, backend="matplotlib").setup_agents(agent_portrayal)

# Here we use renderer.render() to render the agents and grid in one go. 
# This function always renders the grid and then renders the agents or
# preoperty layers on top of  it if specified.
renderer.render()

HappyPlot = make_plot_component({"happy": "tab:green"})


"""
The below code creates a Solara visualization page for your Mesa model.

SolaraViz(...) constructs a page using:

    model1 as the Mesa model
    renderer to draw the grid/agents
    components as extra UI pieces:
    HappyPlot for a plot
    get_happy_agents for the Markdown count
    model_params to expose parameters as controls
    page becomes the UI page object.

page #noqa is just a no-op expression used in notebook-like contexts to display the page, 
while #noqa tells linters not to complain about a bare expression.
"""
page = SolaraViz(
    model1,
    renderer,
    components = [
        HappyPlot,
        get_happy_agents,
    ],
    model_params=model_params,
)
page #noqa


