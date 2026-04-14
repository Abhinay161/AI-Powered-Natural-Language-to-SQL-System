from fastapi import FastAPI
from pydantic import BaseModel
from vanna_setup import get_agent

app = FastAPI()
agent = get_agent()

class Query(BaseModel):
    question: str

def validate_sql(sql):
    if not sql:
        return False

    if not sql.strip().lower().startswith("select"):
        return False

    banned = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "EXEC"]
    for word in banned:
        if word in sql.upper():
            return False

    return True

@app.post("/chat")
def chat(q: Query):
    try:
        response = agent.send_message(q.question)
        sql = response.get("sql")

        if not validate_sql(sql):
            return {"error": "Invalid or unsafe SQL generated"}

        return response

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "NL2SQL API Running"}

@app.get("/health")
def health():
    return {"status": "ok"}