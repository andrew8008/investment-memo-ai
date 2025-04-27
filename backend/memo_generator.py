# backend/memo_generator.py

import os
import openai
from backend.prompts import SECTION_PROMPTS

# Load your OpenAI key (assuming you have it in .env and environment variables loaded)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_section(user_input_text, section_name, model="gpt-4"):
    """
    Generate one section of the investment memo based on user input and section template.
    
    Args:
        user_input_text (str): Raw input about the startup (e.g. founder bio, notes)
        section_name (str): Which section to generate (e.g. "summary", "market")
        model (str): Which OpenAI model to use (default "gpt-4")
        
    Returns:
        str: Generated investment memo section
    """
    # Step 1: Get the prompt template
    section_prompt = SECTION_PROMPTS.get(section_name)
    if not section_prompt:
        raise ValueError(f"Section '{section_name}' not found in SECTION_PROMPTS.")

    instructions = section_prompt["instructions"]
    example_input = section_prompt["example_input"]
    example_output = section_prompt["example_output"]
    
    # Step 2: Build the full prompt
    full_prompt = f"""
You are a professional investment analyst writing internal memos for angel investors.

Instructions:
{instructions}

Example:
Input: {example_input}
Output: {example_output}

Now write the Output for this Input:
Input: {user_input_text}
Output:
"""

    # Step 3: Send it to OpenAI
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional investment analyst helping investors make decisions."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.3,  # Keep it analytical and less "creative"
        max_tokens=500
    )

    # Step 4: Extract and return
    memo_section = response['choices'][0]['message']['content'].strip()
    return memo_section