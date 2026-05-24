import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def format_deadline(deadline):
    """Convert raw deadline string to readable format."""
    if not deadline or deadline == "Unknown":
        return "No deadline listed"
    try:
        return datetime.fromisoformat(deadline).strftime("%B %d, %Y at %I:%M %p")
    except:
        return deadline

def send_digest(subscriber, matches, summaries):
    """Send a daily contract digest email to a subscriber."""

    body = f"<h2>Good morning {subscriber['name']},</h2>"
    body += "<p>Here are today's government contract matches for your business:</p>"

    if len(matches) == 0:
        body += "<p>No new matching contracts today. Check back tomorrow.</p>"
    else:
        for i, contract in enumerate(matches):
            title = contract.get("title", "Untitled")
            deadline = format_deadline(contract.get("responseDeadLine"))
            link = contract.get("uiLink", "#")
            summary = summaries[i]

            body += "<hr>"
            body += f"<h3>{title}</h3>"
            body += f"<p><strong>Deadline:</strong> {deadline}</p>"
            body += f"<p>{summary}</p>"
            body += f"<p><a href='{link}'>View on SAM.gov</a></p>"

    body += f"<hr><p><small>Contract Seeker — <a href='https://contract-seeker.up.railway.app/unsubscribe?email={subscriber['email']}'>Unsubscribe</a></small></p>"

    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=subscriber["email"],
        subject=f"Your daily contract matches — {len(matches)} found today",
        html_content=body
    )

    client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    client.send(message)
    print(f"Email sent to {subscriber['email']}")