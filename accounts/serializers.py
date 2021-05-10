from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

def validate_password(password) -> str :
    min_length = 7

    if len(password) < min_length:
        raise serializers.ValidationError(_(f'Password must be at least {min_length} characters.'))
    
    elif not any(char.isdigit() for char in password):
        raise serializers.ValidationError(_('Password must contain at least one digit.'))
    
    elif not any(char.isalpha() for char in password):
        raise serializers.ValidationError(_('Password must contain at least one letter.'))
    return password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
                            validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    phone_no =PhoneNumberField(required = True,
                                validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(required = True, write_only = True,
                                validators = [validate_password])
    date_created = serializers.DateTimeField(format = "%H:%M, %d-%m-%Y", read_only = True,)

    class Meta:
        model = get_user_model()
        fields = ('id','email','first_name','last_name','phone_no','is_verified','date_created', 'password')
        read_only_fields = ('id','is_verified','date_created','date_updated','is_staff','is_active',)

    
    def create(self, validated_data) -> get_user_model:
        user: get_user_model = get_user_model().objects.create_user(**validated_data)
        return user


    def update(self, instance: get_user_model, validated_data) -> get_user_model:
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
