from django.db import models


# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name
    
class Product(models.Model):
    MIXMAS = 'Mixing and Mastering Package'
    MASO = 'Mastering Only'
    FEAT = 'Request a Feature'
    TUT = 'Request a Tutor'
    NONE = 'Select an option'
    PRODUCT_NAME_CHOICES = [
        (MIXMAS, 'Mixing and Mastering Package'),
        (MASO, 'Mastering Only'),
        (FEAT, 'Request a Feature'),
        (TUT, 'Request a Tutor'),
        (NONE, 'Select an option')
    ]
    name = models.CharField(max_length=100, choices=PRODUCT_NAME_CHOICES, default=NONE)
    stripe_product_id = models.CharField(max_length=100)
    product_description = models.CharField(max_length=300, null=True)
    
    
    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # dollars
    price_description = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ['price']
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price)

    def __str__(self):
        return '%s %s %s %s' % ("$", self.price, "-", self.price_description)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Package Type: ')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, verbose_name="Number of stems: ")
    cust_requests = models.TextField(max_length=500, null=True, verbose_name='Enter any specific requests here: (Leave blank if none): ')
    reference_track = models.CharField(max_length=200, null=True, verbose_name='Reference Track (Leave blank if none): ')
    music_file = models.FileField(upload_to='studio_orders/', verbose_name="Upload zipped music file: ")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cust_details')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default= False)
    customer_paid = models.FloatField(default= 0)
    stripe_order_id = models.CharField(max_length=100, null=True)
    fullfilment_date = models.DateTimeField(null=True)

    def __str__(self):
        return '%s %s %s' % (self.customer, "-", self.order_date)

class FrequentlyAsked(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=1000)

    class Meta:
        verbose_name= 'Frequently Asked Question'

    def __str__(self):
        return self.question

class SampleSong(models.Model):
    before_mix = models.FileField(upload_to='studio_samples/')
    after_mix = models.FileField(upload_to='studio_samples/')
    song_name = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        ordering = ['song_artist']

    def __str__(self):
        return self.song_name