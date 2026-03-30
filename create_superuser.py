"""
Script to create the default superuser and team test accounts for Project Yananai Intranet.
Runs automatically on Railway startup via Procfile.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Affiliate

# ââ Affiliates ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
affiliates_data = [
    {'name': 'Yananai UK',           'country': 'United Kingdom', 'timezone': 'Europe/London'},
    {'name': 'Yananai Zambia',       'country': 'Zambia',         'timezone': 'Africa/Lusaka'},
    {'name': 'Yananai India',        'country': 'India',          'timezone': 'Asia/Kolkata'},
    {'name': 'Yananai Zimbabwe',     'country': 'Zimbabwe',       'timezone': 'Africa/Harare'},
    {'name': 'Yananai South Africa', 'country': 'South Africa',   'timezone': 'Africa/Johannesburg'},
]

for data in affiliates_data:
    affiliate, created = Affiliate.objects.get_or_create(
        name=data['name'],
        defaults={'country': data['country'], 'timezone': data['timezone']}
    )
    if created:
        print(f"Created affiliate: {affiliate.name}")

# Handy affiliate lookups
uk_aff = Affiliate.objects.filter(name='Yananai UK').first()
zambia_aff = Affiliate.objects.filter(name='Yananai Zambia').first()
india_aff = Affiliate.objects.filter(name='Yananai India').first()
zimbabwe_aff = Affiliate.objects.filter(name='Yananai Zimbabwe').first()
sa_aff = Affiliate.objects.filter(name='Yananai South Africa').first()

# ââ Default accounts âââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
DEFAULT_PASSWORD = 'Yananai2024!'

accounts = [
    # (email, full_name, role, team, is_superuser, affiliate, job_title)
    (
        'admin@yananai.org',
        'David Harris Chukwuebuka',
        'admin', 'it_admin', True, uk_aff,
        'Webmaster & User Support Engineer',
    ),
    (
        'ceo@yananai.org',
        'Global Executive Lead',
        'staff', 'global_exec', False, uk_aff,
        'Chief Executive Officer',
    ),
    (
        'board@yananai.org',
        'Board Member',
        'staff', 'board', False, uk_aff,
        'Board of Trustees',
    ),
    (
        'regional@yananai.org',
        'Regional Manager',
        'staff', 'regional_mgmt', False, uk_aff,
        'Regional Management Team',
    ),
    (
        'india@yananai.org',
        'India Team Member',
        'staff', 'india', False, india_aff,
        'India Operations',
    ),
    (
        'southafrica@yananai.org',
        'South Africa Team Member',
        'staff', 'south_africa', False, sa_aff,
        'South Africa Operations',
    ),
    (
        'zambia@yananai.org',
        'Zambia Team Member',
        'staff', 'zambia', False, zambia_aff,
        'Zambia Operations',
    ),
    (
        'zimbabwe@yananai.org',
        'Zimbabwe Team Member',
        'staff', 'zimbabwe', False, zimbabwe_aff,
        'Zimbabwe Operations',
    ),
]

for email, full_name, role, team, is_su, affiliate, job_title in accounts:
    if not User.objects.filter(email=email).exists():
        if is_su:
            user = User.objects.create_superuser(
                email=email,
                password='Admin1234!',
                full_name=full_name,
                role=role,
                team=team,
                job_title=job_title,
                affiliate=affiliate,
            )
        else:
            user = User.objects.create_user(
                email=email,
                password=DEFAULT_PASSWORD,
                full_name=full_name,
                role=role,
                team=team,
                job_title=job_title,
                affiliate=affiliate,
                is_staff=False,
            )
        print(f"Created user: {email} (team={team})")
    else:
        # Ensure existing users have the right team set
        u = User.objects.get(email=email)
        if u.team == 'general' and team != 'general':
            u.team = team
            u.save(update_fields=['team'])
            print(f"Updated team for: {email} â {team}")
        else:
            print(f"User already exists: {email}")

print("\nâ Default setup complete.")

# ââ Fix any admin-created users that have blank username (causes 500 on 2nd create) ââ
broken = User.objects.filter(username='').exclude(email='')
for u in broken:
    u.username = u.email
    u.save(update_fields=['username'])
    print(f"Fixed username for: {u.email}")

# ââ Real team accounts (all 75 members from yananai.org) ââââââââââââââââââââ
REAL_PASSWORD = 'Yananai2024!'

real_accounts = [
    # (email, full_name, role, team, affiliate, job_title)

    # Global Executive Leadership Team
    ('tsungai.magaya@yananai.com',          'Tsungai Magaya',           'admin', 'global_exec', uk_aff,       'Chief Executive Officer'),
    ('kerry.taylor-smith@yananai.com',       'Kerry Taylor-Smith',        'staff', 'global_exec', uk_aff,       'Chief People and Governance Officer'),
    ('maria.flygare@yananai.com',            'Maria Flygare',             'staff', 'global_exec', uk_aff,       'Global General Counsel'),
    ('zoe.chinaka@yananai.com',              'Zoe Chinaka',               'staff', 'global_exec', uk_aff,       'Chief Advancement Officer'),
    ('ash.patel@yananai.com',                'Ash Patel',                 'staff', 'global_exec', uk_aff,       'Chief Mission Operations & Infrastructure Officer'),
    ('vivian.okolie@yananai.com',            'Vivian Okolie',             'staff', 'global_exec', uk_aff,       'Chief Financial Officer'),
    ('sandra.mtambirwa@yananai.com',         'Sandra Mtambirwa',          'staff', 'global_exec', uk_aff,       'Head of Sustainability'),
    ('prashant.gangwar@yananai.com',         'Prashant Gangwar',          'staff', 'global_exec', uk_aff,       'Head of Education Services'),
    ('niq.sibanda@yananai.com',              'Niq Sibanda',               'staff', 'global_exec', uk_aff,       'Head of Global Partnerships'),
    ('monica.schroeder@yananai.com',         'Monica Schroeder',          'staff', 'global_exec', uk_aff,       'Head of Technology and Risk Management'),
    ('river.lu@yananai.com',                 'River Lu',                  'staff', 'global_exec', uk_aff,       'Director of AI Integration & Lead Impact Solutions Engineer'),
    ('chiamaka.nwangwu@yananai.com',         'Chiamaka Nwangwu',          'staff', 'global_exec', uk_aff,       'Senior Administrator'),
    ('chide.atojoko-omomvude@yananai.com',   'Chide Atojoko-Omomvude',    'staff', 'global_exec', uk_aff,       'Lead Process Optimisation and Performance Executive'),
    ('daniel.ehighalua@yananai.com',         'Daniel Ehighalua',          'staff', 'global_exec', uk_aff,       'Deputy Global General Counsel'),
    ('carlo.castillo@yananai.com',           'Carlo Castillo',            'staff', 'global_exec', uk_aff,       'Principal Engineer & Engineering Lead (Software)'),
    ('oliver.vembo@yananai.com',             'Oliver Vembo',              'staff', 'global_exec', uk_aff,       'Head of Relief Operations'),
    ('ana.topalli@yananai.com',              'Ana Topalli',               'staff', 'global_exec', uk_aff,       'Director of Funding'),
    ('nyasha.mwendere@yananai.com',          'Nyasha Mwendere',           'staff', 'global_exec', uk_aff,       'Director of MEL & Staff Development'),
    ('kesh.ladwa@yananai.com',               'Kesh Ladwa',                'staff', 'global_exec', uk_aff,       'Head of Talent Acquisition'),

    # Regional Management Team
    ('edward.nyambawaro@yananai.com',        'Edward Nyambawaro',         'staff', 'regional_mgmt', uk_aff,    'Regional Director â Southern Africa'),
    ('chaitanya.singh@yananai.com',          'Chaitanya Singh',           'staff', 'regional_mgmt', uk_aff,    'Regional Director â South Asia'),
    ('fordson.kafweku@yananai.com',          'Fordson Kafweku',           'staff', 'regional_mgmt', uk_aff,    'Deputy Regional Director â Southern Africa'),
    ('glenda.vergeer@yananai.com',           'Glenda Vergeer',            'staff', 'regional_mgmt', uk_aff,    'Regional Head of Sustainability â Southern Africa'),

    # India Team
    ('avinash.khairnar@yananai.com',         'Avinash Khairnar',          'staff', 'india', india_aff,         'Country Director'),
    ('gajendra.singh@yananai.com',           'Gajendra Singh',            'staff', 'india', india_aff,         'Deputy Country Director â Technology & Sustainable Skills'),
    ('ramesh.kumar@yananai.com',             'Ramesh Kumar',              'staff', 'india', india_aff,         'Senior Manager â HR and Program Delivery'),
    ('karthik@yananai.com',                  'Karthik',                   'staff', 'india', india_aff,         'General Counsel'),
    ('ravi.eleti@yananai.com',               'Ravi Eleti',                'staff', 'india', india_aff,         'Regional Manager â Andhra Pradesh'),
    ('ganesh.jothivelan@yananai.com',        'Ganesh Jothivelan',         'staff', 'india', india_aff,         'National Manager â ICT, Data Insights & Analytics'),
    ('rahul.garg@yananai.com',               'Rahul Garg',                'staff', 'india', india_aff,         'Senior Legal Counsel'),
    ('anuparma.raghukumar@yananai.com',      'Anuparma Raghukumar',       'staff', 'india', india_aff,         'National Head of Funding and Grants Management'),
    ('anshu.jain@yananai.com',               'Anshu Jain',                'staff', 'india', india_aff,         'National Head of Finance'),
    ('meghna.ghosh@yananai.com',             'Meghna Ghosh',              'staff', 'india', india_aff,         'National Head of Communications'),
    ('saurabh.kashyap@yananai.com',          'Saurabh Kashyap',           'staff', 'india', india_aff,         'Senior Legal Counsel'),
    ('simranjeet.talwar@yananai.com',        'Simranjeet Talwar',         'staff', 'india', india_aff,         'Senior Legal Counsel'),

    # South Africa Team (Niq Sibanda is in global_exec above)
    ('bonani.ndlovu@yananai.com',            'Bonani Ndlovu',             'staff', 'south_africa', sa_aff,     'Deputy Country Director â Legal, Compliance and HR'),
    ('lerato.madiba@yananai.com',            'Lerato Madiba',             'staff', 'south_africa', sa_aff,     'National Program Manager â Community Learning Hubs'),
    ('sipho.pilime@yananai.com',             'Sipho Pilime',              'staff', 'south_africa', sa_aff,     'National Program Manager â Humanitarian Aid'),
    ('kgabo.mojela@yananai.com',             'Kgabo Mojela',              'staff', 'south_africa', sa_aff,     'National Program Manager â Sustainable Skills Development'),
    ('themba.mdaka@yananai.com',             'Themba Mdaka',              'staff', 'south_africa', sa_aff,     'National Manager â SHERQ'),
    ('edzani.muedi@yananai.com',             'Edzani Muedi',              'staff', 'south_africa', sa_aff,     'National Head of Funding and Grants Management'),
    ('brandon.jansen@yananai.com',           'Brandon Jansen',            'staff', 'south_africa', sa_aff,     'Senior Legal Counsel'),
    ('rachel.motsepe@yananai.com',           'Rachel Motsepe',            'staff', 'south_africa', sa_aff,     'National Program Manager â Community Engagement'),
    ('nikolay.sankar@yananai.com',           'Nikolay Sankar',            'staff', 'south_africa', sa_aff,     'National Head of Finance'),

    # Zambia Team (Glenda Vergeer is in regional_mgmt above)
    ('gordon.tembo@yananai.com',             'Gordon Tembo',              'staff', 'zambia', zambia_aff,        'Country Director'),
    ('joyce.malasha@yananai.com',            'Joyce Malasha',             'staff', 'zambia', zambia_aff,        'Deputy Country Director â Head of Resourcing and Administration'),
    ('zondwayo.banda@yananai.com',           'Zondwayo Banda',            'staff', 'zambia', zambia_aff,        'Deputy Country Director â Head of Finance and HR'),
    ('cassandra.munungwe-mhone@yananai.com', 'Cassandra Munungwe-Mhone',  'staff', 'zambia', zambia_aff,        'National Head of Communications'),
    ('austin.sichinga@yananai.com',          'Austin Sichinga',           'staff', 'zambia', zambia_aff,        'National Manager â ICT'),
    ('chilufa.kalisha@yananai.com',          'Chilufa Kalisha',           'staff', 'zambia', zambia_aff,        'Mission Funding Executive'),
    ('cleophas.kamurai@yananai.com',         'Cleophas Kamurai',          'staff', 'zambia', zambia_aff,        'National Program Manager â Community Learning Hubs'),
    ('gilbert.mwanza@yananai.com',           'Gilbert Mwanza',            'staff', 'zambia', zambia_aff,        'General Counsel'),

    # Zimbabwe Team
    ('innocent.moyo@yananai.com',            'Innocent Moyo',             'staff', 'zimbabwe', zimbabwe_aff,   'Country Director'),
    ('beauty.nhari@yananai.com',             'Beauty Nhari',              'staff', 'zimbabwe', zimbabwe_aff,   'Deputy Country Director â Internal Management and Compliance'),
    ('mike.makhetho@yananai.com',            'Mike Makhetho',             'staff', 'zimbabwe', zimbabwe_aff,   'Deputy Country Director â Programs Impact and Partnerships'),
    ('zen.kakomo@yananai.com',               'Zen Kakomo',                'staff', 'zimbabwe', zimbabwe_aff,   'Senior Manager â HR and Program Delivery'),
    ('dudzai.kahuni@yananai.com',            'Dudzai Kahuni',             'staff', 'zimbabwe', zimbabwe_aff,   'National Program Manager â Humanitarian Aid'),
    ('juliet.madamombe@yananai.com',         'Juliet Madamombe',          'staff', 'zimbabwe', zimbabwe_aff,   'National Head of Funding and Grants Management'),
    ('tendai.nkomo@yananai.com',             'Tendai Nkomo',              'staff', 'zimbabwe', zimbabwe_aff,   'Public Health Specialist â Health Systems and Community Health'),
    ('kenneth.maeka@yananai.com',            'Kenneth Maeka',             'staff', 'zimbabwe', zimbabwe_aff,   'Public Health Specialist â Epidemiology and Disease Control'),
    ('lorraine.rukarwa@yananai.com',         'Lorraine Rukarwa',          'staff', 'zimbabwe', zimbabwe_aff,   'National Program Manager â Community Engagement'),
    ('david.dzikiti@yananai.com',            'David Dzikiti',             'staff', 'zimbabwe', zimbabwe_aff,   'National Head of Communications'),
    ('moira.gundu@yananai.com',              'Moira Gundu',               'staff', 'zimbabwe', zimbabwe_aff,   'Principal Specialist â Knowledge, Learning and Gender Empowerment'),
    ('onious.mtetwa@yananai.com',            'Onious Mtetwa',             'staff', 'zimbabwe', zimbabwe_aff,   'National Program Manager â Agriculture'),
    ('elastos.chimwanda@yananai.com',        'Elastos Chimwanda',         'staff', 'zimbabwe', zimbabwe_aff,   'National Head of ICT'),
    ('renias.shoko@yananai.com',             'Renias Shoko',              'staff', 'zimbabwe', zimbabwe_aff,   'National Program Manager â The Journey'),
    ('faustina.njanji@yananai.com',          'Faustina Njanji',           'staff', 'zimbabwe', zimbabwe_aff,   'National Program Manager â Community Learning Hubs'),
    ('taurai.mrewa@yananai.com',             'Taurai Mrewa',              'staff', 'zimbabwe', zimbabwe_aff,   'General Counsel'),
    ('lorraine.zhandire-bhebhe@yananai.com', 'Lorraine Zhandire-Bhebhe',  'staff', 'zimbabwe', zimbabwe_aff,   'Senior Legal Counsel'),
    ('freedom.makaya@yananai.com',           'Freedom Makaya',            'staff', 'zimbabwe', zimbabwe_aff,   'Senior Legal Counsel'),
    ('amon.manjovha@yananai.com',            'Amon Manjovha',             'staff', 'zimbabwe', zimbabwe_aff,   'National Head of Internal Audit'),
    ('farisai.perera@yananai.com',           'Farisai Perera',            'staff', 'zimbabwe', zimbabwe_aff,   'Mission Funding Executive'),
    ('sibonginkosi.mpofu@yananai.com',       'Sibonginkosi Mpofu',        'staff', 'zimbabwe', zimbabwe_aff,   'Mission Funding Executive'),
    ('tapiwa.chadamoyo@yananai.com',         'Tapiwa Chadamoyo',          'staff', 'zimbabwe', zimbabwe_aff,   'National Head of Finance'),

    # Trustees (Sandra Mtambirwa is in global_exec above)
    ('nick.mtambirwa@yananai.com',           'Nick Mtambirwa',            'staff', 'board', uk_aff,            'Chair of Trustees'),
    ('grace.chauruka@yananai.com',           'Grace Chauruka',            'staff', 'board', uk_aff,            'Trustee'),
    ('chris.evans@yananai.com',              'Chris Evans',               'staff', 'board', uk_aff,            'Trustee'),
    ('edmore.chitokomerere@yananai.com',     'Edmore Chitokomerere',      'staff', 'board', uk_aff,            'Trustee'),
]

created_count = 0
skipped_count = 0
for email, full_name, role, team, affiliate, job_title in real_accounts:
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(
            email=email,
            password=REAL_PASSWORD,
            full_name=full_name,
            role=role,
            team=team,
            job_title=job_title,
            affiliate=affiliate,
            is_staff=False,
        )
        print(f"  + {full_name} ({email})")
        created_count += 1
    else:
        skipped_count += 1

print(f"\nâ Real accounts: {created_count} created, {skipped_count} already existed.")
print("Admin login:  admin@yananai.org / Admin1234!")
print(f"Team accounts password: {DEFAULT_PASSWORD}")
