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

    today = datetime.now().strftime("%B %d, %Y")

    # Email header
    body = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        
        <!-- Header -->
        <div style="background: #2D6A4F; padding: 28px 32px; border-radius: 8px 8px 0 0;">
            <span style="font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">Contract<span style="color: #A7DFC9;">Seeker</span></span>
        </div>

        <!-- Greeting -->
        <div style="padding: 32px 32px 8px;">
            <p style="font-size: 20px; font-weight: 600; color: #1a1a1a; margin: 0 0 8px;">Good morning, {subscriber['name']}</p>
            <p style="font-size: 14px; color: #888; margin: 0;">{today} · {len(matches)} contract{'s' if len(matches) != 1 else ''} matched your profile</p>
        </div>

        <div style="padding: 0 32px;">
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        </div>
    """

    if len(matches) == 0:
        body += """
        <div style="padding: 20px 32px 32px;">
            <p style="font-size: 15px; color: #666; line-height: 1.6;">No new matching contracts today. We'll keep scanning and send you matches as soon as they appear.</p>
        </div>
        """
    else:
        for i, contract in enumerate(matches):
            title = contract.get("title", "Untitled")
            deadline = format_deadline(contract.get("responseDeadLine"))
            link = contract.get("uiLink", "#")
            summary = summaries[i]

            body += f"""
        <div style="padding: 20px 32px;">
            <p style="font-size: 11px; font-weight: 600; color: #2D6A4F; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px;">Contract {i + 1} of {len(matches)}</p>
            <p style="font-size: 17px; font-weight: 600; color: #1a1a1a; margin: 0 0 10px; line-height: 1.4;">{title}</p>
            <div style="background: #F7F7F5; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px;">
                <p style="font-size: 13px; color: #555; margin: 0;"><strong style="color: #333;">Deadline:</strong> {deadline}</p>
            </div>
            <p style="font-size: 14px; color: #444; line-height: 1.7; margin: 0 0 14px;">{summary}</p>
            <a href="{link}" style="display: inline-block; font-size: 13px; font-weight: 600; color: #2D6A4F; text-decoration: none; border: 1.5px solid #2D6A4F; padding: 8px 18px; border-radius: 6px;">View on SAM.gov →</a>
        </div>
        <div style="padding: 0 32px;">
            <hr style="border: none; border-top: 1px solid #eee; margin: 8px 0;">
        </div>
            """

    # Footer
    body += f"""
        <div style="padding: 24px 32px 32px; text-align: center;">
            <p style="font-size: 12px; color: #bbb; margin: 0 0 6px;">You're receiving this because you signed up at ContractSeeker.</p>
            <a href="https://contract-seeker.up.railway.app/unsubscribe?email={subscriber['email']}" style="font-size: 12px; color: #999; text-decoration: underline;">Unsubscribe</a>
        </div>

    </div>
    """

    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=subscriber["email"],
        subject=f"📋 {len(matches)} contract{'s' if len(matches) != 1 else ''} matched your profile — {today}",
        html_content=body
    )

    client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    client.send(message)
    print(f"Email sent to {subscriber['email']}")