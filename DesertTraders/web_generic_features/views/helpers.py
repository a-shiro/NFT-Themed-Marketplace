from django.core import exceptions as dj_exceptions

from DesertTraders.web_generic_features.models import Collection, Collected, Favorite, NFT

ORDER_BY_VALUES = ['-price', 'price', 'quantity']


def get_most_popular():
    result = {}

    collections = Collection.objects.filter(posted_for_sale=True)

    for collection in collections:
        total_collection_likes = 0
        for nft in collection.nft_set.all():
            total_collection_likes += nft.likes

        result[collection] = total_collection_likes

    sorted_result = list({k: v for k, v in sorted(result.items(), key=lambda item: -item[1])})[0:9]

    return sorted_result


def get_nfts_and_quantity(profile):
    result = []

    collections = profile.collected_set.all()
    for collected_nft in collections:
        nft = collected_nft.NFT
        nft_quantity = collected_nft.quantity

        result.append((nft, nft_quantity))

    return result


def get_nfts_and_favorite(iterable, **kwargs):
    result = []

    if not kwargs.get('ordering') in ORDER_BY_VALUES:
        ordering = 'title'
    else:
        ordering = kwargs.get('ordering')

    for nft in iterable.order_by(ordering):
        try:
            favorite = Favorite.objects.get(profile=kwargs['profile'], nft=nft).favorite

        except dj_exceptions.ObjectDoesNotExist:
            instance = Favorite(profile=kwargs['profile'], nft=nft)
            instance.save()
            favorite = instance.favorite

        result.append((nft, favorite))

    return result


def get_nfts_when_user_anonymous(iterable, **kwargs):
    result = []

    if not kwargs.get('ordering') in ORDER_BY_VALUES:
        ordering = 'title'
    else:
        ordering = kwargs.get('ordering')

    for nft in iterable.order_by(ordering):
        result.append((nft, False))

    return result


def validate_user_info(request, owner_pk):
    if owner_pk != request.user.pk:
        raise dj_exceptions.BadRequest
    return None


def check_if_button_active(user):
    sellable_collections = len(Collection.objects.filter(user=user, posted_for_sale=False))

    if sellable_collections > 0:
        return True
    return False
