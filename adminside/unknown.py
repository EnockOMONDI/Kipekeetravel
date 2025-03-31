
        from django.db import models
from django.contrib.auth.models import User
from users.models import UserBookings
from django.db.models import BigAutoField
from django.urls import reverse
from django.utils import timezone
# from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = CloudinaryField('image', blank=True, null=True)
  
    

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def packages_in_category(self):
        return self.packages.all().count()

    def get_absolute_url(self):
        return reverse('packages:packages_list_by_category', args=[self.slug])

class Destination(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    dtn_description = models.TextField()
  # image = CloudinaryField('image', blank=True, null=True)


    def __str__(self):
        return f'{self.name}'


class Accomodation(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_description = models.TextField()
    #hotel_image = CloudinaryField('image', blank=True, null=True)
    price_per_room = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.hotel_name}'

class Travel(models.Model):
    
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price_per_person = models.PositiveIntegerField()

    ## For Travelling Choices
    TRAIN = 'TN'
    FLIGHT = 'FT'
    BUS = 'BS'

    TRAVELLING_CHOICES = [
        (TRAIN, 'Train'),
        (FLIGHT, 'Flight'),
        (BUS, 'Bus')
    ]

    travelling_mode = models.CharField(max_length=2,choices=TRAVELLING_CHOICES,default=FLIGHT)

    def __str__(self):
        return f'{self.departure} to {self.arrival} | {self.travelling_mode}'


class Package(models.Model):
    ## RelationShip Keys 
    destination = models.ForeignKey(Destination,null=True, on_delete=models.CASCADE)
    accomodation = models.ForeignKey(Accomodation,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='packages', null=True, on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel,on_delete=models.CASCADE)
    bookings = models.ManyToManyField(User,through=UserBookings)

    ## Attributes
    package_name = models.CharField(max_length=200,default="NULL") # ye dalna
    adult_price = models.IntegerField()
    child_price = models.IntegerField() 
    # image = CloudinaryField('image', blank=True, null=True)
    description = models.TextField(default="NO DESCRIPTION ADDED")  
    inclusive = models.TextField()
    exclusive = models.TextField()
    slug = models.SlugField(max_length=100, db_index=True, default='safaris')
    number_of_days = models.PositiveIntegerField()
    number_of_times_booked = models.PositiveIntegerField(default=0)
    pub_date = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-pub_date', )
    
    def snippet(self):
        return self.description[:50]

    def get_absolute_url(self):
        return reverse('packages:package_detail',  kwargs={"id":self.id, "slug":self.slug})



class Itinerary(models.Model):
    package = models.OneToOneField(Package,on_delete=models.CASCADE,default=1)
    itinerary_name = models.CharField(max_length=200,default="NULL")

    def __str__(self):
        return f'{self.itinerary_name}'

class ItineraryDescription(models.Model):
    itinerary = models.ForeignKey(Itinerary,on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField()
    itinerary_description = models.TextField()
    
    class Meta:
        ordering = ['day_number']

    
    def __str__(self):
        return f'{self.itinerary.itinerary_name} | Day {self.day_number}'


        from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from adminside.models import *
from users.models import *
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# Create your views here.

from tours_travels import mail as mail_f
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError 
from .utils import generate_token
from django.views import View



def register(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		
		if form.is_valid():
			form.save()
			user=form.save(commit=False)
			user.is_active=False 
			user.save()
			# print(user.pk)
			current_site=get_current_site(request)
			# message =render_to_string(
			
			# )
			uid64=urlsafe_base64_encode(force_bytes(user.pk))
			token=generate_token.make_token(user)
			m=f'http://{current_site}/users/activate/{uid64}/{token}'
			mail_f.verification_mail(m,user)
			# print(current_site,current_site.domain,uid64,token)
			# print(user.pk,m)
			# print(form.cleaned_data.get('email'))
			# username=form.cleaned_data.get('')
			# messages.success(request,f'{username} your account is created!!')
			return redirect('login')

		return render(request,'users/register.html',{'form':form})

	else:
		form=UserRegisterForm()
		return render(request,'users/register.html',{'form':form})
		
		
def home(request):
	dests=Destination.objects.all()[:4]
	packs=Package.objects.all().order_by('number_of_times_booked')[:3]
	nights=[]
	price=[]
	travel=[]
	dtn_image=[]
	dtn_image_url_list=[]
	for dest in dests:
		dest_obj = dest.destinationimages_set.all()[0] #destination images object
		img = dtn_image.append(dest_obj.small_image.url)
		
	destinations=zip(dests,dtn_image)

	for i in packs:
		nights.append(i.number_of_days-1)
		price.append(i.adult_price+i.accomodation.price_per_room)
		mode=i.travel.travelling_mode
		if(mode=="TN"):
			travel.append("Train")
		elif(mode=="FT"):
			travel.append("Flight")
		else:
			travel.append("Bus")
		
		destination_img_object = i.destination.destinationimages_set.all()[0] #destination images object
		img = dtn_image_url_list.append(destination_img_object.caraousel1.url)
	
	packages=zip(packs,nights,price,travel,dtn_image_url_list)
	

	context={'dests':destinations,'packages':packages}
	
	return render(request,'users/index.html',context)

def destination(request,id):
	id=id
	dest=Destination.objects.get(id=id)
	packs=dest.package_set.all()
	nights=[]
	price=[]
	dtn_image_url_list = []
	travel=[]
	
	for i in packs:
		nights.append(i.number_of_days-1)
		price.append(i.adult_price+i.accomodation.price_per_room)
		mode=i.travel.travelling_mode
		if(mode=="TN"):
			travel.append("Train")
		elif(mode=="FT"):
			travel.append("Flight")
		else:
			travel.append("Bus")


		# Getting the small image of a particular package related to some destination
		destination_img_object = i.destination.destinationimages_set.all()[0] #destination images object
		img = dtn_image_url_list.append(destination_img_object.small_image.url)
	
	
	packages=zip(packs,nights,price,travel,dtn_image_url_list)


	# Images For caraousel purpose
	images = dest.destinationimages_set.all()[0] #destination images object
	caraousel1 = images.caraousel1.url
	caraousel2 = images.caraousel2.url
	caraousel3 = images.caraousel3.url



	context={'dest':dest,'packages':packages,'caraousel1':caraousel1,'caraousel2':caraousel2,'caraousel3':caraousel3}
	
	return render(request,'users/destination.html',context)

def search(request):
	try:
		name=request.POST.get('search','')
		name=name.lstrip()
		name=name.rstrip()
		dest=Destination.objects.filter(city__icontains=name) | Destination.objects.filter(state__icontains=name) | Destination.objects.filter(city__icontains=name)	
		print(dest[0].id)
		return redirect('users-destination', id=dest[0].id)
	except:
		messages.error(request, 'No results found for your search request')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		
def advert_detail(request, id, slug):
    advert = get_object_or_404(Advert, id=id , slug=slug, available=True)
    return render( request, 'listings/advertdetail.html', context = {
        'advert': advert,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    }
      )

def detail_package(request,package_id):
	if request.user.is_authenticated:
		try:
			package = get_object_or_404(Advert, id=id , slug=slug, available=True)


			context = {
					'package':package,
				}

		except:
			return HttpResponse('<H1> An error ocuured in Database , Please try later </H1>')


		return render(request,'users/package_detail.html',context)
	else:
		return redirect('login')


def bookings(request):
	user_id=request.user.id
	context = {}
	if request.method == 'POST':
		user=user_id
		package=request.POST['package_id']
		package=Package.objects.get(pk=package)
		number_of_adults = request.POST['adults']
		number_of_children =request.POST['children']
		number_of_rooms =request.POST['rooms']
		booking_date=request.POST['date']
		include_travelling=request.POST.get('travel')
		if include_travelling:
			include_travelling=True
			total_amount=(package.adult_price * int(number_of_adults)) + (package.child_price * int(number_of_children)) + (package.travel.price_per_person *(int(number_of_adults)+int(number_of_children)))+(package.accomodation.price_per_room*int(number_of_rooms))
			print(total_amount)
		else:
			include_travelling=False
			total_amount=(package.adult_price * int(number_of_adults)) + (package.child_price * int(number_of_children)) + (package.accomodation.price_per_room*int(number_of_rooms))
			print(total_amount)
		bookings=UserBookings(user=request.user,package=package,number_of_adults=number_of_adults,number_of_children=number_of_children,number_of_rooms=number_of_rooms,booking_date=booking_date,include_travelling=include_travelling,paid=False,total_amount=total_amount)
		bookings.save()
		
		return redirect('users-home')
		
	else:
		return redirect('users-home')




# @login_required(login_url='/accounts/login/')
def package_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    packages = Package.objects.filter(available=True)
    paginator = Paginator(packages, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        packages = Package.objects.filter(category=category)
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
        

    return render(request, 'users/package.html',   context = {
        'category': category,
        'categories': categories,
        'packages' : packages,
        'page': page, 
        'next_page_url' : next_url,
        'prev_page_url': prev_url,
        'tab': 'listings',
    })



class ActivateAccountView(View):
	def get(self,request,uid64,token):
		try:
			uid = urlsafe_base64_decode(uid64).decode('utf-8')
			user=User.objects.get(pk=uid)
			print(uid)
		except Exception as identifire :
			user=None

		if user is not None and generate_token.check_token(user,token):
			user.is_active=True 
			user.save()
			messages.success(request, 'account activated successfully')

			return redirect('login')
		return HttpResponse('not working')





