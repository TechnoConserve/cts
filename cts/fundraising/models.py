import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import crypto, timezone
from django.urls import reverse
from sorl.thumbnail import ImageField, get_thumbnail

from accounts.models import Profile

GOAL_AMOUNT = Decimal("1000.00")
DISPLAY_DONOR_DAYS = 365
DEFAULT_DONATION_AMOUNT = 10
LEADERSHIP_LEVEL_AMOUNT = Decimal("1000.00")
INTERVAL_CHOICES = (
    ('monthly', 'Monthly donation'),
    ('quarterly', 'Quarterly donation'),
    ('yearly', 'Yearly donation'),
    ('onetime', 'One-time donation'),
)


class CTSDonorManager(models.Manager):
    def for_public_display(self):
        donors = self.get_queryset().filter(
            is_visible=True,
            approved=True,
            donation__payment__date__gt=datetime.date.today() - datetime.timedelta(days=DISPLAY_DONOR_DAYS),
        ).annotate(donated_amount=models.Sum('donation__payment__amount'))
        return donors.order_by('-donated_amount', 'name')


class FundraisingModel(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        if not self.id:
            self.id = crypto.get_random_string(length=12)
        return super().save(*args, **kwargs)


class CTSDonor(FundraisingModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    logo = ImageField(upload_to="fundraising/logos/", blank=True)
    url = models.URLField(blank=True, verbose_name='URL')
    name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    DONOR_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    )
    donor_type = models.CharField(max_length=30, choices=DONOR_TYPE_CHOICES, blank=True)
    is_visible = models.BooleanField(
        default=False,
        verbose_name="Agreed to displaying on the fundraising page?",
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name="Agreed to being contacted by CTS?",
    )
    approved = models.NullBooleanField(
        verbose_name="Name, URL, and Logo approved?",
    )

    objects = CTSDonorManager()

    def __str__(self):
        return self.name if self.name else 'Anonymous #{}'.format(self.pk)

    class Meta:
        verbose_name = "CTS donor"
        verbose_name_plural = "CTS donors"

    @property
    def display_name(self):
        return self.name

    @property
    def thumbnail(self):
        return get_thumbnail(self.logo, '170x170', quality=100) if self.logo else None

    @property
    def name_with_fallback(self):
        return self.name if self.name else 'Anonymous Donor'


class Donation(FundraisingModel):
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES, blank=True)
    subscription_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    donor = models.ForeignKey(CTSDonor, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    receipt_email = models.EmailField(blank=True)

    def __str__(self):
        return '{} from {}'.format(self.get_interval_display(), self.donor)

    def get_absolute_url(self):
        return reverse('fundraising:thank-you', kwargs={'donation': self.id})

    def is_active(self):
        return bool(self.stripe_subscription_id)
    is_active.boolean = True

    def total_payments(self):
        return self.payment_set.aggregate(models.Sum('amount'))['amount__sum']


class Payment(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    stripe_charge_id = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '${}'.format(self.amount)


class Testimonial(models.Model):
    author = models.CharField(max_length=255)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.author


class InKindDonor(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, verbose_name='URL')
    description = models.TextField()
    logo = ImageField(upload_to='fundraising/logos/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'in-kind donor'
        verbose_name_plural = 'in-kind donors'

    @property
    def display_name(self):
        return self.name

    @property
    def thumbnail(self):
        return get_thumbnail(self.logo, '170x170', quality=100) if self.logo else None


@receiver(post_save, sender=CTSDonor)
@receiver(post_save, sender=InKindDonor)
def create_thumbnail_on_save(sender, **kwargs):
    return kwargs['instance'].thumbnail
