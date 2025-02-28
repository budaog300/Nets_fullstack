import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from .models import *


class SportTypesSerializer(serializers.ModelSerializer):
    # cat = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = SportTypes
        fields = ("id", "name", "cat")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", )


class ClubsSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Clubs
        fields = ("id", "name", "director", "time_create", "address")


class VeteransSerializer(serializers.ModelSerializer):
   # achievements = serializers.JSONField(required=False, default=list)
    class Meta:
        model = Veterans
        fields = ("id", "last_name", "first_name", "patronymic", "get_full_name", "gender", "age_group", "sport", "photo", "club", "achievements")
        extra_kwargs = {
            'patronymic': {'required': False},
            'photo': {'required': False},
            'achievements': {'required': False},
        }




# class SportTypesSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return SportTypes.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance


# class ClubsSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     time_create = serializers.DateTimeField(read_only=True)
#     director_id = serializers.IntegerField()
#     address = serializers.CharField(max_length=255)
#
#     def create(self, validated_data):
#         return Clubs.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.director_id = validated_data.get("director_id", instance.director_id)
#         instance.address = validated_data.get("address", instance.address)
#         instance.save()
#         return instance

