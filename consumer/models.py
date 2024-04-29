from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    transactions_sent = models.ManyToManyField('Transaction', related_name='sender')
    transactions_received = models.ManyToManyField('Transaction', related_name='receiver')

    def __str__(self):
        return str(self.user) + " - Balance: $" + str(round(self.balance, 2))

class Currency(models.Model):
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.code + ' ('+self.symbol+')'
        
# Create a new transaction and add it to the user's balance
def createTransaction(sender, amount, receiver, type, description):
    transaction = Transaction(user=receiver, amount=amount, type=type, description=description)
    if sender != None: # If there is a sender (i.e., this isn't a deposit)
        sender.transactions_sent.add(transaction)
        receiver.transactions_recv.add(transaction)
    else:
        receiver.transactions_recv.add(transaction)
    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10) # Deposit or Withdrawal
    description = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1) # Default to USD
    
    @property
    def net_value(self):
        return self.amount / float(self.currency.exchange_rate)

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
        # Update the User's balance when the transaction is saved
        createTransaction(None, self.net_value, self.user, self.type, self.description)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Transactions"
        verbose_name = "Transaction"
        get_latest_by = 'date'
        unique_together = ('user', 'date')
        index_together = (('user', 'date'),)
        indexes = (
            models.Index(fields=['user', 'date']),
        )

