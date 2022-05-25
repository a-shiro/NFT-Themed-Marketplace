from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

from DesertTraders.web_generic_features.validators import max_image_size

UserModel = get_user_model()


class Collection(models.Model):
    __TITLE_MAX_LEN = 50

    __UPLOAD_TO_PATH = 'collections/'

    title = models.CharField(
        max_length=__TITLE_MAX_LEN,
    )

    image = models.ImageField(
        upload_to=__UPLOAD_TO_PATH,
        validators=(
            max_image_size,
        )
    )

    cover_image = models.ImageField(
        upload_to=__UPLOAD_TO_PATH,
        validators=(
            max_image_size,
        ),
        blank=True,
        null=True,
    )

    description = models.TextField()

    posted_for_sale = models.BooleanField(
        default=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class NFT(models.Model):
    __TITLE_MAX_LEN = 50

    __UPLOAD_TO_PATH = 'nfts/'

    __MIN_VALIDATOR_VALUE = 0.000001

    __CURRENCY_TYPE_CHOICES = [(type, type) for type in ['BTC', 'ETH', 'SOL']]
    __CURRENCY_TYPE_MAX_LEN = 6

    __MIN_QUANTITY_VALUE = 1

    __DEFAULT_LIKES_VALUE = 0

    title = models.CharField(
        max_length=__TITLE_MAX_LEN,
    )

    image = models.ImageField(
        upload_to=__UPLOAD_TO_PATH,
        validators=(
            max_image_size,
        )
    )

    price = models.FloatField(
        validators=(
            MinValueValidator(__MIN_VALIDATOR_VALUE),
        ),
    )

    blockchain = models.CharField(
        max_length=__CURRENCY_TYPE_MAX_LEN,
        choices=__CURRENCY_TYPE_CHOICES,
    )

    quantity = models.IntegerField(
        validators=(
            MinValueValidator(__MIN_QUANTITY_VALUE),
        ),
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
    )

    likes = models.IntegerField(
        default=__DEFAULT_LIKES_VALUE
    )

    def __str__(self):
        return self.title


class Profile(models.Model):
    __USERNAME_MAX_LEN = 30

    __DEFAULT_BALANCE_VALUE = 10000

    __UPLOAD_TO_PATH = 'profile/'

    username = models.CharField(
        max_length=__USERNAME_MAX_LEN,
    )

    balance = models.FloatField(
        default=__DEFAULT_BALANCE_VALUE
    )

    profile_image = models.ImageField(
        upload_to=__UPLOAD_TO_PATH,
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to=__UPLOAD_TO_PATH,
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.username


class Collected(models.Model):
    __DEFAULT_COLLECTED_QUANTITY = 0

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    nft = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=__DEFAULT_COLLECTED_QUANTITY
    )

    def __str__(self):
        return f'{self.profile.username} {self.nft.title}'


class Favorite(models.Model):
    __FAVORITE_DEFAULT = False

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    nft = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    favorite = models.BooleanField(
        default=__FAVORITE_DEFAULT
    )

    def __str__(self):
        return f'{self.profile.username} {self.nft.title}'
