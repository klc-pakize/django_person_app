from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from dj_rest_auth.serializers import TokenSerializer

from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required = True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only = True, required = True, validators=[validate_password],
    style = {'input_type':'password'})
    password2 = serializers.CharField(write_only = True, required = True, style = {'input_type':'password'})
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"massega":"Password fields didint match!"}
            )
        return data


    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



#! We have customized the TokenSerializer so that when the user logs in, not only the key information is returned, but also personal information.
class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]

class CustomTokenSerializer(TokenSerializer):

    user = UserTokenSerializer(read_only = True)

    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")



class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(required = False)
    class Meta:

        model = Profile
        fields = ["id","user","user_id","display_name","avatar","bio"]

#! In order not to get the user_id from the front end, we add the user_id part to automatically edit it with the help of the token while the profile owner is updating the profile from their environment.

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)  # We reached the parent with super(). We wanted it to continue using the default update method for fields in parent.
        instance.user_id = self.context["request"].user.id  # instance = represents a row in the profile table in the database, we recorded the id of the user who made the request in the user_id of that row.
        instance.save()
        return instance
        