from rest_framework import serializers
from .models import UserFoodRestriction, UserFoodPreference


class ResponseDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class UserFoodRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodRestriction
        fields = "__all__"


class UserFoodRestrictionListSerializer(serializers.Serializer):
    restrictions = UserFoodRestrictionSerializer(many=True)


class UserFoodRestrictionDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodRestriction
        fields = ["fdc_id", "reason"]

    def create(self, validated_data):
        user = self.context["request"].user
        restriction = UserFoodRestriction.objects.create(
            user=user, fdc_id=validated_data["fdc_id"], reason=validated_data["reason"]
        )
        return restriction


class UserFoodPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodPreference
        fields = "__all__"


class UserFoodPreferenceListSerializer(serializers.Serializer):
    preferences = UserFoodPreferenceSerializer(many=True)


class UserFoodPreferencesDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodPreference
        fields = ["fdc_id", "dislikes"]

    def create(self, validated_data):
        user = self.context["request"].user
        preference = UserFoodPreference.objects.create(
            user=user, fdc_id=validated_data["fdc_id"], dislikes=validated_data["dislikes"]
        )
        return preference


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
    unitName = serializers.CharField()


class FoodNutrientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()
    dataPoints = serializers.IntegerField
    min = serializers.FloatField()
    max = serializers.FloatField()
    type = serializers.CharField()
    nutrient = NutrientSerializer()
    foodNutrientDerivation = FoodNutrientDerivationSerializer()
    nutrientAnalysisDetails = NutrientAnalysisDetailsSerializer()


class AbridgedNutrientSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    name = serializers.CharField()
    amount = serializers.FloatField()
    unitName = serializers.CharField()
    derivationCode = serializers.CharField()
    derivationDescription = serializers.CharField()


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
    brandOwner = serializers.CharField()
    gtinUpc = serializers.CharField()
    nbdNumber = serializers.CharField()
    foodCode = serializers.CharField()


class LabelNutrientSerializer(serializers.Serializer):
    value = serializers.FloatField()


class LableNutrientsSerializer(serializers.Serializer):
    fat = LabelNutrientSerializer()
    saturated_fat = LabelNutrientSerializer()
    cholesterol = LabelNutrientSerializer()
    sodium = LabelNutrientSerializer()
    carbohydrates = LabelNutrientSerializer()
    fiber = LabelNutrientSerializer()
    sugars = LabelNutrientSerializer()
    protein = LabelNutrientSerializer()
    calcium = LabelNutrientSerializer()
    iron = LabelNutrientSerializer()
    potassium = LabelNutrientSerializer()
    callories = LabelNutrientSerializer()


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
    labelNutrients = LableNutrientsSerializer()


class FoodSearchCriteriaSerializer(serializers.Serializer):
    query = serializers.CharField()
    dataType = serializers.CharField()
    pageSize = serializers.IntegerField()
    pageNumber = serializers.IntegerField()
    sortBy = serializers.CharField()
    sortOrder = serializers.CharField()
    brandOwner = serializers.CharField()


class SearchResultFoodSerializer(serializers.Serializer):
    fdcId = serializers.IntegerField()
    dataType = serializers.CharField()
    description = serializers.CharField()
    foodCode = serializers.CharField()
    foodNutrients = AbridgedNutrientSerializer(many=True)
    publicationDate = serializers.DateField()
    scientificName = serializers.CharField()
    brandOwner = serializers.CharField()
    gtinUpc = serializers.CharField()
    ingredients = serializers.CharField()
    nbdNumber = serializers.CharField()
    additionalDescriptions = serializers.CharField()
    allHighlightFields = serializers.CharField()
    score = serializers.FloatField()


class SearchResultSerializer(serializers.Serializer):
    foodSearchCriteria = FoodSearchCriteriaSerializer()
    totalHits = serializers.IntegerField()
    currentPage = serializers.IntegerField()
    totalPages = serializers.IntegerField()
    foods = SearchResultFoodSerializer(many=True)
