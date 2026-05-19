import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_digest(subscriber, matches, summaries):
    """Send a daily contract digest email to a subscriber."""

    # Build the email body
    body = f"<h2>Good morning {subscriber['name']},</h2>"
    body += f"<p>Here are today's government contract matches for your business:</p>"

    if len(matches) == 0:
        body += "<p>No new matching contracts today. Check back tomorrow.</p>"
    else:
        for i, contract in enumerate(matches):
            title = contract.get("title", "Untitled")
            deadline = contract.get("responseDeadLine", "Unknown")
            link = contract.get("uiLink", "#")
            summary = summaries[i]

            body += f"<hr>"
            body += f"<h3>{title}</h3>"
            from datetime import datetime
            deadline_formatted = datetime.fromisoformat(deadline).strftime("%B %d, %Y at %I:%M %p") if deadline != "Unknown" else "Unknown"
            body += f"<p><strong>Deadline:</strong> {deadline_formatted}</p>"
            body += f"<p>{summary}</p>"
            body += f"<p><a href='{link}'>View on SAM.gov</a></p>"

    body += "<hr><p><small>Contract Scanner — unsubscribe anytime.</small></p>"

    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=subscriber["email"],
        subject=f"Your daily contract matches — {len(matches)} found today",
        html_content=body
    )

    client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    client.send(message)
    print(f"Email sent to {subscriber['email']}")