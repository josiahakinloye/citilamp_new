from django.core.management.base import BaseCommand

from citilamp.models import Continent, Country, City


class Command(BaseCommand):
    help = 'Initialize continents, countries, states and cities data'

    def handle(self, *args, **options):
        # Clear the current data to avoid duplicates
        Continent.objects.all().delete()
        Country.objects.all().delete()
        City.objects.all().delete()

        # add continents
        continents = [
            Continent(name='Africa'),
            Continent(name='Americas'),
            Continent(name='Antarctica'),
            Continent(name='Asia'),
            Continent(name='Europe'),
            Continent(name='Oceania')
        ]
        Continent.objects.bulk_create(continents)
        print(len(continents), "continents have been added")

        # add countries
        countries = []
        # Countries in Africa
        africa = Continent.objects.filter(name='Africa').first()
        countries += [
            Country(name=u"Algeria", continent=africa, iso_alpha_2_code='DZ', iso_alpha_3_code='DZA'),
            Country(name=u"Angola", continent=africa, iso_alpha_2_code='AO', iso_alpha_3_code='AGO'),
            Country(name=u"Benin", continent=africa, iso_alpha_2_code='BJ', iso_alpha_3_code='BEN'),
            Country(name=u"Botswana", continent=africa, iso_alpha_2_code='BW', iso_alpha_3_code='BWA'),
            Country(name=u"Burkina Faso", continent=africa, iso_alpha_2_code='BF', iso_alpha_3_code='BFA'),
            Country(name=u"Burundi", continent=africa, iso_alpha_2_code='BI', iso_alpha_3_code='BDI'),
            Country(name=u"Cameroon", continent=africa, iso_alpha_2_code='CM', iso_alpha_3_code='CMR'),
            Country(name=u"Cape Verde", continent=africa, iso_alpha_2_code='CV', iso_alpha_3_code='CPV'),
            Country(name=u"Central African Republic", continent=africa, iso_alpha_2_code='CF', iso_alpha_3_code='CAF'),
            Country(name=u"Chad", continent=africa, iso_alpha_2_code='TD', iso_alpha_3_code='TCD'),
            Country(name=u"Comoros", continent=africa, iso_alpha_2_code='KM', iso_alpha_3_code='COM'),
            Country(name=u"Republic of the Congo", continent=africa, iso_alpha_2_code='CG', iso_alpha_3_code='COG'),
            Country(name=u"Democratic Republic of the Congo", continent=africa, iso_alpha_2_code='CD', iso_alpha_3_code='COD'),
            Country(name=u"Côte d'Ivoire", continent=africa, iso_alpha_2_code='CI', iso_alpha_3_code='CIV'),
            Country(name=u"Djibouti", continent=africa, iso_alpha_2_code='DJ', iso_alpha_3_code='DJI'),
            Country(name=u"Egypt", continent=africa, iso_alpha_2_code='EG', iso_alpha_3_code='EGY'),
            Country(name=u"Equatorial Guinea", continent=africa, iso_alpha_2_code='GQ', iso_alpha_3_code='GNQ'),
            Country(name=u"Eritrea", continent=africa, iso_alpha_2_code='ER', iso_alpha_3_code='ERI'),
            Country(name=u"Ethiopia", continent=africa, iso_alpha_2_code='ET', iso_alpha_3_code='ETH'),
            Country(name=u"Gabon", continent=africa, iso_alpha_2_code='GA', iso_alpha_3_code='GAB'),
            Country(name=u"Gambia", continent=africa, iso_alpha_2_code='GM', iso_alpha_3_code='GMB'),
            Country(name=u"Ghana", continent=africa, iso_alpha_2_code='GH', iso_alpha_3_code='GHA'),
            Country(name=u"Guinea", continent=africa, iso_alpha_2_code='GN', iso_alpha_3_code='GIN'),
            Country(name=u"Guinea-Bissau", continent=africa, iso_alpha_2_code='GW', iso_alpha_3_code='GNB'),
            Country(name=u"Kenya", continent=africa, iso_alpha_2_code='KE', iso_alpha_3_code='KEN'),
            Country(name=u"Lesotho", continent=africa, iso_alpha_2_code='LS', iso_alpha_3_code='LSO'),
            Country(name=u"Liberia", continent=africa, iso_alpha_2_code='LR', iso_alpha_3_code='LBR'),
            Country(name=u"Libya", continent=africa, iso_alpha_2_code='LY', iso_alpha_3_code='LBY'),
            Country(name=u"Madagascar", continent=africa, iso_alpha_2_code='MG', iso_alpha_3_code='MDG'),
            Country(name=u"Malawi", continent=africa, iso_alpha_2_code='MW', iso_alpha_3_code='MWI'),
            Country(name=u"Mali", continent=africa, iso_alpha_2_code='ML', iso_alpha_3_code='MLI'),
            Country(name=u"Mauritania", continent=africa, iso_alpha_2_code='MR', iso_alpha_3_code='MRT'),
            Country(name=u"Mauritius", continent=africa, iso_alpha_2_code='MU', iso_alpha_3_code='MUS'),
            Country(name=u"Mayotte", continent=africa, iso_alpha_2_code='YT', iso_alpha_3_code='MYT'),
            Country(name=u"Morocco", continent=africa, iso_alpha_2_code='MA', iso_alpha_3_code='MAR'),
            Country(name=u"Mozambique", continent=africa, iso_alpha_2_code='MZ', iso_alpha_3_code='MOZ'),
            Country(name=u"Namibia", continent=africa, iso_alpha_2_code='NA', iso_alpha_3_code='NAM'),
            Country(name=u"Niger", continent=africa, iso_alpha_2_code='NE', iso_alpha_3_code='NER'),
            Country(name=u"Nigeria", continent=africa, iso_alpha_2_code='NG', iso_alpha_3_code='NGA'),
            Country(name=u"Reunion", continent=africa, iso_alpha_2_code='RE', iso_alpha_3_code='REU'),
            Country(name=u"Rwanda", continent=africa, iso_alpha_2_code='RW', iso_alpha_3_code='RWA'),
            Country(name=u"Saint Helena", continent=africa, iso_alpha_2_code='SH', iso_alpha_3_code='SHN'),
            Country(name=u"São Tomé and Príncipe", continent=africa, iso_alpha_2_code='ST', iso_alpha_3_code='STP'),
            Country(name=u"Senegal", continent=africa, iso_alpha_2_code='SN', iso_alpha_3_code='SEN'),
            Country(name=u"Seychelles", continent=africa, iso_alpha_2_code='SC', iso_alpha_3_code='SYC'),
            Country(name=u"Sierra Leone", continent=africa, iso_alpha_2_code='SL', iso_alpha_3_code='SLE'),
            Country(name=u"Somalia", continent=africa, iso_alpha_2_code='SO', iso_alpha_3_code='SOM'),
            Country(name=u"South Africa", continent=africa, iso_alpha_2_code='ZA', iso_alpha_3_code='ZAF'),
            Country(name=u"South Sudan", continent=africa, iso_alpha_2_code='SS', iso_alpha_3_code='SSD'),
            Country(name=u"Sudan", continent=africa, iso_alpha_2_code='SD', iso_alpha_3_code='SDN'),
            Country(name=u"Swaziland", continent=africa, iso_alpha_2_code='SZ', iso_alpha_3_code='SWZ'),
            Country(name=u"Tanzania", continent=africa, iso_alpha_2_code='TZ', iso_alpha_3_code='TZA'),
            Country(name=u"Togo", continent=africa, iso_alpha_2_code='TG', iso_alpha_3_code='TGO'),
            Country(name=u"Tunisia", continent=africa, iso_alpha_2_code='TN', iso_alpha_3_code='TUN'),
            Country(name=u"Uganda", continent=africa, iso_alpha_2_code='UG', iso_alpha_3_code='UGA'),
            Country(name=u"Western Sahara", continent=africa, iso_alpha_2_code='EH', iso_alpha_3_code='ESH'),
            Country(name=u"Zambia", continent=africa, iso_alpha_2_code='ZM', iso_alpha_3_code='ZMB'),
            Country(name=u"Zimbabwe", continent=africa, iso_alpha_2_code='ZW', iso_alpha_3_code='ZWE'),
        ]
        # Countries in Americas
        americas = Continent.objects.filter(name='Americas').first()
        countries += [
            Country(name=u'United States', continent=americas, iso_alpha_2_code='US',
                    iso_alpha_3_code='USA'),
            Country(name=u'Anguilla', continent=americas, iso_alpha_2_code='AI', iso_alpha_3_code='AIA'),
            Country(name=u'Antigua and Barbuda', continent=americas, iso_alpha_2_code='AG', iso_alpha_3_code='ATG'),
            Country(name=u'Aruba', continent=americas, iso_alpha_2_code='AW', iso_alpha_3_code='ABW'),
            Country(name=u'Bahamas', continent=americas, iso_alpha_2_code='BS', iso_alpha_3_code='BHS'),
            Country(name=u'Barbados', continent=americas, iso_alpha_2_code='BB', iso_alpha_3_code='BRB'),
            Country(name=u'Belize', continent=americas, iso_alpha_2_code='BZ', iso_alpha_3_code='BLZ'),
            Country(name=u'Bermuda', continent=americas, iso_alpha_2_code='BM', iso_alpha_3_code='BMU'),
            Country(name=u'British Virgin Islands', continent=americas, iso_alpha_2_code='VG', iso_alpha_3_code='VGB'),
            Country(name=u'Canada', continent=americas, iso_alpha_2_code='CA', iso_alpha_3_code='CAN'),
            Country(name=u'Cayman Islands', continent=americas, iso_alpha_2_code='KY', iso_alpha_3_code='CYM'),
            Country(name=u'Costa Rica', continent=americas, iso_alpha_2_code='CR', iso_alpha_3_code='CRI'),
            Country(name=u'Cuba', continent=americas, iso_alpha_2_code='CU', iso_alpha_3_code='CUB'),
            Country(name=u'Dominica', continent=americas, iso_alpha_2_code='DM', iso_alpha_3_code='DMA'),
            Country(name=u'Dominican Republic', continent=americas, iso_alpha_2_code='DO', iso_alpha_3_code='DOM'),
            Country(name=u'El Salvador', continent=americas, iso_alpha_2_code='SV', iso_alpha_3_code='SLV'),
            Country(name=u'Greenland', continent=americas, iso_alpha_2_code='GL', iso_alpha_3_code='GRL'),
            Country(name=u'Grenada', continent=americas, iso_alpha_2_code='GD', iso_alpha_3_code='GRD'),
            Country(name=u"Guadeloupe", continent=americas, iso_alpha_2_code='GP', iso_alpha_3_code='GLP'),
            Country(name=u'Guatemala', continent=americas, iso_alpha_2_code='GT', iso_alpha_3_code='GTM'),
            Country(name=u'Haiti', continent=americas, iso_alpha_2_code='HT', iso_alpha_3_code='HTI'),
            Country(name=u'Honduras', continent=americas, iso_alpha_2_code='HN', iso_alpha_3_code='HND'),
            Country(name=u'Jamaica', continent=americas, iso_alpha_2_code='JM', iso_alpha_3_code='JAM'),
            Country(name=u'Mexico', continent=americas, iso_alpha_2_code='MX', iso_alpha_3_code='MEX'),
            Country(name=u'Martinique', continent=americas, iso_alpha_2_code='MQ', iso_alpha_3_code='MTQ'),
            Country(name=u'Netherlands Antilles', continent=americas, iso_alpha_2_code='AN', iso_alpha_3_code='ANT'),
            Country(name=u'Nicaragua', continent=americas, iso_alpha_2_code='NI', iso_alpha_3_code='NIC'),
            Country(name=u'Panama', continent=americas, iso_alpha_2_code='PA', iso_alpha_3_code='PAN'),
            Country(name=u'Puerto Rico', continent=americas, iso_alpha_2_code='PR', iso_alpha_3_code='PRI'),
            Country(name=u'Saint Kitts and Nevis', continent=americas, iso_alpha_2_code='KN', iso_alpha_3_code='KNA'),
            Country(name=u'Saint Lucia', continent=americas, iso_alpha_2_code='LC', iso_alpha_3_code='LCA'),
            Country(name=u'Saint Pierre and Miquelon', continent=americas, iso_alpha_2_code='PM', iso_alpha_3_code='SPM'),
            Country(name=u'Saint Vincent and Grenadines', continent=americas, iso_alpha_2_code='VC',
                    iso_alpha_3_code='VCT'),
            Country(name=u'Trinidad and Tobago', continent=americas, iso_alpha_2_code='TT', iso_alpha_3_code='TTO'),
            Country(name=u'Turks and Caicos', continent=americas, iso_alpha_2_code='TC', iso_alpha_3_code='TCA'),
            Country(name=u'Argentina', continent=americas, iso_alpha_2_code='AR', iso_alpha_3_code='ARG'),
            Country(name=u'Bolivia', continent=americas, iso_alpha_2_code='BO', iso_alpha_3_code='BOL'),
            Country(name=u'Brazil', continent=americas, iso_alpha_2_code='BR', iso_alpha_3_code='BRA'),
            Country(name=u'Chile', continent=americas, iso_alpha_2_code='CL', iso_alpha_3_code='CHL'),
            Country(name=u'Colombia', continent=americas, iso_alpha_2_code='CO', iso_alpha_3_code='COL'),
            Country(name=u'Ecuador', continent=americas, iso_alpha_2_code='EC', iso_alpha_3_code='ECU'),
            Country(name=u'French Guiana', continent=americas, iso_alpha_2_code='GF', iso_alpha_3_code='GUF'),
            Country(name=u'Guyana', continent=americas, iso_alpha_2_code='GY', iso_alpha_3_code='GUY'),
            Country(name=u'Paraguay', continent=americas, iso_alpha_2_code='PY', iso_alpha_3_code='PRY'),
            Country(name=u'Peru', continent=americas, iso_alpha_2_code='PE', iso_alpha_3_code='PER'),
            Country(name=u'Suriname', continent=americas, iso_alpha_2_code='SR', iso_alpha_3_code='SUR'),
            Country(name=u'Uruguay', continent=americas, iso_alpha_2_code='UY', iso_alpha_3_code='URY'),
            Country(name=u'Venezuela', continent=americas, iso_alpha_2_code='VE', iso_alpha_3_code='VEN'),
        ]
        # Countries in Asia
        asia = Continent.objects.filter(name='Asia').first()
        countries += [
            Country(name=u"Afghanistan", continent=asia, iso_alpha_2_code='AF', iso_alpha_3_code='AFG'),
            Country(name=u"Armenia", continent=asia, iso_alpha_2_code='AM', iso_alpha_3_code='ARM'),
            Country(name=u"Azerbaijan", continent=asia, iso_alpha_2_code='AZ', iso_alpha_3_code='AZE'),
            Country(name=u"Bahrain", continent=asia, iso_alpha_2_code='BH', iso_alpha_3_code='BHR'),
            Country(name=u"Bangladesh", continent=asia, iso_alpha_2_code='BD', iso_alpha_3_code='BGD'),
            Country(name=u"Bhutan", continent=asia, iso_alpha_2_code='BT', iso_alpha_3_code='BTN'),
            Country(name=u"Brunei", continent=asia, iso_alpha_2_code='BN', iso_alpha_3_code='BRN'),
            Country(name=u"Cambodia", continent=asia, iso_alpha_2_code='KH', iso_alpha_3_code='KHM'),
            Country(name=u"China", continent=asia, iso_alpha_2_code='CN', iso_alpha_3_code='CHN'),
            Country(name=u"India", continent=asia, iso_alpha_2_code='IN', iso_alpha_3_code='IND'),
            Country(name=u"Indonesia", continent=asia, iso_alpha_2_code='ID', iso_alpha_3_code='IDN'),
            Country(name=u"Iran", continent=asia, iso_alpha_2_code='IR', iso_alpha_3_code='IRN'),
            Country(name=u"Iraq", continent=asia, iso_alpha_2_code='IQ', iso_alpha_3_code='IRQ'),
            Country(name=u"Israel", continent=asia, iso_alpha_2_code='IL', iso_alpha_3_code='ISR'),
            Country(name=u"Japan", continent=asia, iso_alpha_2_code='JP', iso_alpha_3_code='JPN'),
            Country(name=u"Jordan", continent=asia, iso_alpha_2_code='JO', iso_alpha_3_code='JOR'),
            Country(name=u"Kazakhstan", continent=asia, iso_alpha_2_code='KZ', iso_alpha_3_code='KAZ'),
            Country(name=u"Kuwait", continent=asia, iso_alpha_2_code='KW', iso_alpha_3_code='KWT'),
            Country(name=u"Kyrgyzstan", continent=asia, iso_alpha_2_code='KG', iso_alpha_3_code='KGZ'),
            Country(name=u"Laos", continent=asia, iso_alpha_2_code='LA', iso_alpha_3_code='LAO'),
            Country(name=u"Lebanon", continent=asia, iso_alpha_2_code='LB', iso_alpha_3_code='LBN'),
            Country(name=u"Malaysia", continent=asia, iso_alpha_2_code='MY', iso_alpha_3_code='MYS'),
            Country(name=u"Maldives", continent=asia, iso_alpha_2_code='MV', iso_alpha_3_code='MDV'),
            Country(name=u"Mongolia", continent=asia, iso_alpha_2_code='MN', iso_alpha_3_code='MNG'),
            Country(name=u"Myanmar", continent=asia, iso_alpha_2_code='MM', iso_alpha_3_code='MMR'),
            Country(name=u"Nepal", continent=asia, iso_alpha_2_code='NP', iso_alpha_3_code='NPL'),
            Country(name=u"Oman", continent=asia, iso_alpha_2_code='OM', iso_alpha_3_code='OMN'),
            Country(name=u"Pakistan", continent=asia, iso_alpha_2_code='PK', iso_alpha_3_code='PAK'),
            Country(name=u"Philippines", continent=asia, iso_alpha_2_code='PH', iso_alpha_3_code='PHL'),
            Country(name=u"Qatar", continent=asia, iso_alpha_2_code='QA', iso_alpha_3_code='QAT'),
            Country(name=u"Saudi Arabia", continent=asia, iso_alpha_2_code='SA', iso_alpha_3_code='SAU'),
            Country(name=u"Singapore", continent=asia, iso_alpha_2_code='SG', iso_alpha_3_code='SGP'),
            Country(name=u"South Korea", continent=asia, iso_alpha_2_code='KR', iso_alpha_3_code='KOR'),
            Country(name=u"Sri Lanka", continent=asia, iso_alpha_2_code='LK', iso_alpha_3_code='LKA'),
            Country(name=u"Syria", continent=asia, iso_alpha_2_code='SY', iso_alpha_3_code='SYR'),
            Country(name=u"Tajikistan", continent=asia, iso_alpha_2_code='TJ', iso_alpha_3_code='TJK'),
            Country(name=u"Thailand", continent=asia, iso_alpha_2_code='TH', iso_alpha_3_code='THA'),
            Country(name=u"Taiwan", continent=asia, iso_alpha_2_code='TW', iso_alpha_3_code='TWN'),
            Country(name=u"Turkmenistan", continent=asia, iso_alpha_2_code='TM', iso_alpha_3_code='TKM'),
            Country(name=u"United Arab Emirates", continent=asia, iso_alpha_2_code='AE', iso_alpha_3_code='ARE'),
            Country(name=u"Uzbekistan", continent=asia, iso_alpha_2_code='UZ', iso_alpha_3_code='UZB'),
            Country(name=u"Vietnam", continent=asia, iso_alpha_2_code='VN', iso_alpha_3_code='VNM'),
            Country(name=u"Yemen", continent=asia, iso_alpha_2_code='YE', iso_alpha_3_code='YEM'),
        ]
        # Countries in Europe
        europe = Continent.objects.filter(name='Europe').first()
        countries += [
            Country(name=u"Albania", continent=europe, iso_alpha_2_code='AL', iso_alpha_3_code='ALB'),
            Country(name=u"Andorra", continent=europe, iso_alpha_2_code='AD', iso_alpha_3_code='AND'),
            Country(name=u"Austria", continent=europe, iso_alpha_2_code='AT', iso_alpha_3_code='AUT'),
            Country(name=u"Belarus", continent=europe, iso_alpha_2_code='BY', iso_alpha_3_code='BLR'),
            Country(name=u"Belgium", continent=europe, iso_alpha_2_code='BE', iso_alpha_3_code='BEL'),
            Country(name=u"Bosnia and Herzegovina", continent=europe, iso_alpha_2_code='BA', iso_alpha_3_code='BIH'),
            Country(name=u"Bulgaria", continent=europe, iso_alpha_2_code='BG', iso_alpha_3_code='BGR'),
            Country(name=u"Croatia", continent=europe, iso_alpha_2_code='HR', iso_alpha_3_code='HRV'),
            Country(name=u"Cyprus", continent=europe, iso_alpha_2_code='CY', iso_alpha_3_code='CYP'),
            Country(name=u"Czech Republic", continent=europe, iso_alpha_2_code='CZ', iso_alpha_3_code='CZE'),
            Country(name=u"Denmark", continent=europe, iso_alpha_2_code='DK', iso_alpha_3_code='DNK'),
            Country(name=u"Estonia", continent=europe, iso_alpha_2_code='EE', iso_alpha_3_code='EST'),
            Country(name=u"Faroe Islands", continent=europe, iso_alpha_2_code='FO', iso_alpha_3_code='FRO'),
            Country(name=u"Finland", continent=europe, iso_alpha_2_code='FI', iso_alpha_3_code='FIN'),
            Country(name=u"France", continent=europe, iso_alpha_2_code='FR', iso_alpha_3_code='FRA'),
            Country(name=u"Georgia", continent=europe, iso_alpha_2_code='GE', iso_alpha_3_code='GEO'),
            Country(name=u"Germany", continent=europe, iso_alpha_2_code='DE', iso_alpha_3_code='DEU'),
            Country(name=u"Gibraltar", continent=europe, iso_alpha_2_code='GI', iso_alpha_3_code='GIB'),
            Country(name=u"Greece", continent=europe, iso_alpha_2_code='GR', iso_alpha_3_code='GRC'),
            Country(name=u"Hungary", continent=europe, iso_alpha_2_code='HU', iso_alpha_3_code='HUN'),
            Country(name=u"Iceland", continent=europe, iso_alpha_2_code='IS', iso_alpha_3_code='ISL'),
            Country(name=u"Ireland", continent=europe, iso_alpha_2_code='IE', iso_alpha_3_code='IRL'),
            Country(name=u"Italy", continent=europe, iso_alpha_2_code='IT', iso_alpha_3_code='ITA'),
            Country(name=u"Latvia", continent=europe, iso_alpha_2_code='LV', iso_alpha_3_code='LVA'),
            Country(name=u"Liechtenstein", continent=europe, iso_alpha_2_code='LI', iso_alpha_3_code='LIE'),
            Country(name=u"Lithuania", continent=europe, iso_alpha_2_code='LT', iso_alpha_3_code='LTU'),
            Country(name=u"Luxembourg", continent=europe, iso_alpha_2_code='LU', iso_alpha_3_code='LUX'),
            Country(name=u"Macedonia", continent=europe, iso_alpha_2_code='MK', iso_alpha_3_code='MKD'),
            Country(name=u"Malta", continent=europe, iso_alpha_2_code='MT', iso_alpha_3_code='MLT'),
            Country(name=u"Moldova", continent=europe, iso_alpha_2_code='MD', iso_alpha_3_code='MDA'),
            Country(name=u"Monaco", continent=europe, iso_alpha_2_code='MC', iso_alpha_3_code='MCO'),
            Country(name=u"Montenegro", continent=europe, iso_alpha_2_code='ME', iso_alpha_3_code='MNE'),
            Country(name=u"Netherlands", continent=europe, iso_alpha_2_code='NL', iso_alpha_3_code='NLD'),
            Country(name=u"Norway", continent=europe, iso_alpha_2_code='NO', iso_alpha_3_code='NOR'),
            Country(name=u"Poland", continent=europe, iso_alpha_2_code='PL', iso_alpha_3_code='POL'),
            Country(name=u"Portugal", continent=europe, iso_alpha_2_code='PT', iso_alpha_3_code='PRT'),
            Country(name=u"Romania", continent=europe, iso_alpha_2_code='RO', iso_alpha_3_code='ROU'),
            Country(name=u"Russia", continent=europe, iso_alpha_2_code='RU', iso_alpha_3_code='RUS'),
            Country(name=u"San Marino", continent=europe, iso_alpha_2_code='SM', iso_alpha_3_code='SMR'),
            Country(name=u"Serbia", continent=europe, iso_alpha_2_code='RS', iso_alpha_3_code='SRB'),
            Country(name=u"Slovakia", continent=europe, iso_alpha_2_code='SK', iso_alpha_3_code='SVK'),
            Country(name=u"Slovenia", continent=europe, iso_alpha_2_code='SI', iso_alpha_3_code='SVN'),
            Country(name=u"Spain", continent=europe, iso_alpha_2_code='ES', iso_alpha_3_code='ESP'),
            Country(name=u"Svalbard and Jan Mayen", continent=europe, iso_alpha_2_code='SJ', iso_alpha_3_code='SJM'),
            Country(name=u"Sweden", continent=europe, iso_alpha_2_code='SE', iso_alpha_3_code='SWE'),
            Country(name=u"Switzerland", continent=europe, iso_alpha_2_code='CH', iso_alpha_3_code='CHE'),
            Country(name=u"Turkey", continent=europe, iso_alpha_2_code='TR', iso_alpha_3_code='TUR'),
            Country(name=u"Ukraine", continent=europe, iso_alpha_2_code='UA', iso_alpha_3_code='UKR'),
            Country(name=u"United Kingdom", continent=europe, iso_alpha_2_code='GB', iso_alpha_3_code='GBR'),
            Country(name=u"Vatican City", continent=europe, iso_alpha_2_code='VA', iso_alpha_3_code='VAT'),
        ]
        # Countries in Oceania
        oceania = Continent.objects.filter(name='Oceania').first()
        countries += [
            Country(name=u"Australia", continent=oceania, iso_alpha_2_code='AU', iso_alpha_3_code='AUS'),
            Country(name=u"Cook Islands", continent=oceania, iso_alpha_2_code='CK', iso_alpha_3_code='COK'),
            Country(name=u"Fiji", continent=oceania, iso_alpha_2_code='FJ', iso_alpha_3_code='FJI'),
            Country(name=u"French Polynesia", continent=oceania, iso_alpha_2_code='PF', iso_alpha_3_code='PYF'),
            Country(name=u"Papua New Guinea", continent=oceania, iso_alpha_2_code='PG', iso_alpha_3_code='PNG'),
            Country(name=u"Solomon Islands", continent=oceania, iso_alpha_2_code='SB', iso_alpha_3_code='SLB'),
            Country(name=u"Vanuatu", continent=oceania, iso_alpha_2_code='VU', iso_alpha_3_code='VUT'),
            Country(name=u"Kiribati", continent=oceania, iso_alpha_2_code='KI', iso_alpha_3_code='KIR'),
            Country(name=u"Marshall Islands", continent=oceania, iso_alpha_2_code='MH', iso_alpha_3_code='MHL'),
            Country(name=u"Micronesia", continent=oceania, iso_alpha_2_code='FM', iso_alpha_3_code='FSM'),
            Country(name=u"Nauru", continent=oceania, iso_alpha_2_code='NR', iso_alpha_3_code='NRU'),
            Country(name=u"New Caledonia", continent=oceania, iso_alpha_2_code='NC', iso_alpha_3_code='NCL'),
            Country(name=u"New Zealand", continent=oceania, iso_alpha_2_code='NZ', iso_alpha_3_code='NZL'),
            Country(name=u"Niue", continent=oceania, iso_alpha_2_code='NU', iso_alpha_3_code='NIU'),
            Country(name=u"Palau", continent=oceania, iso_alpha_2_code='PW', iso_alpha_3_code='PLW'),
            Country(name=u"Samoa", continent=oceania, iso_alpha_2_code='WS', iso_alpha_3_code='WSM'),
            Country(name=u"Tonga", continent=oceania, iso_alpha_2_code='TO', iso_alpha_3_code='TON'),
            Country(name=u"Tuvalu", continent=oceania, iso_alpha_2_code='TV', iso_alpha_3_code='TUV'),
            Country(name=u"Wallis and Futuna", continent=oceania, iso_alpha_2_code='WF', iso_alpha_3_code='WLF'),
        ]
        Country.objects.bulk_create(countries)
        print(len(countries), "countries have been added")

        # load cities
        fh = open("cities.txt")
        data = fh.read()
        lines = data.split('\n')
        cities_by_country = {}
        for line in lines:
            if line == "Country,City,AccentCity,Region,Population,Latitude,Longitude":
                continue
            tokens = line.split(',')
            if len(tokens) == 7:
                if tokens[0] in cities_by_country:
                    cities_by_country[tokens[0]].append(line)
                else:
                    cities_by_country[tokens[0]] = [line]
        fh.close()
        cities = []
        for item in cities_by_country.items():
            country = None
            try:
                country = Country.objects.get(iso_alpha_2_code__iexact=item[0])
            except:
                print("Country with code {} not found.".format(item[0]))
            if country:
                for city in item[1]:
                    tokens = city.split(',')
                    cities.append(
                        City(name=tokens[2], country=country, latitude=tokens[5], longitude=tokens[6])
                    )
        if cities:
            City.objects.bulk_create(cities)
            print(len(cities), "cities has been added")
