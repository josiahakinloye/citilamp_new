from django.db import models


class CountryAndCityInfo(models.Model):
    """
    This is the base class for info shared by countries and cities like
    Politics,Sleep,etiquette etc.
    """
    travel_choices = (
        ('Air', 'By Air'),
        ('Plane', 'By Plane'),
        ('Bus', 'By Boat '),
        ('Train', 'By Train')
    )
    entry_requirement = models.CharField(max_length=250, choices=travel_choices,blank=True)
    history = models.TextField(blank=True)
    pre_colonial_era = models.TextField(blank=True)
    colonial_era = models.TextField(blank=True)
    post_independence= models.TextField(blank=True)
    terrain = models.TextField(blank=True)
    region = models.TextField(blank=True)
    talks_and_language = models.TextField(blank=True)
    politics_ruler_government = models.TextField(blank=True)
    contact = models.TextField(blank=True)
    respects = models.TextField(blank=True)
    stay_healthy = models.TextField(blank=True)
    lgbt = models.TextField(blank=True)
    stay_safe = models.TextField(blank=True)
    work = models.TextField(blank=True)
    education = models.TextField(blank=True)
    sleep = models.TextField(blank=True)
    drinks_eat = models.TextField(blank=True)
    bargaining = models.TextField(blank=True)
    buys = models.TextField(blank=True)
    holiday = models.TextField(blank=True)
    electricity = models.TextField(blank=True)
    law_bureaucracy = models.TextField(blank=True)
    etiquettes = models.TextField(blank=True)
    exchange  = models.TextField(blank=True)
    cost = models.TextField(blank=True)
    tipping = models.TextField(blank=True)
    culture = models.TextField(blank=True)
    measurement = models.TextField(blank=True)
    planning_preArrival_documentation_visaProcessing = models.TextField(blank=True)
    corruption_crime = models.TextField(blank=True)
    homosexuals_lesbian = models.TextField(blank=True)
    drug = models.TextField(blank=True)
    racism = models.TextField(blank=True)
    curfew = models.TextField(blank=True)
    animal_hunting = models.TextField(blank=True)
    prostitute = models.TextField(blank=True)
    fun_games_relaxation = models.TextField(blank=True)
    excursion = models.TextField(blank=True)

    class Meta:
        abstract = True


class Continent(models.Model):
    name = models.CharField(max_length=200, unique=True)
    map = models.ImageField(upload_to='pictures/continent', width_field="width_field",
                                height_field="height_field", blank=True)
    height_field = models.IntegerField(default=200, blank=True)
    width_field = models.IntegerField(default=319, blank=True)
    history = models.TextField(blank=True)
    geo_loc = models.TextField(blank=True)
    region = models.CharField(max_length=200, blank=True)
    climate = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Continents"

class Country(CountryAndCityInfo):
    name = models.CharField(max_length=250, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, blank=True, null=True)
    iso_alpha_2_code = models.CharField(max_length=2, null=True, blank=True, default=None, unique=True)
    iso_alpha_3_code = models.CharField(max_length=3, null=True, blank=True, default=None, unique=True)
    map = models.ImageField(upload_to='pictures/country', width_field="width_field",
                            height_field="height_field", blank=True)
    height_field = models.IntegerField(default=200, blank=True)
    width_field = models.IntegerField(default=319, blank=True)
    currency_code = models.CharField(max_length=3, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

class StateProvince(models.Model):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    map = models.ImageField(upload_to='pictures/state', width_field="width_field",
                            height_field="height_field", blank=True)
    height_field = models.IntegerField(default=200, blank=True)
    width_field = models.IntegerField(default=319, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "States And Provinces"

class City(CountryAndCityInfo):
    name = models.CharField(max_length=250)
    stateprovince = models.ForeignKey(StateProvince, on_delete=models.CASCADE, null=True, blank=True, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, default=None)
    map = models.ImageField(upload_to='pictures/city', width_field="width_field",
                                       height_field="height_field", blank=True)
    height_field = models.IntegerField(default=200, blank=True)
    width_field = models.IntegerField(default=319, blank=True)
    best_city = models.BooleanField(default=False)
    latitude = models.TextField(null=True, blank=True, default=None)
    longitude = models.TextField(null=True, blank=True, default=None)
    def __str__(self):
        return self.name + " - " + self.country.iso_alpha_3_code

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Cities"

class CountryAndCityAttractions(models.Model):
    """
    Base class for attractions like zoos, restaurants, hotels etc of countries and cities
    """
    name = models.CharField(max_length=450,)
    city= models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True,null=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    # what can be done in this place
    details = models.TextField(blank=True)
    height_field = models.IntegerField(default=200, blank=True)
    width_field = models.IntegerField(default=319, blank=True)

    # check that the attraction was tied to a city or a country not both, if not do not save
    def save(self, *args, **kwargs):
        if self.city  or  self.country:
            if self.city and self.country:
                raise Exception("Attraction can only be tied to city or country not both")
            else:
                super(CountryAndCityAttractions, self).save(*args, **kwargs)
        else:
            raise Exception("Attraction must be linked to a country or a city")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]

class Park(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/parks', width_field="width_field",
                                      height_field="height_field", blank=True)
class TouristCenter(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/tourist_centers', width_field="width_field",
                            height_field="height_field", blank=True)
class Beach(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/beaches', width_field="width_field",
                            height_field="height_field", blank=True)

    class Meta:
        verbose_name_plural = "Beaches"


class Museum(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/museums', width_field="width_field",
                            height_field="height_field", blank=True)


class Gallery(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/galleries', width_field="width_field",
                            height_field="height_field", blank=True)

    class Meta:
        verbose_name_plural = "Galleries"


class MarketTradingcenterSHOP(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/markets', width_field="width_field",
                            height_field="height_field", blank=True)
    class Meta:
        verbose_name_plural = "Markets, Trading centers and Shops "


class HistoricalAttraction(CountryAndCityAttractions):
    map = models.ImageField(upload_to='pictures/historical_attractions', width_field="width_field",
                            height_field="height_field", blank=True)

class PartnerTag(models.Model):
    """
    A database of partner tags like hotels, restaurants.
    To help know what type of business partners are into.
    """
    name = models.CharField(primary_key=True, max_length=40,  verbose_name="Name of tag")
    description = models.TextField(verbose_name="Description of tag")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Partner Tags"


class Partner(models.Model):
    name = models.TextField(verbose_name="Partner's business name")
    tag = models.ForeignKey(PartnerTag, on_delete=models.CASCADE, verbose_name="The partner's tag.")
    website = models.URLField(blank=True, null=True, verbose_name="The partner's websites url.")
    description = models.TextField(verbose_name="More specific details on what the partner does.")
    address = models.TextField(verbose_name="Business address of partner.")
    areas_of_operation= models.TextField(verbose_name="Areas partner operates in or out of.")

    def __str__(self):
        return self.name + " with tag " + self.tag.name

    class Meta:
        ordering = ['name', 'tag']
        verbose_name_plural = "Partners"


class Contacts(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contacts"


class GalleryPhoto(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField()
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.city.name + ", " + self.country.name
