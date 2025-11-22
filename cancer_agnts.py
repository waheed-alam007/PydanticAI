
from dataclasses import dataclass
from typing import Any
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

load_dotenv()

# DATABASE 
@dataclass
class Patient:
    id: int
    name: str
    age: int
    history: dict[str, Any]

PATIENT_DB = {
    1: Patient(1, "Ali Khan", 58, {"cancer_history": "none"}),
    2: Patient(2, "Sara Ahmed", 45, {"cancer_history": "breast - treated 2019"}),
}

class DatabaseConn:
    async def patient_info(self, id: int) -> dict[str, Any]:
        p = PATIENT_DB.get(id)
        if not p:   # if patient does not exist
            return {"name": "Unknown", "age": None, "history": {}}
        return {"name": p.name, "age": p.age, "history": p.history}

# ------------------- OUTPUT MODEL -------------------
class CancerOutput(BaseModel):
    response_text: str
    recommend_tests: bool
    urgent_referral: bool
    urgency: int = Field(ge=0, le=10)

# AGENT 
cancer_agent = Agent(
    model="groq:llama-3.3-70b-versatile",  
    deps_type=DatabaseConn,           # class used for data access
    result_type=CancerOutput,            # AI outputs this structure

    system_prompt=(
        "You are a cancer triage assistant. "
        "Provide safe, helpful, structured clinical triage. "
        "Urgency from 0–10."
    )
)

# SYSTEM PROMPT HOOK (Adds patient info inside system prompt
@cancer_agent.system_prompt
async def patient_context(ctx: RunContext[DatabaseConn]) -> str:
    pid = ctx.deps.patient_id
    info = await ctx.deps.patient_info(pid)
    return (
        f"Patient name: {info['name']}. "
        f"Age: {info['age']}. "
        f"History: {info['history']}."
    )

# MAIN TRIAGE FUNCTION (Runs the AI agent)
async def run_triage(pid: int, symptoms: str):
    deps = DatabaseConn()
    deps.patient_id = pid   # attach patient id

 # Call the AI model
    result = await cancer_agent.run(f"Symptoms: {symptoms}", deps=deps)
# All structured output is inside result.data
    out = result.data   

    print("\n--- TRIAGE RESULT ---")
    print("Advice:", out.response_text)
    print("Recommend Tests:", out.recommend_tests)
    print("Urgent Referral:", out.urgent_referral)
    print("Urgency:", out.urgency)
    print("----------------------\n")

#  here is the ENTRY POINT .
if __name__ == "__main__":
    try:
        pid = int(input("Enter patient ID: ").strip())
    except:
        print("Invalid ID.")
        exit()

    symptoms = input("Enter symptoms: ").strip()

    asyncio.run(run_triage(pid, symptoms))

