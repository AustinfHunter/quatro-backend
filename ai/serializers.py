from rest_framework import serializers


class ChatBotQuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class ChatBotResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
