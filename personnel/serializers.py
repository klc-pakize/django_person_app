from rest_framework import serializers

from django.utils.timezone import now

from .models import Department, Personnel

class DepartmentSerializer(serializers.ModelSerializer):

    personnel_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "personnel_count",
        )

    def get_personnel_count(self, obj):
        return obj.personnels.count()  # Calculates the number of people belonging to a department


class PersonnelSerializer(serializers.ModelSerializer):

    create_user = serializers.StringRelatedField()
    create_user_id = serializers.IntegerField(required = False)
    days_since_jained = serializers.SerializerMethodField()
    class Meta:
        model = Personnel
        fields = (
            "id",
            "department",
            "create_user",
            "create_user_id",
            "first_name",
            "last_name",
            "title",
            "gender",
            "salary",
            "start_date",
            "days_since_jained",
        )

#! While creating the personnel, we process with the user token and reach the create user_id section automatically
    def create(self, validated_data):
        validated_data["create_user_id"] = self.context["request"].user.id 
        instance = Personnel.objects.create(**validated_data)
        return instance


#! The time elapsed from the date of employment of the personnel to this date
    def get_days_since_jained(self, obj):
        return (now() - obj.start_date).days



class DepartmentPersonnelSerializer(serializers.ModelSerializer):
    
    personnel_count = serializers.SerializerMethodField()
    personnels = PersonnelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = ("id", "name", "personnel_count", "personnels")
        
    def get_personnel_count(self, obj):
        return obj.personnels.count() # Calculates the number of people belonging to a department