from DesertTraders.web_generic_features.models import Collection, Collected, NFT


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


def check_if_button_active(user):
    sellable_collections = len(Collection.objects.filter(user=user, posted_for_sale=False))

    if sellable_collections > 0:
        return True
    return False


def get_profile_nfts_and_nft_quantity(profile):
    result = []

    collections = profile.my_collection.all()
    for collected_nft in collections:
        nft_quantity = Collected.objects.get(profile=profile, NFT=collected_nft).quantity
        result.append((collected_nft, nft_quantity))

    return result


def match_users(session_user_pk, **kwargs):
    if session_user_pk == kwargs['pk']:
        return True
    return False


def validate_info(profile, nft):
    nft_quantity_left = nft.quantity
    transaction_cost = profile.balance.balance - nft.price

    if nft_quantity_left == 0 or transaction_cost < 0:
        return True  # Invalid
    return False  # Valid


def is_owner(request, collection):
    collection_owner_pk = collection.user.pk

    if collection_owner_pk != request.user.pk:
        return True
    return False