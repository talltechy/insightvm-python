from trial_and_error.insight_agents import get_insight_agents

# Retrieve the first page of agents with a page size of 50
agents = get_insight_agents(page=1, page_size=50)

# Print the list of agents
print(agents)
