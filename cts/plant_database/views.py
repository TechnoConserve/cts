from django.contrib import messages
from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect

from .forms import AccessionForm
from .models import Accession, Collector, CommonName, Site, Species, Variety


def add_accession(request):
    if request.method == 'POST':
        form = AccessionForm(request.POST)

        if form.is_valid():
            collectors = []
            num_collectors = form.cleaned_data['add_collector_count']
            col_fname = form.cleaned_data['col_fname']
            col_lname = form.cleaned_data['col_lname']
            collector, created = Collector.objects.get_or_create(first_name=col_fname, last_name=col_lname)

            collectors.append(collector)
            if int(num_collectors) > 1:
                for num in range(1, num_collectors):
                    fn = form.cleaned_data['col_fname_' + str(num_collectors)]
                    ln = form.cleaned_data['col_lname_' + str(num_collectors)]
                    collector, created = Collector.objects.get_or_create(first_name=fn, last_name=ln)
                    collectors.append(collector)

            common_name_data = form.cleaned_data['common_name']
            common_name, created = CommonName.objects.get_or_create(name=common_name_data)

            family = form.cleaned_data['family']
            genus = form.cleaned_data['genus']
            species_data = form.cleaned_data['species']
            species, created = Species.objects.get_or_create(genus=genus, name=species_data,
                                                             defaults={'common_name': common_name})
            if not created and common_name not in list(species.common_name.all()):
                species.common_name.add(common_name)

            variety_data = form.cleaned_data['variety']
            variety, created = Variety.objects.get_or_create(species=species, name=variety_data)

            country = form.cleaned_data['country']
            maj_country = form.cleaned_data['maj_country']
            min_country = form.cleaned_data['min_country']
            locality = form.cleaned_data['locality']
            site, created = Site.objects.get_or_create(country=country, major_country_area=maj_country,
                                                       minor_country_area=min_country, locality=locality)

            plant_total = form.cleaned_data['plant_total']
            sample_size = form.cleaned_data['sample_size']
            percent_sampled = form.cleaned_data['percent_sampled']
            percent_flowering = form.cleaned_data['percent_flowering']
            percent_fruiting = form.cleaned_data['percent_fruiting']
            storage_location = form.cleaned_data['storage_location']

            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            point = Point(latitude, longitude)

            altitude = form.cleaned_data['altitude']
            bank_date = form.cleaned_data['bank_date']

            accession = Accession(family=family,
                                  genus=genus,
                                  species=species,
                                  variety=variety,
                                  site=site,
                                  plant_total=plant_total,
                                  sample_size=sample_size,
                                  percent_sampled=percent_sampled,
                                  percent_flowering=percent_flowering,
                                  percent_fruiting=percent_fruiting,
                                  storage_location=storage_location,
                                  location=point,
                                  altitude=altitude,
                                  bank_date=bank_date)
            accession.save()
            accession.collectors.set(collectors)

            messages.add_message(request, messages.SUCCESS, "Accession added to database!")
            return redirect('plant_database:index')
    else:
        form = AccessionForm()

    return render(request, "plant_database/accession.html", {'form': form})


def index(request):
    accessions = Accession.objects.all()
    return render(request, 'plant_database/index.html', {'accessions': accessions})