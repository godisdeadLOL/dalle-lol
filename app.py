if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

from fastapi import Depends, FastAPI, HTTPException, Request
from KeyStash import KeyStash
from exceptions import GenerationFailedException, KeyStashEmptyException
from security import verify_token
from utils import generate_image

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.state.key_stash = KeyStash()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/models")
async def models(_=Depends(verify_token)):
    return {"data": [{"id": "dall-e-2"}, {"id": "dall-e-3"}]}


@app.post("/images/generations")
async def generations(request: Request, _=Depends(verify_token)):
    key_stash: KeyStash = request.app.state.key_stash
    body = await request.json()

    try:
        result = await generate_image(key_stash, body)
    except KeyStashEmptyException:
        raise HTTPException(400, "Luck runs out")
    except GenerationFailedException as e:
        raise HTTPException(e.status_code, e.detail)

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
