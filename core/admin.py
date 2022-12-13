from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Insurer)
admin.site.register(XDC_Account)
admin.site.register(Claim_Insure)
admin.site.register(Provider)

