import json
import os
from flask import Flask, Response, request
from flask_cors import CORS

model_cache_dir = os.path.join(os.getcwd(), "models")

os.environ["HF_HOME"] = model_cache_dir

from transformers import AutoImageProcessor, AutoModel
from services.minio_service import MinioService

app = Flask(__name__)
CORS(app)
minio_client = MinioService()

processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
model = AutoModel.from_pretrained("facebook/dinov2-base")

print("Embedding server is ready")


@app.get("/health_check")
def health_check():
    return Response(
        status=200,
        response=json.dumps({
            "status": "ok"
        })
    )


@app.post("/generate_embedding")
def generate_embedding():
    try:
        req_body_json = request.get_json()
        image_object_key = req_body_json.get("image_object_key")

        image = minio_client.get_file(image_object_key)

        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state

        array = last_hidden_states.cpu().detach().numpy()

        return Response(
            status=200,
            response=json.dumps({
                "embedding": array.tolist()
            })
        )

    except Exception as err:
        print(f"Error in generating embedding : {err}")

        return Response(
            status=500,
            response=json.dumps({
                "status": "Error in generating embedding",
                "error": str(err)
            })
        )


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5545)
