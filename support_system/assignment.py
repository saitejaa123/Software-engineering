from typing import List, Tuple

from support_system.models import Agent, Ticket

SEVERITY_WEIGHT = {
    "critical": 1.50,
    "high": 1.25,
    "medium": 1.00,
    "low": 0.80,
}


def _agent_score(ticket: Ticket, agent: Agent) -> float:
    expertise_score = 1.0 if ticket.predicted_category in agent.expertise else 0.2
    performance_score = (agent.review_score / 5.0) + (agent.solved_count / 150.0)
    load_penalty = max(0.1, 1.0 - (agent.active_tickets * 0.1))
    severity_multiplier = SEVERITY_WEIGHT.get(ticket.severity, 1.0)
    return expertise_score * performance_score * load_penalty * severity_multiplier


def rank_agents_for_ticket(ticket: Ticket, agents: List[Agent]) -> List[Agent]:
    weighted_agents: List[Tuple[float, int, Agent]] = []
    for agent in agents:
        final_score = _agent_score(ticket, agent)
        weighted_agents.append((final_score, -agent.active_tickets, agent))

    weighted_agents.sort(key=lambda row: (row[0], row[1]), reverse=True)
    return [agent for _, _, agent in weighted_agents]


def assign_ticket(ticket: Ticket, agents: List[Agent]) -> Ticket:
    ranked = rank_agents_for_ticket(ticket, agents)
    if not ranked:
        return ticket

    winner = ranked[0]
    winner.active_tickets += 1
    ticket.assigned_to = winner.name
    return ticket
