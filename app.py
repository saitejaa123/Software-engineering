import argparse
import json
from dataclasses import asdict
from pathlib import Path

from support_system.engine import process_ticket
from support_system.models import Agent, Ticket


def load_agents() -> list[Agent]:
    raw = json.loads(Path("data/agents.json").read_text())
    return [Agent(**item) for item in raw]


def load_tickets() -> list[Ticket]:
    raw = json.loads(Path("data/tickets.json").read_text())
    return [Ticket(**item) for item in raw]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart support assignment demo")
    parser.add_argument("--export", type=Path, help="Export processed tickets to a JSON file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agents = load_agents()
    tickets = load_tickets()

    processed_tickets = [process_ticket(ticket, agents) for ticket in tickets]
    processed_tickets.sort(key=lambda t: t.priority_score, reverse=True)

    print("\nSmart Support Ticket Assignment\n" + "-" * 34)
    for ticket in processed_tickets:
        print(
            f"{ticket.ticket_id}: priority={ticket.priority_score:<5.1f} "
            f"severity={ticket.severity:<8} category={ticket.predicted_category:<15} assigned_to={ticket.assigned_to}"
        )

    if args.export:
        payload = [asdict(t) for t in processed_tickets]
        args.export.write_text(json.dumps(payload, indent=2))
        print(f"\nExported processed tickets to {args.export}")


if __name__ == "__main__":
    main()
