from django.contrib import admin

from DesertTraders.web_generic_features.models import Collection, NFT, Profile, Balance


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'posted_for_sale')
    list_filter = ('posted_for_sale',)
    sortable_by = ('title', 'posted_for_sale')


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ('collection', 'title', 'price', 'quantity', 'blockchain')
    list_filter = ('collection', 'blockchain')
    sortable_by = ('title', 'posted_for_sale', 'price', 'quantity', 'blockchain')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username')
    sortable_by = ('username', )


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'balance')
    sortable_by = ('balance',)



