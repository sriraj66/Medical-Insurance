from django.db import models
from django.contrib.auth.models import User
ROLL = (
    ("0","insure"),
    ("1","provider")
)
STU = (
    ("0","single"),
    ("1","married")
)
POLICY = (
    ("Jeevan Policy 100 days","Jeevan Policy 100 days"),
)
STATUS = (
    ("0","Not Allotted"),
    ("1","Pending"),
    ("2","Allotted")
)
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True)
    roll = models.CharField(choices=ROLL,default='0',max_length=255)
    email = models.EmailField()
    created = models.DateField(auto_now_add=True)
    profile = models.FileField(upload_to='profile/')
    phone = models.CharField(max_length=255,blank=True,default="0")
    address = models.CharField(max_length=255,default="")
    account = models.CharField(max_length=255,blank=True,default="")
    private_key = models.CharField(max_length=255,blank=True,default="")
    def __str__(self):
        return self.name

class Insurer(models.Model):
    policy = models.CharField(default="Jeevan Policy 100 days",max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True)
    adhar = models.CharField(max_length=255,blank=True)
    dob = models.DateField()
    father_name = models.CharField(max_length=255,blank=True)
    mother_name = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    status = models.CharField(default='0',choices=STU,max_length=255,blank=True)
    qulification = models.CharField(max_length=255,blank=True)
    pob = models.CharField(max_length=255,blank=True)
    pan = models.CharField(max_length=255,blank=True)
    occupation = models.CharField(max_length=255,blank=True)
    AIncome = models.CharField(max_length=255,blank=True)
    climed_amt = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    amt_paid = models.FloatField()
    status = models.CharField(choices=STATUS,max_length=50,default='0')
    done = models.BooleanField(default=False)
    # paid_account = models.ForeignKey(XDC_Account)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return  self.policy +"-"+self.name

class XDC_Account(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    insure = models.ForeignKey(Insurer, on_delete=models.CASCADE)

    account = models.CharField(max_length=255,unique=True)
    privatekey = models.CharField(max_length=255)
    hashes = models.CharField(max_length=10000,default="[]",blank=True)
    amt_paid = models.FloatField(default=0)
    total_amt = models.FloatField(default=600)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    duedate = models.DateField(null=True)

class Claim_Insure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insure = models.ForeignKey(Insurer, on_delete=models.CASCADE)
    clime_form = models.FileField(upload_to='clime form/')
    pan = models.FileField(upload_to='pan/')
    photo = models.FileField(upload_to='pic/')
    adhar = models.FileField(upload_to='adhar/')
    bc =  models.FileField(upload_to='birth certificate/')
    created = models.DateTimeField(auto_now_add=True)
    dis = models.CharField(max_length=255,default="")
    clime_hash = models.CharField(default="",max_length=1000,blank=True)
    

class Provider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insurence = models.ManyToManyField(Insurer,blank=True)
    email = models.EmailField()
    amount_recived = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    amount_paid = models.FloatField(default=0)
