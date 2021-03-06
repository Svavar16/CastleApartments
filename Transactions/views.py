from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from Apartments.models import Apartments
from django.contrib.auth.models import User
from User.models import CardDetails
from Transactions.models import Transactions
from django.contrib import auth
from User.forms.select_card import SelectCardForm

# Create your views here.

def make_transaction(request, apartment_id, payment_id):
    buyer = auth.get_user(request)
    apartment = get_object_or_404(Apartments, pk=apartment_id)
    seller = User.objects.get(pk=apartment.sellerID.id)
    credit_card = get_object_or_404(CardDetails, pk=payment_id)
    if credit_card.owner == buyer and buyer != seller and apartment.forSale:
        transaction = Transactions(buyer=buyer, seller=seller, payment=credit_card, apartment=apartment)
        transaction.save()
        apartment.sellerID = buyer
        apartment.forSale = False
        apartment.save()
        return render(request, 'Transactions/make_transaction.html', {
            'buyer': buyer,
            'apartment': apartment,
            'seller': seller,
            'credit_card': credit_card.cardNumber[-4:],
        })
    return render(request, 'apartments/index.html')


def review(request, apartment_id, payment_id=None):
    if payment_id == None:
        payment_id=request.POST['CardSelect']

    buyer = auth.get_user(request)
    apartment = get_object_or_404(Apartments, pk=apartment_id)
    credit_card = get_object_or_404(CardDetails, pk=payment_id)
    if apartment.forSale:
        return render(request, 'Transactions/review.html', {
            'buyer': buyer,
            'apartment': apartment,
            'payment': credit_card,
            'credit_card': credit_card.cardNumber[-4:],
        })
    return render(request, 'apartments/index.html')


@permission_required('Transactions.can_view_transactions')
def list_transactions(request):
    transactions = Transactions.objects.all()
    return render(request, 'Transactions/archive.html', {
        'transactions': transactions
    })


def transaction_details(request, id):
    user = request.user
    transaction = get_object_or_404(Transactions, pk=id)
    if user.has_perm('Transactions.can_view_transactions') or user == transaction.buyer or user == transaction.seller:
        return render(request, 'Transactions/single_transaction.html', {
            'transaction': transaction,
            'card_number': transaction.payment.cardNumber[-4:]
        })
    raise PermissionDenied


@login_required
def personal_transactions(request):
    user = request.user
    if user.has_perm('Transactions.can_view_transactions'):
        transactions = Transactions.objects.filter(Q(seller=user) | Q(buyer=user))
        return render(request, 'Transactions/archive.html', {
            'transactions': transactions,
        })
