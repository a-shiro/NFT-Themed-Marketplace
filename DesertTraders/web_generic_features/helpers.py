from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from DesertTraders.web_generic_features.models import Collection, Collected


# For marketplace views
def get_collections_on_market():
    collections = Collection.objects.filter(posted_for_sale=True)

    return collections


def get_collection_with_pk(**kwargs):
    collection = Collection.objects.get(pk=kwargs['pk'])
    return collection


def transaction(profile, nft):
    if nft in profile.my_collection.all():
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


def get_tuple_my_nfts_with_nft_quantity(profile):
    result = []

    my_collection = profile.my_collection.all()
    for collected_nft in my_collection:
        nft_quantity = Collected.objects.filter(profile=profile, NFT=collected_nft).first().quantity
        result.append((collected_nft, nft_quantity))

    return result


def check_if_button_active(collections):
    for collection in collections:
        if not collection.posted_for_sale:
            return True
    return False
