from django.core.exceptions import ObjectDoesNotExist
from .models import AbridgedBrandedFoodItem
from .serializers import AbridgedBrandedFoodSerializer
from .fdcclient import get_fdc_client


def get_or_create_food(fdc_id: int) -> AbridgedBrandedFoodItem:
    try:
        AbridgedBrandedFoodItem.objects.get(fdc_id=fdc_id)
    except ObjectDoesNotExist:
        client = get_fdc_client()
        fdc_food = client.get_food(fdc_ids=f"{fdc_id}", format="full")[0]
        return AbridgedBrandedFoodSerializer(fdc_food).save()
