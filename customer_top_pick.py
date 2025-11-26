from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List
import asyncio
import os
from dotenv import load_dotenv

# Load .env
load_dotenv(".env")

#
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))

# here we make the pydantic model  structure response model
class TopPickResult(BaseModel):
#     This model defines the structure of the output returned from the agent.
#     'picks'  → list of selected top models.
#     'reason' → explanation why these models were selected.
    picks: List[str]
    reason: str

# now we have to Create a Custom Top Pick Selection Agent
custom_top_pick_agent = Agent(
    name="custom_top_pick_agent",
    model="groq:llama-3.3-70b-versatile",
    instructions="""
You are a Top Pick Selection Agent.
Rules:
- Always prefer the latest / highest-numbered model when comparing similar items.
-These phones offer the best performance, camera quality, and long-term support. Mid-range devices like Vivo Y21 and Tecno Commo 40 Pro do not compete in flagship-level performance.
- Treat all items as real and available.
- Select only the most advanced devices.
Return output only in JSON:
{"picks": [...], "reason": "..."}
"""


)
# Function to run the Agent with item list in this at the end you can see the list item 
async def get_top_picks(items: List[str]):
    prompt = f"Select the best top picks from: {items}"
    
    # Run the AI agent and wait for its response
    response = await custom_top_pick_agent.run(prompt)

    cleaned_output = response.output.strip()   #now we hav to  Remove extra spaces or newline characters from the response.
    if cleaned_output.startswith('```json') and cleaned_output.endswith('```'):   # If the output starts with ```json and ends with ``` (meaning it's fenced markdo
        cleaned_output = cleaned_output[len('```json'):-len('```')].strip()  #   Remove the opening ```json and closing ``` to extract ONLY the pure JSON

    return TopPickResult.model_validate_json(cleaned_output)      # Convert the cleaned JSON text into a TopPickResult Pydantic model

# Main function
async def main():
    items = [
        "Samsung S24 Ultra",
        "iPhone 16",
        "Google Pixel 9",
        "Tecno Commo 40 Pro",
        "Vivo Y 21",
        "iphone 17"
    ]
    result = await get_top_picks(items)
    print("\nTop Picks Result:\n", result)

if __name__ == "__main__":
    asyncio.run(main())

# Run in Colab
# await main()
