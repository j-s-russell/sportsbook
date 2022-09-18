from django.contrib import admin

# Register your models here.
from .models import User, League, Game, Bet, Market, Update

admin.site.register(User)
admin.site.register(League)
admin.site.register(Game)
admin.site.register(Bet)
admin.site.register(Market)
admin.site.register(Update)