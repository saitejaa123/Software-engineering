from dataclasses import dataclass, field
from typing import List


@dataclass
class Agent:
    name: str
    expertise: List[str]
    solved_count: int
    review_score: float
    active_tickets: int = 0


@dataclass
class Ticket:
    ticket_id: str
    customer_id: str
    subject: str
    description: str
    severity: str = "medium"
    predicted_category: str = "general"
    priority_score: float = 0.0
    assigned_to: str = ""
    status: str = "open"


@dataclass
class Feedback:
    ticket_id: str
    agent_name: str
    rating: int
    comment: str = ""


@dataclass
class AssignmentResult:
    ticket: Ticket
    ranked_agents: List[Agent] = field(default_factory=list)
