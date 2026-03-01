import unittest

from support_system.assignment import assign_ticket
from support_system.engine import close_ticket, process_ticket
from support_system.feedback import apply_feedback
from support_system.models import Agent, Feedback, Ticket
from support_system.nlp import compute_priority, predict_category, predict_severity


class SupportSystemTests(unittest.TestCase):
    def test_severity_prediction(self):
        text = "Production outage and users cannot login"
        self.assertEqual(predict_severity(text), "critical")

    def test_severity_word_boundary(self):
        text = "Customer mentioned terror concerns in message"
        self.assertEqual(predict_severity(text), "medium")

    def test_category_prediction(self):
        text = "Need refund due to wrong payment charge"
        self.assertEqual(predict_category(text), "billing")

    def test_priority_scoring(self):
        self.assertGreater(compute_priority("critical"), compute_priority("medium"))

    def test_assignment_prefers_expertise(self):
        agents = [
            Agent("BillingPro", ["billing"], solved_count=50, review_score=4.2),
            Agent("TechPro", ["technical"], solved_count=300, review_score=4.8),
        ]
        ticket = Ticket("1", "c1", "Invoice issue", "wrong payment charge", predicted_category="billing")
        assigned = assign_ticket(ticket, agents)
        self.assertEqual(assigned.assigned_to, "BillingPro")

    def test_feedback_updates_rating(self):
        agents = [Agent("Aisha", ["billing"], solved_count=100, review_score=4.0)]
        updated = apply_feedback(agents, Feedback("T1", "Aisha", rating=5))
        self.assertTrue(updated)
        self.assertGreater(agents[0].review_score, 4.0)

    def test_close_ticket_reduces_load_and_applies_feedback(self):
        agents = [Agent("Aisha", ["billing"], solved_count=100, review_score=4.0, active_tickets=1)]
        ticket = Ticket("1", "c1", "Invoice issue", "wrong payment charge")
        processed = process_ticket(ticket, agents)
        self.assertEqual(processed.assigned_to, "Aisha")

        closed = close_ticket(processed, agents, Feedback("1", "Aisha", rating=5))
        self.assertEqual(closed.status, "closed")
        self.assertEqual(agents[0].active_tickets, 1)
        self.assertGreater(agents[0].review_score, 4.0)


if __name__ == "__main__":
    unittest.main()
