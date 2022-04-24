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

    DEFAULT_LIKES_VALUE = 0

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

    blockchain = models.CharField(
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

    likes = models.IntegerField(
        default=DEFAULT_LIKES_VALUE
    )

    class Meta:
        verbose_name = 'NFT'

    def __str__(self):
        return self.title


class Profile(models.Model):
    USERNAME_MAX_LEN = 30

    UPLOAD_TO_PATH = 'profile/'

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
    )

    profile_image = models.ImageField(
        upload_to=UPLOAD_TO_PATH,
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to=UPLOAD_TO_PATH,
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    collection = models.ManyToManyField(
        NFT,
        through='Collected'
    )

    def __str__(self):
        return self.username


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


class Collected(models.Model):
    DEFAULT_COLLECTED_QUANTITY = 0

    DEFAULT_FAVORITE_VALUE = False

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    NFT = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=DEFAULT_COLLECTED_QUANTITY
    )

    favorite = models.BooleanField(
        default=DEFAULT_FAVORITE_VALUE
    )

    class Meta:
        verbose_name_plural = "Profile's collection"


class Balance(models.Model):
    DEFAULT_PROFILE_BALANCE = 10000

    balance = models.FloatField(
        default=DEFAULT_PROFILE_BALANCE
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True,
    )
