
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import uvicorn

# Carrega modelo local (vai baixar na primeira vez)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI()

class EmbedRequest(BaseModel):
	texto: str

@app.post("/embed")
async def embed(req: EmbedRequest):
	embedding = model.encode(req.texto, convert_to_tensor=False)
	return {"embedding": embedding.tolist()}

# Teste local
if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
