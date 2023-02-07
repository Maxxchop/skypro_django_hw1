from rest_framework import serializers

from ads.models import Ad, Category
from authentication.models import Location, User


class NotPublishedValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("Couldn't be published")


class AgeAtLeastValidator:
    def __init__(self, min_age):
        self.min_age = min_age

    def __call__(self, value):
        if value < self.min_age:
            raise serializers.ValidationError(f'Age should be at least {self.min_age} years')


class BadDomainValidator:
    def __init__(self, bad_domains):
        if not isinstance(bad_domains, list):
            bad_domains = [bad_domains]
        self.bad_domains = bad_domains

    def __call__(self, value):
        if value.split('@')[1] in self.bad_domains:
            raise serializers.ValidationError('This domain is not allowed')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        many=True
    )

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        many=True
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        slug_field='name',
        many=True,
        queryset=Location.objects.all()
    )
    age = serializers.IntegerField(required=False, default=18, validators=[AgeAtLeastValidator(9)])
    email = serializers.EmailField(required=False, validators=[BadDomainValidator(['rambler.ru'])])
    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(
                name=location,
                defaults={
                    "lat": 0,
                    "lng": 0
                    }
                )
            user.locations.add(location_obj)

        user.set_password(user.password)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        slug_field='name',
        many=True,
        queryset=Location.objects.all()
    )
    username = serializers.CharField(max_length=20, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(
                name=location,
                defaults={
                    "lat": 0,
                    "lng": 0
                    }
                )
            user.locations.add(location_obj)
        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class AdDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[NotPublishedValidator()])
    class Meta:
        model = Ad
        fields = '__all__'
