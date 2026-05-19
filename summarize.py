import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarize_contract(contract):
    """Send a contract to Claude and get a plain English summary back."""
    
    title = contract.get("title", "Unknown")
    agency = contract.get("fullParentPathName", "Unknown agency")
    deadline = contract.get("responseDeadLine", "Unknown")
    naics = contract.get("naicsCode", "Unknown")
    description_url = contract.get("description", "No description available")

    prompt = f"""You are helping a small contractor understand a government contract opportunity.

Here are the details:
Title: {title}
Agency: {agency}
Deadline: {deadline}
NAICS Code: {naics}
Description link: {description_url}

Write a 2-3 sentence plain English summary of this contract opportunity. 
Focus on: what the job is, who posted it, and when the bid is due.
Keep it simple — write like you're explaining it to a small business owner, not a lawyer.
Do not use markdown, bullet points, or any special formatting. Plain sentences only."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

# Test with a fake contract
test_contract = {
    "title": "Electrical work at LA Federal Building",
    "fullParentPathName": "DEPT OF HOMELAND SECURITY.FEDERAL PROTECTIVE SERVICE",
    "responseDeadLine": "2026-06-01T17:00:00-05:00",
    "naicsCode": "238210",
    "description": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=abc123"
}

summary = summarize_contract(test_contract)
print(summary)