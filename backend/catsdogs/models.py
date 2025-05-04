from django.db import models

class CatDogPrediction(models.Model):
    file_url = models.CharField(max_length=2000)
    predicted_class = models.IntegerField()
    prediction_date_time = models.DateTimeField()
    is_vote_positive = models.BooleanField(null=True, blank=True, default=None)
    feedback = models.CharField(max_length=2000, null=True, blank=True, default=None)
    is_included_in_training_dataset = models.BooleanField(default=False)
