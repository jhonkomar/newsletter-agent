from graph.state import AgentState
from datetime import datetime
time = datetime.datetime.now()


initial_state = AgentState(
    topic=f"Look for coding or AI engineering competitions where registration is still open until {time} "
)