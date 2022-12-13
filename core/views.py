from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from datetime import *
from dateutil.relativedelta import relativedelta
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from .xdcpay import pay
def getData(request,field):
    return request.POST.get(field,0)

def index(request):

    return render(request, 'core/index.html',{})

def insure_pay(request,id):
    insure = Insurer.objects.get(id=id)
    to_acc = "xdc2c9d3e542e1dc0946bdc9798b35de1cfbecf18e4"
    profile = Profile.objects.get(user=request.user)
    amt = 100
    if request.POST:
        user = request.user
        account = getData(request, 'acc')
        pk = getData(request, 'pk')
        Tamt = 100*6
        
        obj= XDC_Account.objects.filter(
            user=user,insure=insure,
        )
        print(obj)
        print(obj)
        if len(obj) !=0:
            obj = obj[0]
            obj.account = account
            obj.insure=insure
            obj.amt_paid = obj.amt_paid + amt
            obj.total_amt = Tamt
            insure.amt_paid = obj.amt_paid
            print(obj.amt_paid,type(obj.total_amt))
            if obj.amt_paid>=obj.total_amt: 
                print("Plane Sucess")
                insure.done = True                
            else:
                insure.done = False
            obj.privatekey = pk
            obj.duedate = datetime.today().date() + relativedelta(months=+1)
        else:
            obj = XDC_Account(
            user=user,insure=insure,amt_paid=amt,total_amt=Tamt,account=account,privatekey=pk
            )
        
        profile.account = account
        profile.private_key = pk
        profile.save()

        result = pay(account, to_acc, pk, 100)
        if result['done']:
            success(request, result['msg']+" Hash : "+result['hash'])
            success(request, " Verify Here  "+result['url'])
            hashes = list(obj.hashes)
            print(hashes)
            hashes.append(result['hash'])
            obj.hashes = hashes
            print(hashes)
            print(obj.hashes)
            if obj.hashes == None:
                obj.hashes = []
        else:
            success(request,result['error'])
            return redirect('dash')
        obj.save()
        insure.save() 
        return redirect('dash')
    
    return render(request, 'core/insure_pay.html',{
        "insure":insure,
        "amt":amt,
        "to_acc":to_acc,
        "profile":profile,
    })

def dash(request):
    context = {
        "insure":Insurer.objects.filter(user=request.user),
        "climes":Claim_Insure.objects.filter(user=request.user),
        "account":XDC_Account.objects.filter(user=request.user),
        "profile":Profile.objects.get(user=request.user),
        "clime":Claim_Insure.objects.filter(user=request.user)
    }
    
    return render(request, 'core/dash.html',context)

def user_form(request):
    if request.POST:
        user = request.user
        policy =request.POST.get("pp","Jeevan Policy 100 days")
        print(policy)
        name = getData(request, "name")
        adhar = getData(request, "adhar")
        dob = getData(request, "dob")
        father_name = getData(request, "father")
        mother_name = getData(request, "mother")
        address = getData(request, "address")
        status = getData(request, "status")
        qulification = getData(request, "quli")
        pob = getData(request, "pob")
        pan = getData(request, "pan")
        AIncome = getData(request, "inc")
        occupation = getData(request, "occ")
        
        temp = Insurer.objects.filter(user=user)
        print(temp)
        s = False
        if len(temp)!=0:
            for i in temp:
                if i.policy == 'Jeevan Policy 100 days':
                    s = True
                    break
                else:
                    s = False
        print(s)
        if s is not True and len(temp) ==0:
            obj = Insurer(
                policy=policy,
                user=user,name=name,adhar=adhar,dob=dob,father_name=father_name,mother_name=mother_name,
                address=address,status=status,qulification=qulification,pob=pob,pan=pan,occupation=occupation,
                AIncome=AIncome,
                amt_paid=0
            )
            obj.save()
        else:
            success(request, "You Alredy Have This Insurance")
            return redirect('dash')
        return redirect(insure_pay,obj.id)

    return render(request, 'core/user.html',{})


def clime_insure(request):
    user = request.user
    insure = Insurer.objects.get(user=user)
    profile = Profile.objects.get(user=user)
    if request.POST:
        clime_form = request.FILES.get("cf")
        pan = request.FILES.get("pan")
        photo = request.FILES.get("photo")
        adhar = request.FILES.get("adhar")
        bc = request.FILES.get("bc")
        dis = getData(request, 'reson')

        obj = Claim_Insure(
            user=user,insure=insure,clime_form=clime_form,
            pan = pan,photo = photo,adhar = adhar,dis=dis,bc = bc
        )
        # Transwer money
        pk = "69072e6ff5ee48eefd9b4fe524838ceb8a7b0d674d515f278742df14795b1bb6"

        from_acc = "xdc2c9d3e542e1dc0946bdc9798b35de1cfbecf18e4"
        number = insure.amt_paid + ((2.4*6/100)*100)-0.5
        climed = pay(from_acc, profile.account, pk, round(number,2))
        if climed['done']:
            insure.status = 2
            obj.clime_hash = climed['hash']
            success(request, "Insurance Climed Check Your XDC wallet  "+str(round(number,2)))

        else:
            insure.status = 1
            success(request, "Insurance Pending! kindly Check Your XDC wallet")
        insure.climed_amt = str(round(number,2))
        obj.save()
        insure.save()
        # print("Waiting for Provider to Confirm!!")
        print('Climed')

        return redirect('dash')

    return render(request, 'core/clime.html',{
        'insure':insure
    })

def user_register(request):
    context = {}

    if request.POST:
        username = request.POST.get("username",'')
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        profile = request.FILES.get('img')
        
        p1 = request.POST.get('passwd')
        p2 = request.POST.get('cpassword')
        
        if p1==p2:
            obj = User.objects.create(first_name=fname,last_name=lname,email=email,username=username,password=p1)
            obj.set_password(p1)
            obj.save()
            pro = Profile(
                user=obj,
                name=fname+" "+lname,account="",private_key="",
                profile=profile,
                email=email,phone=phone,address=address,
            )
            pro.save()
            auth = authenticate(request,username=username,password=p2)
            if auth is not None:
                login(request, auth)
                return redirect('dash')
        else:
            success(request, "oops! something went wrong..")

    return render(request, 'auth/register.html',context)

def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('username','')
        passwd = request.POST.get('password','')

        user = authenticate(request,username=name,password=passwd)

        if user:
            login(request, user)
            return redirect('dash')

    return render(request, 'auth/login.html')

@login_required()
def user_logout(request):
    logout(request)
    return redirect('login')  