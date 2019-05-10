from django.shortcuts import render, redirect, get_object_or_404
from Apartments.forms.apartments_form import ApartmentsCreateForm, LocationCreateForm
from Apartments.models import ApartmentImage, Apartments
from django.http import JsonResponse
from Apartments.forms.change_price_form import ChangePriceForm


def index(request):
    context = {'apartments': Apartments.objects.all()}
    return render(request, 'apartments/index.html', context)


def all_listing(request):
    # get the Json if they are searcing by price
    if 'arrange_by_price' in request.GET:
        apartments = [{
            'id': x.id,
            'price': x.price,
            'size': x.size,
            'locationID': x.locationID.id,
            'rooms': x.rooms,
            'privateEntrance': x.privateEntrance,
            'animalsAllowed': x.animalsAllowed,
            'garage': x.garage,
            'yearBuild': x.yearBuild,
            'description': x.description,
            'sellerID': x.sellerID.id,
            'firstImage': x.apartmentimage_set.first().image,
        } for x in Apartments.objects.all().order_by('-price')]
        return JsonResponse({'data': apartments})
    #get the Json if they are searching for a name
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        apartments = [{
            'id': x.id,
            'price': x.price,
            'size': x.size,
            'locationID': x.locationID.id,
            'rooms': x.rooms,
            'privateEntrance': x.privateEntrance,
            'animalsAllowed': x.animalsAllowed,
            'garage': x.garage,
            'yearBuild': x.yearBuild,
            'description': x.description,
            'sellerID': x.sellerID.id,
            'firstImage': x.apartmentimage_set.first().image,
        } for x in Apartments.objects.filter(locationID__streetName__icontains=search_filter)]
        return JsonResponse({'data': apartments})
    context = {'apartments': Apartments.objects.all()}
    return render(request, 'apartments/all_listing.html', context)


def all_listing_by_price(request):
    context = {'apartments': Apartments.objects.all().order_by('-price')}
    return render(request, 'apartments/all_listing.html', context)


def all_listing_by_name(request):
    context = {'apartments': Apartments.objects.all().order_by('locationID__streetName')}
    return render(request, 'apartments/all_listing.html', context)


def get_apartment_by_id(request, id):
    return render(request, 'apartments/single_apartment.html', {
        'apartments': get_object_or_404(Apartments, pk=id)
    })


def create_apartment(request):
    if request.method == 'POST':
        apartment_form = ApartmentsCreateForm(data=request.POST)
        location_form = LocationCreateForm(data=request.POST)
        if all([apartment_form.is_valid(), location_form.is_valid()]):
            location = location_form.save()
            apartment = apartment_form.save(commit=False)
            apartment.locationID = location
            location.save()
            apartment.save()
            apartment_image = ApartmentImage(image=request.POST['image'], apartmentID=apartment)
            apartment_image.save()
            return redirect('apartment-index')
    else:
        apartment_form = ApartmentsCreateForm()
        location_form = LocationCreateForm()
    return render(request, 'apartments/create_apartment.html', {
        'apartment_form': apartment_form,
        'location_form': location_form,
    })


def delete_apartment(request, id):
    apartment = get_object_or_404(Apartments, pk=id)
    apartment.delete()
    return redirect('apartment-index')

def change_price(request, id):
    if request.method == 'POST':
        price_form = ChangePriceForm(data=request.POST)
        if price_form.is_valid():
            apartment = get_object_or_404(Apartments, pk=id)
            apartment.price = request.POST['price']
            apartment.save()
        return redirect('apartment-index')
    context = {
        'form': ChangePriceForm,
        'id': id
    }
    return render(request, 'apartments/change_price.html', context)