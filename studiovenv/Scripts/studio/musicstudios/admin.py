from django.contrib import admin
from django import forms
from . models import Customer, Product, Price, Order, FrequentlyAsked, SampleSong

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Customer, OrderAdmin)
admin.site.register(Product, OrderAdmin)
admin.site.register(Price, OrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FrequentlyAsked, OrderAdmin)
admin.site.register(SampleSong, OrderAdmin)