from .models import Transaction
from django.shortcuts import get_object_or_404
from .models import Person
from .schema import FriendSchema
from django.db import connection

class ExpenseTracker:
    def __init__(self, paid, share):
        self.paid = paid
        self.share = share

class PersonService:
    @staticmethod
    def save(data):
        p = Person(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data['email']
        )
        p.save()
        return p

class TransactionService:
    def __init__(self,user, lender, borrowers, amount, ptype, share=[]):
        self.user = user
        self.creator = user
        self.lender = lender
        self.borrowers = borrowers
        self.borrowers_map = {borrower.id:borrower for borrower in borrowers}
        self.amount = amount
        self.ptype = ptype
        self.share = share


    def __createSharedExpenses(self):
        expense_data = {}
        #expense_data[self.lender.id] = ExpenseTracker(self.amount, 0)
        for user in self.borrowers_map:
            expense_data[user] = ExpenseTracker(0, 0)
        return expense_data

    def __getsharedExpenses(self):
        expense_data = self.__createSharedExpenses()
        if self.ptype == 1:
            # equal
            share = self.amount / len(expense_data)
            for u in expense_data:
                expense_data[u].share = share
        elif self.ptype == 2:
            # percent
            count = 0
            for ratio in self.share:
                user = self.borrowers[count]
                expense_data[user.id].share = ratio * self.amount
                count += 1
        return expense_data

    def save(self):
        expense_data = self.__getsharedExpenses()
        for exp in expense_data:
            print('Saving',exp,self.borrowers_map,expense_data)
            Transaction(
                lender=self.lender,
                borrower=self.borrowers_map[exp],
                amount=expense_data[exp].share,
                user=self.user
            ).save()

    @staticmethod
    def settle(user, friend, settle_amount):
        if settle_amount > 0:
            # user is getting money back
            lender = friend
            borrow = user
        else:
            lender = user
            borrow = friend

        Transaction(
            lender=lender,
            borrower=borrow,
            amount=settle_amount,
            user=user
        ).save()

    @staticmethod
    def logs(user_id):
        QUERY = '''
            select created_at,sum(amount) from person_transaction where user_id = %s group by created_at;
        '''
        cursor = connection.cursor()
        cursor.execute(QUERY, [user_id])
        row = cursor.fetchall()
        return row

class FriendService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.lends = Transaction.objects.filter(lender_id=user_id)
        self.owes = Transaction.objects.filter(borrower_id=user_id)

    def __fetchAllExpenses(self):
        expense_data = {}
        # TODO Handle currency
        for transaction in self.lends:
            friend_id = transaction.borrower_id
            if friend_id not in expense_data:
                expense_data[friend_id] = 1 * transaction.amount
            else:
                expense_data[friend_id] += 1 * transaction.amount
        for transaction in self.owes:
            friend_id = transaction.lender_id
            if friend_id not in expense_data:
                expense_data[friend_id] = -1 * transaction.amount
            else:
                expense_data[friend_id] += -1 * transaction.amount
        return expense_data

    def fetch(self):
        expense_data = self.__fetchAllExpenses()
        friends = []
        for friend_id in expense_data:
            friend = FriendSchema(get_object_or_404(Person, id=friend_id))
            friend.amount = expense_data[friend_id]
            friends.append(friend.toJSON())
        return friends




