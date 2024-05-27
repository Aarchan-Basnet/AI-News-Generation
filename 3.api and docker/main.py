from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from PIL import Image
import io
from typing import List
from clip1 import get_title
from title2news import gen_article

app = FastAPI()

def get_titles_list(
    titles: List[str] = Form(...)
) -> List[str]:
    return titles

@app.post("/upload-inputs/")
async def upload_inputs(file: UploadFile = File(...),
                        string1: str = Form(...),
                        string2: str = Form(...),
                        string3: str = Form(...)
):
    try:
        # Read the image data from the uploaded file
        image_data = await file.read()

        # Open the image using Pillow
        image_bytes = io.BytesIO(image_data)
        image = Image.open(image_bytes)
        # # Get image details
        # image_format = image.format
        # image_size = image.size
        titles = [string1, string2, string3]

        pred_title = get_title(titles, image_bytes)
        article = gen_article(pred_title)

        return JSONResponse(content={
            'title': pred_title,
            'article': article
        })
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
