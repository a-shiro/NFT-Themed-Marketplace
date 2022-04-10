from DesertTraders.web_generic_features.models import Collection, Profile, Collected


def get_tuple_collection_with_profile():
    result = []

    collections = Collection.objects.filter(posted_for_sale=True)
    for collection in collections:
        profile = Profile.objects.filter(user_id=collection.user.id).first()
        result.append((collection, profile))

    return result


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