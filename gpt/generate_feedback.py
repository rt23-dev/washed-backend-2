import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feedback(score_data):
    prompt = f"""
You are a golf coach. A user just completed a golf swing and here is the analysis output:

Score Data: {json.dumps(score_data, indent=2)}

Based on this data, provide detailed feedback on the user's swing. Include specific tips for improvement, focusing on both pose and club tracking aspects. The feedback should be encouraging and constructive, helping the user understand what they did well and what they can improve.

Make sure to format the feedback in a clear and structured way, suitable for a user who is looking to improve their golf swing.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and encouraging golf coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()
