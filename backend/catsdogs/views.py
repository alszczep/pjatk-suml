import os

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from keras import models, preprocessing
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
import tempfile

from .blobStorage import download_model_from_blob, upload_image_to_blob, get_blob_file_url_with_sas_token
from .models import CatDogPrediction
from .serializers import CatDogPredictionSerializer


@api_view(["GET"])
def index(request):
    return HttpResponse("Api")


def load_model():
    model_path = "/app/saved_model.keras"

    print(os.listdir("/app"))

    if os.path.exists(model_path):
        print("Existing model found locally")
        return models.load_model(model_path)
    else:
        try:
            file = download_model_from_blob()
            with tempfile.NamedTemporaryFile(suffix=".keras", delete=True) as temp_file:
                temp_file.write(file.read())
                temp_file.flush()
                model = models.load_model(temp_file.name)
                return model
        except Exception as e:
            print("Error loading model from blob storage:")
            print(e)
            return None


@api_view(["POST"])
def predict(request):
    file = request.FILES.get("file")
    if file:
        model = load_model()

        image = Image.open(file)
        resized_image = image.resize((32, 32))
        img_array = preprocessing.image.img_to_array(resized_image)
        img_array = img_array.astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        file_url = upload_image_to_blob(file)

        prediction = CatDogPrediction.objects.create(
            file_url=file_url,
            predicted_class=predicted_class,
            prediction_date_time=timezone.now(),
            is_vote_positive=None,
            feedback=None,
            is_included_in_training_dataset=False,
        )

        return JsonResponse(
            {"predicted_class": int(predicted_class), "prediction_id": prediction.id},
            status=200,
        )
    return JsonResponse({"error": "No file provided"}, status=400)


@api_view(["GET"])
def all_predictions(request):
    queryset = CatDogPrediction.objects.all()
    serializer = CatDogPredictionSerializer(queryset, many=True)
    data = serializer.data

    for row in data:
        row["file_url"] = get_blob_file_url_with_sas_token(row["file_url"])

    return Response(serializer.data)


@api_view(["POST"])
def change_vote_and_feedback(request):
    prediction_id = request.data.get("prediction_id")
    is_vote_positive = request.data.get("is_vote_positive")
    feedback = request.data.get("feedback")

    prediction = CatDogPrediction.objects.filter(id=prediction_id).first()
    if prediction:
        prediction.is_vote_positive = is_vote_positive
        prediction.feedback = feedback
        prediction.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Prediction not found"}, status=404)
