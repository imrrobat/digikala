from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.utils.timezone import localtime


admin.site.register(ShippingAddress)
# admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # readonly_fields = ['date_ordered', 'last_update']
    readonly_fields = ['formatted_date_ordered', 'formatted_last_update']
    inlines = [OrderItemInLine]
    
    def formatted_date_ordered(self, obj):
        return localtime(obj.date_ordered).strftime("%Y-%m-%d %H:%M") 
    formatted_date_ordered.short_description = "تاریخ سفارش"

    def formatted_last_update(self, obj):
        return localtime(obj.last_update).strftime("%Y-%m-%d %H:%M")
    formatted_last_update.short_description = "آخرین ویرایش"


