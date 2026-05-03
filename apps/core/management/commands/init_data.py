from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time


class Command(BaseCommand):
    help = 'Инициализация данных клиники'

    def handle(self, *args, **kwargs):
        from apps.doctors.models import Specialization, Doctor, Schedule
        from apps.services.models import ServiceCategory, Service
        from apps.patients.models import Patient, MedicalRecord
        from apps.appointments.models import Appointment

        self.stdout.write('📋 Создаём специализации...')
        specs = {}
        specs_data = [
            ('Пластический хирург', 'Операции по коррекции и улучшению внешности'),
            ('Косметолог', 'Неинвазивные процедуры по уходу за кожей'),
            ('Дерматолог', 'Лечение заболеваний кожи'),
            ('Анестезиолог', 'Обеспечение анестезии при операциях'),
            ('Трихолог', 'Лечение волос и кожи головы'),
        ]
        for name, desc in specs_data:
            spec, _ = Specialization.objects.get_or_create(name=name, defaults={'description': desc})
            specs[name] = spec

        self.stdout.write('👨‍⚕️ Создаём врачей...')
        doctors_data = [
            {
                'first_name': 'Александр', 'last_name': 'Морозов', 'middle_name': 'Сергеевич',
                'specialization': specs['Пластический хирург'],
                'photo': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=400',
                'experience_years': 15, 'rating': 4.9,
                'bio': 'Ведущий пластический хирург клиники с 15-летним опытом. Специализируется на ринопластике, блефаропластике и абдоминопластике.',
                'education': 'РНИМУ им. Пирогова, специализация по пластической хирургии. Стажировка в Германии и США.',
                'phone': '+7 (495) 111-11-01', 'email': 'morozov@klinika.ru',
            },
            {
                'first_name': 'Елена', 'last_name': 'Соколова', 'middle_name': 'Владимировна',
                'specialization': specs['Косметолог'],
                'photo': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400',
                'experience_years': 10, 'rating': 4.8,
                'bio': 'Сертифицированный косметолог. Эксперт по инъекционным методикам омоложения.',
                'education': 'Первый МГМУ им. Сеченова. Курсы по дерматокосметологии в Италии.',
                'phone': '+7 (495) 111-11-02', 'email': 'sokolova@klinika.ru',
            },
            {
                'first_name': 'Дмитрий', 'last_name': 'Волков', 'middle_name': 'Игоревич',
                'specialization': specs['Пластический хирург'],
                'photo': 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=400',
                'experience_years': 12, 'rating': 4.7,
                'bio': 'Хирург-ортопед с опытом в контурной пластике. Специализируется на маммопластике.',
                'education': 'МГМСУ. Стажировки в ведущих клиниках Южной Кореи.',
                'phone': '+7 (495) 111-11-03', 'email': 'volkov@klinika.ru',
            },
            {
                'first_name': 'Ольга', 'last_name': 'Петрова', 'middle_name': 'Николаевна',
                'specialization': specs['Дерматолог'],
                'photo': 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400',
                'experience_years': 8, 'rating': 4.8,
                'bio': 'Дерматолог-косметолог. Специалист по лечению акне, пигментации и аппаратным методикам.',
                'education': 'РУДН. Повышение квалификации в Европейской академии дерматологии.',
                'phone': '+7 (495) 111-11-04', 'email': 'petrova@klinika.ru',
            },
            {
                'first_name': 'Мария', 'last_name': 'Иванова', 'middle_name': 'Андреевна',
                'specialization': specs['Косметолог'],
                'photo': 'https://images.unsplash.com/photo-1614608682850-e0d6ed316d47?w=400',
                'experience_years': 6, 'rating': 4.6,
                'bio': 'Специалист по уходу за кожей и аппаратной косметологии. Мастер по химическим пилингам.',
                'education': 'МГМУ. Сертификаты международных школ косметологии.',
                'phone': '+7 (495) 111-11-05', 'email': 'ivanova@klinika.ru',
            },
        ]
        doctors = {}
        for d in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                last_name=d['last_name'], first_name=d['first_name'],
                defaults=d
            )
            doctors[d['last_name']] = doctor
            if created:
                for day in [0, 1, 2, 3, 4]:
                    Schedule.objects.get_or_create(
                        doctor=doctor, day_of_week=day,
                        defaults={'start_time': time(9, 0), 'end_time': time(18, 0)}
                    )

        self.stdout.write('💉 Создаём категории и услуги...')
        cats = {}
        cats_data = [
            ('Хирургия лица', '✂️', 0),
            ('Хирургия тела', '🏥', 1),
            ('Инъекционная косметология', '💉', 2),
            ('Аппаратная косметология', '⚡', 3),
            ('Уход за кожей', '✨', 4),
        ]
        for name, icon, order in cats_data:
            cat, _ = ServiceCategory.objects.get_or_create(name=name, defaults={'icon': icon, 'order': order})
            cats[name] = cat

        services_data = [
            {
                'category': cats['Хирургия лица'], 'name': 'Ринопластика',
                'description': 'Коррекция формы и размера носа. Операция позволяет изменить контур, высоту переносицы, форму кончика носа.',
                'duration_minutes': 180, 'price': 120000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=600',
                'is_popular': True,
                'rehabilitation': 'Реабилитация 2-4 недели. Отёк спадает через 3 месяца.',
                'contraindications': 'Возраст до 18 лет, беременность, онкология, нарушения свёртываемости крови.',
            },
            {
                'category': cats['Хирургия лица'], 'name': 'Блефаропластика',
                'description': 'Операция на веках — устраняет нависшие веки, мешки под глазами, возвращает молодой взгляд.',
                'duration_minutes': 120, 'price': 60000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600',
                'is_popular': True,
                'rehabilitation': 'Синяки проходят через 7-14 дней. Полный результат через 1 месяц.',
                'contraindications': 'Глаукома, синдром сухого глаза, диабет.',
            },
            {
                'category': cats['Хирургия лица'], 'name': 'Подтяжка лица (SMAS-лифтинг)',
                'description': 'Хирургическое омоложение лица и шеи. Устраняет птоз тканей, морщины, восстанавливает контур.',
                'duration_minutes': 240, 'price': 180000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1519824145371-296894a0daa9?w=600',
                'is_popular': False,
                'rehabilitation': 'Реабилитация 4-6 недель. Результат сохраняется 8-10 лет.',
                'contraindications': 'Сахарный диабет, нарушения свёртываемости, тяжёлые сердечно-сосудистые заболевания.',
            },
            {
                'category': cats['Хирургия тела'], 'name': 'Маммопластика (увеличение груди)',
                'description': 'Увеличение, подтяжка или уменьшение груди с помощью имплантов или собственных тканей.',
                'duration_minutes': 150, 'price': 150000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=600',
                'is_popular': True,
                'rehabilitation': 'Ношение специального белья 2 месяца. Возврат к активности через 4-6 недель.',
                'contraindications': 'Беременность, кормление грудью, онкология.',
            },
            {
                'category': cats['Хирургия тела'], 'name': 'Липосакция',
                'description': 'Удаление жировых отложений с помощью инновационных методов. Живот, бёдра, руки, спина.',
                'duration_minutes': 120, 'price': 80000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600',
                'is_popular': True,
                'rehabilitation': 'Компрессионное бельё 2 месяца. Результат через 3-6 месяцев.',
                'contraindications': 'ИМТ более 30, диабет, нарушения свёртываемости.',
            },
            {
                'category': cats['Хирургия тела'], 'name': 'Абдоминопластика',
                'description': 'Коррекция живота — иссечение лишней кожи и жира, восстановление мышечного корсета.',
                'duration_minutes': 180, 'price': 130000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600',
                'is_popular': False,
                'rehabilitation': 'Реабилитация 6-8 недель. Компрессионное бельё обязательно.',
                'contraindications': 'Планирование беременности, ожирение, тяжёлые хронические заболевания.',
            },
            {
                'category': cats['Инъекционная косметология'], 'name': 'Ботулинотерапия (Ботокс)',
                'description': 'Коррекция мимических морщин препаратами на основе ботулотоксина. Лоб, межбровье, периорбитальная зона.',
                'duration_minutes': 30, 'price': 8000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=600',
                'is_popular': True,
                'rehabilitation': 'Без реабилитации. Эффект через 7-14 дней, сохраняется 4-6 месяцев.',
                'contraindications': 'Беременность, лактация, миастения, индивидуальная непереносимость.',
            },
            {
                'category': cats['Инъекционная косметология'], 'name': 'Контурная пластика (филлеры)',
                'description': 'Восполнение объёмов и коррекция морщин гиалуроновой кислотой. Губы, скулы, носогубные складки.',
                'duration_minutes': 45, 'price': 12000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=600',
                'is_popular': True,
                'rehabilitation': 'Отёк 2-3 дня. Результат сохраняется 6-18 месяцев.',
                'contraindications': 'Аутоиммунные заболевания, беременность, воспаления в зоне введения.',
            },
            {
                'category': cats['Аппаратная косметология'], 'name': 'SMAS-лифтинг (ультразвук)',
                'description': 'Безоперационная подтяжка лица и тела с помощью высокочастотного ультразвука.',
                'duration_minutes': 60, 'price': 25000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600',
                'is_popular': True,
                'rehabilitation': 'Без реабилитации. Результат нарастает 3-6 месяцев.',
                'contraindications': 'Импланты в зоне воздействия, онкология, беременность.',
            },
            {
                'category': cats['Уход за кожей'], 'name': 'Химический пилинг',
                'description': 'Обновление кожи с помощью кислот. Устраняет пигментацию, акне, выравнивает рельеф и тон.',
                'duration_minutes': 60, 'price': 5000, 'price_from': True,
                'image_url': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600',
                'is_popular': True,
                'rehabilitation': 'Шелушение 3-7 дней. Защита от солнца обязательна.',
                'contraindications': 'Беременность, активные воспаления, аллергия на компоненты.',
            },
        ]
        services = {}
        for s in services_data:
            service, created = Service.objects.get_or_create(
                name=s['name'],
                defaults=s
            )
            services[s['name']] = service

        # Assign doctors to services
        if 'Морозов' in doctors and 'Ринопластика' in services:
            services['Ринопластика'].doctors.add(doctors['Морозов'])
            services['Блефаропластика'].doctors.add(doctors['Морозов'])
            services['Подтяжка лица (SMAS-лифтинг)'].doctors.add(doctors['Морозов'])
        if 'Волков' in doctors:
            services['Маммопластика (увеличение груди)'].doctors.add(doctors['Волков'])
            services['Липосакция'].doctors.add(doctors['Волков'])
            services['Абдоминопластика'].doctors.add(doctors['Волков'])
        if 'Соколова' in doctors:
            services['Ботулинотерапия (Ботокс)'].doctors.add(doctors['Соколова'])
            services['Контурная пластика (филлеры)'].doctors.add(doctors['Соколова'])
        if 'Иванова' in doctors:
            services['Химический пилинг'].doctors.add(doctors['Иванова'])
            services['SMAS-лифтинг (ультразвук)'].doctors.add(doctors['Иванова'])

        self.stdout.write('👥 Создаём пациентов...')
        patients_data = [
            {'first_name': 'Анна', 'last_name': 'Смирнова', 'middle_name': 'Олеговна', 'date_of_birth': date(1985, 3, 15), 'gender': 'F', 'phone': '+7 (916) 111-22-33', 'email': 'smirnova@mail.ru', 'blood_type': 'A+'},
            {'first_name': 'Татьяна', 'last_name': 'Козлова', 'middle_name': 'Михайловна', 'date_of_birth': date(1978, 7, 22), 'gender': 'F', 'phone': '+7 (916) 222-33-44', 'email': 'kozlova@mail.ru', 'blood_type': 'B+'},
            {'first_name': 'Наталья', 'last_name': 'Новикова', 'middle_name': 'Петровна', 'date_of_birth': date(1990, 11, 8), 'gender': 'F', 'phone': '+7 (916) 333-44-55', 'email': 'novikova@mail.ru', 'blood_type': 'O+'},
            {'first_name': 'Андрей', 'last_name': 'Кузнецов', 'middle_name': 'Александрович', 'date_of_birth': date(1975, 5, 30), 'gender': 'M', 'phone': '+7 (916) 444-55-66', 'email': 'kuznetsov@mail.ru', 'blood_type': 'AB+'},
            {'first_name': 'Светлана', 'last_name': 'Попова', 'middle_name': 'Юрьевна', 'date_of_birth': date(1982, 9, 14), 'gender': 'F', 'phone': '+7 (916) 555-66-77', 'email': 'popova@mail.ru', 'blood_type': 'A-'},
            {'first_name': 'Ирина', 'last_name': 'Лебедева', 'middle_name': 'Сергеевна', 'date_of_birth': date(1993, 2, 28), 'gender': 'F', 'phone': '+7 (916) 666-77-88', 'email': 'lebedeva@mail.ru', 'blood_type': 'B-'},
        ]
        patients = []
        for p in patients_data:
            patient, created = Patient.objects.get_or_create(phone=p['phone'], defaults=p)
            patients.append(patient)

        self.stdout.write('📅 Создаём записи...')
        from datetime import timedelta
        today = date.today()
        appointments_data = [
            {'patient': patients[0], 'doctor': doctors.get('Морозов'), 'service': services.get('Ринопластика'), 'date': today, 'time': time(10, 0), 'status': 'confirmed', 'price': 125000, 'complaint': 'Хочу скорректировать форму носа'},
            {'patient': patients[1], 'doctor': doctors.get('Соколова'), 'service': services.get('Ботулинотерапия (Ботокс)'), 'date': today, 'time': time(11, 30), 'status': 'confirmed', 'price': 9500, 'complaint': 'Морщины на лбу'},
            {'patient': patients[2], 'doctor': doctors.get('Иванова'), 'service': services.get('Химический пилинг'), 'date': today + timedelta(days=1), 'time': time(14, 0), 'status': 'pending', 'price': 6000, 'complaint': 'Пигментация и неровный тон'},
            {'patient': patients[3], 'doctor': doctors.get('Волков'), 'service': services.get('Липосакция'), 'date': today + timedelta(days=2), 'time': time(9, 0), 'status': 'confirmed', 'price': 85000, 'complaint': 'Живот и бока'},
            {'patient': patients[4], 'doctor': doctors.get('Петрова'), 'service': None, 'date': today - timedelta(days=3), 'time': time(15, 0), 'status': 'completed', 'price': 3500, 'complaint': 'Акне', 'result': 'Назначена терапия', 'is_paid': True},
            {'patient': patients[5], 'doctor': doctors.get('Соколова'), 'service': services.get('Контурная пластика (филлеры)'), 'date': today - timedelta(days=5), 'time': time(12, 0), 'status': 'completed', 'price': 15000, 'is_paid': True, 'result': 'Губы 1 мл, носогубные складки'},
        ]
        for a in appointments_data:
            if a.get('doctor'):
                Appointment.objects.get_or_create(
                    patient=a['patient'], doctor=a['doctor'], date=a['date'], time=a['time'],
                    defaults={k: v for k, v in a.items() if k not in ['patient', 'doctor', 'date', 'time']}
                )

        self.stdout.write(self.style.SUCCESS('✅ Все данные успешно загружены!'))
