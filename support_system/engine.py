from typing import List

from support_system.assignment import assign_ticket
from support_system.feedback import apply_feedback
from support_system.models import Agent, Feedback, Ticket
from support_system.nlp import predict_ticket_labels


def process_ticket(ticket: Ticket, agents: List[Agent], sentiment_hint: str = "neutral") -> Ticket:
    combined_text = f"{ticket.subject} {ticket.description}"
    severity, category, priority = predict_ticket_labels(combined_text, sentiment_hint=sentiment_hint)
    ticket.severity = severity
    ticket.predicted_category = category
    ticket.priority_score = priority
    return assign_ticket(ticket, agents)


def close_ticket(ticket: Ticket, agents: List[Agent], feedback: Feedback | None = None) -> Ticket:
    ticket.status = "closed"
    if feedback:
        apply_feedback(agents, feedback)

    for agent in agents:
        if agent.name == ticket.assigned_to and agent.active_tickets > 0:
            agent.active_tickets -= 1
            break

    return ticket
