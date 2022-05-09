from django.core import exceptions as django_exceptions

from DesertTraders.web_generic_features.models import Collection, Collected, Favorite, NFT


def transaction(request, nft):
    profile = request.user.profile

    if nft in profile.collection.all():
        collected_nft = Collected.objects.get(profile=profile, NFT=nft)
        collected_nft.quantity += 1
        collected_nft.save()
    else:
        profile_collection = Collected(profile=profile, NFT=nft, quantity=1)
        profile_collection.save()

    profile.balance.balance -= nft.price
    nft.quantity -= 1

    profile.balance.save()
    nft.save()


def check_if_button_active(user):
    sellable_collections = len(Collection.objects.filter(user=user, posted_for_sale=False))

    if sellable_collections > 0:
        return True
    return False


def get_profile_nfts_and_nft_quantity(profile):
    result = []

    collections = profile.collection.all()
    for collected_nft in collections:
        nft_quantity = Collected.objects.get(profile=profile, NFT=collected_nft).quantity
        result.append((collected_nft, nft_quantity))

    return result


def validate_info(profile, nft):
    nft_quantity_left = nft.quantity
    transaction_cost = profile.balance.balance - nft.price

    if nft_quantity_left == 0 or transaction_cost < 0:
        return True  # Invalid
    return False  # Valid


def validate_user_info(request, owner_pk):
    if owner_pk != request.user.pk:
        raise django_exceptions.BadRequest
    return None


def validate_and_sell(request, collection):
    owner_pk = collection.user.pk

    validate_user_info(request, owner_pk)

    collection.posted_for_sale = True
    collection.save()

    return None


def validate_and_remove(request, instance):
    if isinstance(instance, Collection):
        owner_pk = instance.user.pk
    else:
        owner_pk = instance.collection.user.pk

    validate_user_info(request, owner_pk)

    instance.delete()

    return None


def favorite_nft(request, nft):

    if nft.favorite:
        nft.favorite = False
        nft.nft.likes -= 1
    else:
        nft.favorite = True
        nft.nft.likes += 1

    nft.save()
    nft.nft.save()


def get_nfts_and_favorite(iterable, **kwargs):
    result = []

    ordering = kwargs.get('ordering')  # get ordering func here
    if not ordering:
        ordering = 'title'

    for nft in iterable.order_by(ordering):
        try:
            favorite = Favorite.objects.get(profile=kwargs['profile'], nft=nft).favorite

        except django_exceptions.ObjectDoesNotExist:
            instance = Favorite(profile=kwargs['profile'], nft=nft)
            instance.save()
            favorite = instance.favorite

        result.append((nft, favorite))

    return result


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