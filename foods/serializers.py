from rest_framework import serializers
from .models import (
    UserFoodRestriction,
    UserFoodPreference,
    AbridgedBrandedFoodItem,
    LabelNutrients,
    Nutrient,
    FoodNutrient,
)


class ResponseDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class NutrientAcquisitionDetailsSerializer(serializers.Serializer):
    sampleUnitId = serializers.IntegerField()
    purchaseDate = serializers.DateField()
    storeCity = serializers.CharField()
    storeState = serializers.CharField()


class NutrientAnalysisDetailsSerializer(serializers.Serializer):
    subSampleId = serializers.IntegerField()
    amount = serializers.IntegerField()
    nutrientId = serializers.IntegerField()
    labMethodDescription = serializers.CharField()
    labMethodOriginal_description = serializers.CharField()
    labMethodLink = serializers.URLField()
    labMethodTechnique = serializers.CharField()
    nutrientAcquisitionDetails = NutrientAcquisitionDetailsSerializer()


class FoodNutrientSourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    description = serializers.CharField()


class FoodNutrientDerivationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    description = serializers.CharField()
    foodNutrientSource = FoodNutrientSourceSerializer()


class NutrientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.CharField()
    name = serializers.CharField()
    rank = serializers.IntegerField()
    unitName = serializers.CharField(source="unit_name")


class FoodNutrientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()
    dataPoints = serializers.IntegerField()
    min = serializers.FloatField()
    max = serializers.FloatField()
    type = serializers.CharField()
    nutrient = NutrientSerializer()
    foodNutrientDerivation = FoodNutrientDerivationSerializer()
    nutrientAnalysisDetails = NutrientAnalysisDetailsSerializer()


class AbridgedNutrientSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    amount = serializers.FloatField(required=False)
    unitName = serializers.CharField(required=False)
    derivationCode = serializers.CharField(required=False)
    derivationDescription = serializers.CharField(required=False)


class FoodCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    descriiption = serializers.CharField()


class FoodComponentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    dataPoints = serializers.IntegerField()
    gramWeight = serializers.FloatField()
    isRefuse = serializers.BooleanField()
    minYearAcquired = serializers.IntegerField()
    percentWeight = serializers.FloatField()


class MeasureUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    abbreviation = serializers.CharField()
    name = serializers.CharField()


class FoodPortionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()
    dataPoints = serializers.IntegerField()
    gramWeight = serializers.FloatField()
    minYearAcquired = serializers.IntegerField()
    modifier = serializers.CharField()
    portionDescription = serializers.CharField()
    sequenceNumber = serializers.IntegerField()
    measureUnit = MeasureUnitSerializer()


class SampleFoodItemSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodClass = serializers.CharField()
    publicaitonDate = serializers.DateField()
    foodAttributes = FoodCategorySerializer(many=True)


class InputFoodFoundationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    foodDescription = serializers.CharField()
    inputFood = SampleFoodItemSerializer()


class NutrientConversionFactorSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    value = serializers.FloatField()


class FoundationFoodItemSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodClass = serializers.CharField()
    footNote = serializers.CharField()
    isHistoricalReference = serializers.BooleanField()
    nbdNumber = serializers.CharField()
    publicationDate = serializers.DateField()
    scientificName = serializers.CharField()
    foodCategory = FoodCategorySerializer()
    foodNutrients = FoodNutrientSerializer(many=True)
    foodComponents = FoodComponentSerializer(many=True)
    foodPortions = FoodPortionSerializer(many=True)
    inputFoods = InputFoodFoundationSerializer(many=True)
    nutrientConversionFactors = NutrientConversionFactorSerializer(many=True)


class FoodAttributeTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()


class FoodAttributeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sequence_number = serializers.IntegerField()
    value = serializers.CharField()
    foodAttributeType = FoodAttributeTypeSerializer()


class AbridgedFoodItemSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodNutrients = AbridgedNutrientSerializer(many=True)
    publicationDate = serializers.DateField()
    brandOwner = serializers.CharField(required=False, default="")
    gtinUpc = serializers.CharField(required=False, default="")
    nbdNumber = serializers.CharField(required=False, default="")
    foodCode = serializers.CharField(required=False, default="")


class AbridgedFoodItemListSerializer(serializers.Serializer):
    foods = AbridgedFoodItemSerializer(many=True)


class LabelNutrientSerializer(serializers.Serializer):
    value = serializers.FloatField()


class LabelNutrientsSerializer(serializers.Serializer):
    fat = LabelNutrientSerializer(required=False)
    saturatedFat = LabelNutrientSerializer(required=False, source="saturated_fat")
    transFat = LabelNutrientSerializer(required=False, source="trans_fat")
    cholesterol = LabelNutrientSerializer(
        required=False,
    )
    sodium = LabelNutrientSerializer(required=False)
    carbohydrates = LabelNutrientSerializer(required=False)
    fiber = LabelNutrientSerializer(required=False)
    sugars = LabelNutrientSerializer(required=False)
    protein = LabelNutrientSerializer(required=False)
    calcium = LabelNutrientSerializer(required=False)
    iron = LabelNutrientSerializer(required=False)
    potassium = LabelNutrientSerializer(required=False)
    calories = LabelNutrientSerializer(required=False)


class FoodUpdateLogSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    availableDate = serializers.DateField()
    brandOwner = serializers.CharField()
    dataSource = serializers.CharField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodClass = serializers.CharField()
    gtinUpc = serializers.CharField()
    houseHoldServingFullText = serializers.CharField()
    ingredients = serializers.CharField()
    modifiedDate = serializers.DateField()
    publicationDate = serializers.DateField()
    servingSize = serializers.IntegerField()
    servingSize_unit = serializers.CharField()
    brandedFoodCategory = serializers.CharField()
    changes = serializers.CharField()
    foodAttributes = FoodAttributeSerializer(many=True)


class BrandedFoodItemSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    availableDate = serializers.DateField()
    brandOwner = serializers.CharField()
    dataSource = serializers.CharField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodClass = serializers.CharField()
    gtinUpc = serializers.CharField()
    householdServingFullText = serializers.CharField()
    ingredients = serializers.CharField()
    modifiedDate = serializers.DateField()
    publicationDate = serializers.DateField()
    servingSize = serializers.IntegerField()
    servingSizeUnit = serializers.CharField()
    brandedFoodCategory = serializers.CharField()
    foodNutrients = FoodNutrientSerializer(many=True)
    foodUpdateLog = FoodUpdateLogSerializer(many=True)
    labelNutrients = LabelNutrientsSerializer()


class AbridgedFoodNutrientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()
    nutrient = NutrientSerializer()


class AbridgedBrandedFoodSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField(source="fdc_id")
    brandOwner = serializers.CharField(source="brand_owner", allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    ingredients = serializers.CharField(allow_blank=True)
    servingSize = serializers.FloatField(source="serving_size")
    servingSizeUnit = serializers.CharField(source="serving_size_unit", allow_blank=True)
    foodNutrients = AbridgedFoodNutrientSerializer(many=True, source="food_nutrients")
    labelNutrients = LabelNutrientsSerializer(required=False)

    def create(self, validated_data):
        food_nutrients = validated_data.pop("food_nutrients")
        label_nutrients = validated_data.pop("labelNutrients")
        food, _ = AbridgedBrandedFoodItem.objects.get_or_create(**validated_data)
        nutrients = []
        fnutrients = []
        for food_nutrient in food_nutrients:
            n = food_nutrient.pop("nutrient")
            nutrient = Nutrient(**n)
            nutrients.append(nutrient)
            fnutrients.append(FoodNutrient(**food_nutrient, nutrient=nutrient))
        Nutrient.objects.bulk_create(nutrients, ignore_conflicts=True)

        FoodNutrient.objects.bulk_create(fnutrients, ignore_conflicts=True)

        for nutrient in fnutrients:
            food.food_nutrients.add(nutrient)
        print(label_nutrients)
        for k, v in label_nutrients.items():
            label_nutrients[k] = v["value"]
        lnutrients = LabelNutrients.objects.create(**label_nutrients)
        food.label_nutrients = lnutrients
        food.save()
        return food


class AbridgedBrandedFoodListSerializer(serializers.Serializer):
    foods = AbridgedBrandedFoodSerializer(many=True)


class SearchResultNutrientSerializer(serializers.Serializer):
    nutrientId = serializers.IntegerField()
    nutrientNumber = serializers.IntegerField()
    nutrientName = serializers.CharField()
    value = serializers.FloatField()
    unitName = serializers.CharField()
    derivationCode = serializers.CharField()
    derivationDescription = serializers.CharField()


class FoodSearchCriteriaSerializer(serializers.Serializer):
    query = serializers.CharField()
    dataType = serializers.CharField(required=False)
    pageSize = serializers.IntegerField(required=False)
    pageNumber = serializers.IntegerField(required=False)
    sortBy = serializers.CharField(required=False)
    sortOrder = serializers.CharField(required=False)
    brandOwner = serializers.CharField(required=False)


class SearchResultFoodSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodCode = serializers.CharField(required=False)
    foodNutrients = SearchResultNutrientSerializer(many=True, required=False)
    publicationDate = serializers.DateField(required=False)
    scientificName = serializers.CharField(required=False)
    brandOwner = serializers.CharField()
    gtinUpc = serializers.CharField(required=False)
    ingredients = serializers.CharField()
    nbdNumber = serializers.CharField(required=False)
    additionalDescriptions = serializers.CharField(required=False)
    allHighlightFields = serializers.CharField(required=False)
    score = serializers.FloatField()


class SearchResultSerializer(serializers.Serializer):
    foodSearchCriteria = FoodSearchCriteriaSerializer()
    totalHits = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    totalPages = serializers.IntegerField()
    foods = SearchResultFoodSerializer(many=True)


class UserFoodRestrictionSerializer(serializers.ModelSerializer):
    food_details = serializers.SerializerMethodField()

    class Meta:
        model = UserFoodRestriction
        fields = "__all__"

    def get_food_details(self, obj) -> AbridgedBrandedFoodSerializer:
        print("obj")
        print(obj)
        return AbridgedBrandedFoodSerializer(obj.food).data


class UserFoodRestrictionListSerializer(serializers.Serializer):
    restrictions = UserFoodRestrictionSerializer(many=True)


class UserFoodRestrictionDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodRestriction
        fields = ["reason"]

    def create(self, validated_data):
        user = self.context["request"].user
        food = self.context["food"]
        restriction = UserFoodRestriction(user=user, food=food, reason=validated_data["reason"])
        restriction.save()
        return restriction


class UserFoodPreferenceSerializer(serializers.ModelSerializer):
    food_details = serializers.SerializerMethodField()

    class Meta:
        model = UserFoodPreference
        fields = "__all__"

    def get_food_details(self, obj) -> AbridgedBrandedFoodSerializer:
        return AbridgedBrandedFoodSerializer(obj.food).data


class UserFoodPreferenceListSerializer(serializers.Serializer):
    preferences = UserFoodPreferenceSerializer(many=True)


class UserFoodPreferencesDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodPreference
        fields = ["dislikes"]

    def create(self, validated_data):
        user = self.context["request"].user
        food = self.context["food"]
        preference = UserFoodPreference(user=user, food=food, dislikes=validated_data["dislikes"])
        preference.save()
        return preference


class UserFoodDetailsSerializer(serializers.Serializer):
    food_details = AbridgedBrandedFoodSerializer()
    is_liked = serializers.BooleanField()
    is_disliked = serializers.BooleanField()
    is_restricted = serializers.BooleanField()
