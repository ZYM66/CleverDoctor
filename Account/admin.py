from django.contrib import admin
from .models import Account, DiagnosticRecords
# Register your models here.

admin.site.register([Account, DiagnosticRecords])
