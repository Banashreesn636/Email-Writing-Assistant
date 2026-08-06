def create_prompt(tone, purpose, recipient, message):
    prompt = f"""
You are an expert email writer.

Write a complete email.

Tone:
{tone}

Purpose:
{purpose}

Recipient:
{recipient}

Details:
{message}

Generate only the email.
"""
    return prompt