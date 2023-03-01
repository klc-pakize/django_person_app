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
        # Calculates the number of people belonging to a department
        # Bir departmana ait kişi sayısını hesaplar
        return obj.personnels.count()  


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
#! Personeli oluştururken user token ile işlem yapıyoruz ve otomatik olarak create user_id bölümüne ulaşıyoruz.
    def create(self, validated_data):
        validated_data["create_user_id"] = self.context["request"].user.id 
        instance = Personnel.objects.create(**validated_data)
        return instance


#! The time elapsed from the date of employment of the personnel to this date
#! Personelin işe giriş tarihinden bu tarihe kadar geçen süre
    def get_days_since_jained(self, obj):
        return (now() - obj.start_date).days



class DepartmentPersonnelSerializer(serializers.ModelSerializer):
    
    personnel_count = serializers.SerializerMethodField()
    personnels = PersonnelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = ("id", "name", "personnel_count", "personnels")
        
    def get_personnel_count(self, obj):
        # Calculates the number of people belonging to a department
        # Bir departmana ait kişi sayısını hesaplar
        return obj.personnels.count() 