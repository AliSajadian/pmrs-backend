from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.models import Group, Permission

from accounts.models import *


#=========== Authorization Serializers ============
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'full_name', 'user_img')

class UserExSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')
                
class UserGroupSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    
    class Meta:
        model = get_user_model()    
        fields = ['id', 'groups']
        
class UserGroupsExSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    # serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'groups') 

class GroupPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    
    class Meta:
        model = Group    
        fields = ['id', 'permissions']

class GroupPermissionsExSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')
        
class UserPermissionSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    
    class Meta:
        model = get_user_model()    
        fields = ['id', 'user_permissions']

class UserPermissionsExSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'user_permissions')    
        
        
class UserContractPermissionsSerializers(serializers.ModelSerializer):
    permissions = serializers.ReadOnlyField()
    class Meta:
        model = UserRole
        fields = ['userid', 'contractid', 'permissions']
        
#=========== Authentication Serializers ============
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['username'],
        validated_data['email'], validated_data['password'])

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Have Incorrect Credentials")

class PasswordSerializer(serializers.Serializer):
    userid = serializers.IntegerField()
    username = serializers.CharField()
    currentpassword = serializers.CharField()
    newpassword = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
        # instance.userid = validated_data.get('userid', instance.userid)
        # instance.password = validated_data.get('hashedNewPassword', instance.password)
        # instance.save()
        # return instance

    def validate(self, data):
        """ check that userid and new password are different """
        if data["username"] == data["newpassword"]:
            raise serializers.ValidationError("username and new password should be different")
        return data

    def validate_password(self, value):
        """
        check if new password meets the specs
        min 1 lowercase and 1 uppercase alphabet
        1 number
        1 special character
        8-16 character length
        """

        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError("It should be between 8 and 16 characters long")

        if not any(x.isupper() for x in value):
            raise serializers.ValidationError("It should have at least one upper case alphabet")

        if not any(x.islower() for x in value):
            raise serializers.ValidationError("It should have at least one lower case alphabet")

        if not any(x.isdigit() for x in value):
            raise serializers.ValidationError("It should have at least one number")

        valid_special_characters = {'@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')',
                                    '<', '>', '?', '/', '|', '{', '}', '~', ':'}

        if not any(x in valid_special_characters for x in value):
            raise serializers.ValidationError("It should have at least one special character")

        return value


