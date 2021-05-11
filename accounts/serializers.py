from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator


from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

def validate_password(password) -> str : #For custom password validation
    min_length = 7

    if len(password) < min_length:
        raise serializers.ValidationError(_(f'Password must be at least {min_length} characters.'))
    
    elif not any(char.isdigit() for char in password):
        raise serializers.ValidationError(_('Password must contain at least one digit.'))
    
    elif not any(char.isalpha() for char in password):
        raise serializers.ValidationError(_('Password must contain at least one letter.'))
    return password

def email_verification_flow(user) -> None:  # To send verification email
    user.generate_email_verification_token()
    mail_message = 'This is your email verification link'
    send_mail(
        'Email Verification at AUTH',
        f'{mail_message}  http://127.0.0.1:8000/accounts/verify_mail/{user.email_verification_token}',
        'from admin@email.com',
        [f'{user.email}'],
        fail_silently = False,)

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
                            validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    phone_no =PhoneNumberField(required = True,
                                validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(required = True, write_only = True,
                                validators = [validate_password])
    password2 = serializers.CharField(required = True, write_only = True,
                                validators = [validate_password])

    date_created = serializers.DateTimeField(format = "%H:%M, %d-%m-%Y", read_only = True,)

    class Meta:
        model = get_user_model()
        fields = ('id','email','first_name','last_name','phone_no','is_verified','date_created', 'password',
                    'password2')
        read_only_fields = ('id','is_verified','date_created','date_updated','is_staff','is_active',
                            'password_last_changed')


    def validate(self, attrs) -> str:
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(_('Passwords do not match'))
        
        return attrs
    
    def create(self, validated_data) -> get_user_model:
        user: get_user_model = get_user_model().objects.create(
                                email = validated_data['email'],
                                first_name = validated_data['first_name'],
                                last_name = validated_data['last_name'],
                                phone_no = validated_data['phone_no'],
                                )
        user.set_password(validated_data['password'])
     
        email_verification_flow(user)
        
        user.save()
        return user


    def update(self, instance: get_user_model, validated_data) -> get_user_model:
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class PasswordChangeSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(write_only = True, required = True,
                                    validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True,
                                    validators = [validate_password])
    old_password = serializers.CharField(write_only = True, required = True)
    password_last_changed = serializers.DateTimeField(read_only = True,)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'password', 'password2','password_last_changed')
        read_only_fields = ('password_last_changed')

    def validate(self, attrs) -> str:
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value) -> str:

        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data) -> get_user_model():

        instance.set_password(validated_data['password'])
        instance.password_last_changed = timezone.now()
        instance.save()

        return instance

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('email',)

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only = True, required = True,
                                    validators = [validate_password])
    new_password2 = serializers.CharField(write_only = True, required = True,
                                    validators = [validate_password])

    class Meta:
        model = get_user_model()
        fields = ('new_password', 'new_password2',)
    
    def validate(self, attrs) -> str:
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data) -> get_user_model():

        instance.set_password(validated_data['new_password'])
        instance.password_last_changed = timezone.now()
        instance.save()

        return instance