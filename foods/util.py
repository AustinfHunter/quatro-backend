from django.core.exceptions import ObjectDoesNotExist
from .models import AbridgedBrandedFoodItem
from .serializers import AbridgedBrandedFoodSerializer
from .fdcclient import get_fdc_client
from django.http import Http404


def get_or_create_food(fdc_id: int) -> AbridgedBrandedFoodItem:
    try:
        food = AbridgedBrandedFoodItem.objects.get(fdc_id=fdc_id)
        return food
    except ObjectDoesNotExist:
        client = get_fdc_client()
        fdc_food = client.get_food(fdc_ids=f"{fdc_id}", format="full").json()[0]
        result_food = AbridgedBrandedFoodSerializer(data=fdc_food)
        if result_food.is_valid():
            return result_food.save()
        else:
            raise Http404("Food does not exist")
