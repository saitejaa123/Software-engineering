from typing import Iterable

from support_system.models import Agent, Feedback


def apply_feedback(agents: Iterable[Agent], feedback: Feedback) -> bool:
    for agent in agents:
        if agent.name == feedback.agent_name:
            normalized_rating = max(1, min(5, feedback.rating))
            agent.review_score = round((agent.review_score * 0.8) + (normalized_rating * 0.2), 2)
            return True
    return False
