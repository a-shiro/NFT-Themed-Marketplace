from django.shortcuts import redirect

from DesertTraders.web_generic_features.models import Collection, Collected, NFT


def get_collections_on_market():
    collections = Collection.objects.filter(posted_for_sale=True)

    return collections


def get_collection_with_pk(**kwargs):
    collection = Collection.objects.get(pk=kwargs['pk'])
    return collection


def get_nft_with_pk(**kwargs):
    nft = NFT.objects.get(pk=kwargs['pk'])
    return nft


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


def get_profile_collections(user):
    collections = Collection.objects.filter(user=user).order_by('-posted_for_sale')

    return collections


def check_if_button_active(user):
    collections = Collection.objects.filter(user=user, posted_for_sale=False)

    if len(collections) > 0:
        return True
    return False


def get_profile_nfts_and_nft_quantity(profile):
    result = []

    collections = profile.my_collection.all()
    for collected_nft in collections:
        nft_quantity = Collected.objects.get(profile=profile, NFT=collected_nft).quantity
        result.append((collected_nft, nft_quantity))

    return result


def users_match(session_user_pk, **kwargs):
    if session_user_pk == kwargs['pk']:
        return True
    return False
