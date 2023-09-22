from rest_framework import serializers

from .models import Cat, Owner, Achievement


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(read_only=True, many=True)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')




