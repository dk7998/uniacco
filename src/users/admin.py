import csv
from django.contrib import admin

from .models import User, UserLoginHistory


def csv_file(modeladmin, request, queryset):
    f = open('LoginHistory.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['user', 'ip address'])
    for q in queryset:
        writer.writerow([q.user.username, q.ip])

class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip']
    actions      = [csv_file]


admin.site.register(User)
admin.site.register(UserLoginHistory, UserLoginHistoryAdmin)