
import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, field_validator
from sentence_transformers import SentenceTransformer
import uvicorn

_EMBED_API_KEY = os.getenv("EMBED_API_KEY", "")

# Carrega modelo local (vai baixar na primeira vez)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI()

class EmbedRequest(BaseModel):
	texto: str

	@field_validator("texto")
	@classmethod
	def validate_length(cls, v: str) -> str:
		if len(v) > 10_000:
			raise ValueError("texto must not exceed 10,000 characters")
		return v

@app.post("/embed")
async def embed(req: EmbedRequest, x_api_key: str = Header(default="")):
	if not _EMBED_API_KEY or x_api_key != _EMBED_API_KEY:
		raise HTTPException(status_code=401, detail="Invalid or missing API key")
	embedding = model.encode(req.texto, convert_to_tensor=False)
	return {"embedding": embedding.tolist()}

if __name__ == "__main__":
	reload = os.getenv("UVICORN_RELOAD", "false").lower() == "true"
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
