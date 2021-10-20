from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from .models import Person, Transaction
from .service import TransactionService, FriendService, PersonService
from .util import myconverter, ExtendedEncoder
# TODO Handle exception handling


def register(request):
    data = json.loads(request.body.decode('utf-8'))
    p = PersonService.save(data)
    return HttpResponse(json.dumps(p, cls=ExtendedEncoder),status=201)


def expense(request, user_id):
    '''
    :param request:
        amount - amount added
        currency - currency of the transaction
        lender_id - user who lent the money
        borrow_ids - user/users who borrowed money
        ptype -
            1 - equal weightage
            2 - percentage weightage
        share_ratio - if ptype = 2 , share_ratio represents an array of borrowers ratio
    :param user_id: This is the user adding the transaction
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    amount = data['amount']
    #TODO handle currency other than default
    #currency = data['currency']
    user = get_object_or_404(Person, id=user_id)
    lender = get_object_or_404(Person, id=data['lender_id'])
    borrowers = [get_object_or_404(Person, id=user) for user in data['borrow_ids']]
    #TODO create schema for share type
    ptype = data['ptype']
    #TODO move this into ptype schema
    share = data.get('share_ratio')
    TransactionService(user, lender, borrowers, amount, ptype, share=share).save()
    return HttpResponse(status=201)


def friends(request, user_id):
    data = FriendService(user_id).fetch()
    return HttpResponse(json.dumps(data), content_type="application/json")


def logs(request, user_id):
    row = TransactionService.logs(user_id)
    return HttpResponse(json.dumps(row, default=myconverter), content_type="application/json")


def settle(request, user_id):
    data = json.loads(request.body.decode('utf-8'))
    friend_id = data['friend_id']
    settle_amount = data['amount']
    user = get_object_or_404(Person, id=user_id)
    friend = get_object_or_404(Person, id=friend_id)
    TransactionService.settle(user, friend, settle_amount)
    return HttpResponse(status=201)
