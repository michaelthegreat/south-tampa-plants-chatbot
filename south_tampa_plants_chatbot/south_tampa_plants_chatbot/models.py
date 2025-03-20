from django.db import models

class Listing(models.Model):
    listingId = models.IntegerField(primary_key=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deleted = models.BooleanField()
    siteId = models.IntegerField()
    price = models.BigIntegerField()
    inStock = models.IntegerField(null=True, blank=True)
    createdOn = models.DateTimeField()
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    imageUrl = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'listing'  # or the actual tabl
