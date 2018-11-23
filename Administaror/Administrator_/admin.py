from django.contrib import admin

from .models import Lottery, Barrage, Activity, Barrage2

admin.site.register(Lottery)
admin.site.register(Barrage)
admin.site.register(Barrage2)
admin.site.register(Activity)
