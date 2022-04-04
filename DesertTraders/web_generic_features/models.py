from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

UserModel = get_user_model()


class Collection(models.Model):
    TITLE_MAX_LEN = 50

    UPLOAD_TO_PATH = 'collections/'

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    image = models.ImageField(
        upload_to=UPLOAD_TO_PATH,
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
    TITLE_MAX_LEN = 50

    UPLOAD_TO_PATH = 'nfts/'

    MIN_VALIDATOR_VALUE = 0.000001

    CURRENCY_TYPE_CHOICES = [(type, type) for type in ['BTC', 'ETH', 'SOL']]
    CURRENCY_TYPE_MAX_LEN = 6

    MIN_QUANTITY_VALUE = 1

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    image = models.ImageField(
        upload_to=UPLOAD_TO_PATH,
    )

    price = models.FloatField(
        validators=(
            MinValueValidator(MIN_VALIDATOR_VALUE),
        ),
    )

    currency_type = models.CharField(
        max_length=CURRENCY_TYPE_MAX_LEN,
        choices=CURRENCY_TYPE_CHOICES,
    )

    quantity = models.IntegerField(
        validators=(
            MinValueValidator(MIN_QUANTITY_VALUE),
        ),
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Profile(models.Model):
    USERNAME_MAX_LEN = 30

    UPLOAD_TO_PATH = 'profile/'

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        blank=True,
        null=True,
    )

    profile_image = models.ImageField(
        upload_to=UPLOAD_TO_PATH,
        blank=True,
        null=True,
    )

    my_collection = models.ManyToManyField(
        NFT,
        through='Collected'
    )


class Collected(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    NFT = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=0
    )

