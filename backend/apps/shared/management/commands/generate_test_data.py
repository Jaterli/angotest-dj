
# apps/shared/management/commands/generate_test_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.test.models import Test, Question, Answer
from apps.results.models import Result
from apps.shared.models import get_topics
from datetime import datetime, timedelta
import random
import logging
from faker import Faker  # Necesitas instalar: pip install Faker
from django.db.models import Avg, Count


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Genera datos de prueba para tests, usuarios y resultados'
    
    def add_arguments(self, parser):
        # Configuración de usuarios
        parser.add_argument('--users', type=int, default=15, help='Número de usuarios a crear')
        parser.add_argument('--admin-percentage', type=float, default=0.1, help='Porcentaje de admins (0-1)')
        parser.add_argument('--guest-percentage', type=float, default=0.2, help='Porcentaje de invitados (0-1)')
        
        # Configuración de tests
        parser.add_argument('--tests-per-topic', type=int, default=2, help='Tests por combinación de tema específico')
        parser.add_argument('--questions-per-test', type=int, default=8, help='Preguntas por test (min 3)')
        parser.add_argument('--answers-per-question', type=int, default=4, help='Respuestas por pregunta (min 2)')
        
        # Configuración de fechas
        parser.add_argument('--test-start-date', type=str, default='2024-01-01', help='Fecha inicio tests (YYYY-MM-DD)')
        parser.add_argument('--test-end-date', type=str, default='2024-12-31', help='Fecha fin tests (YYYY-MM-DD)')
        
        # Configuración de resultados
        parser.add_argument('--results-per-user', type=int, default=8, help='Resultados por usuario')
        parser.add_argument('--incomplete-percentage', type=float, default=0.15, help='Porcentaje de tests incompletos (0-1)')
        parser.add_argument('--abandoned-percentage', type=float, default=0.10, help='Porcentaje de tests abandonados (0-1)')
        
        # Flags de control
        parser.add_argument('--clear-existing', action='store_true', help='Limpiar datos existentes antes de generar')
        parser.add_argument('--skip-users', action='store_true', help='Saltar creación de usuarios')
        parser.add_argument('--seed', type=int, default=42, help='Semilla para reproducibilidad')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = None
        self.topics = []
        self.created_users = []
        self.created_tests = []
        
    def handle(self, *args, **options):
        # Configurar semilla para reproducibilidad
        random.seed(options['seed'])
        self.fake = Faker()
        self.fake.seed_instance(options['seed'])
        
        self.stdout.write(self.style.SUCCESS(f'🚀 Iniciando generación de datos de prueba (Semilla: {options["seed"]})'))
        
        # Limpiar datos existentes si se solicita
        if options['clear_existing']:
            self.clear_existing_data()
        
        # 1. Crear usuarios (o usar existentes)
        if not options['skip_users']:
            self.create_users(options)
        else:
            # Usar usuarios existentes
            self.created_users = list(User.objects.filter(is_active=True))
            self.stdout.write(self.style.SUCCESS(f'📌 Usando {len(self.created_users)} usuarios existentes'))
        
        # Verificar que hay usuarios
        if not self.created_users:
            self.stdout.write(self.style.ERROR('❌ No hay usuarios disponibles. Usa --skip_users=False o crea usuarios primero.'))
            return
        
        # 2. Obtener y procesar temas
        self.load_topics()
        
        # Verificar si hay temas
        if not self.topics:
            self.stdout.write(self.style.ERROR('❌ No hay temas cargados en la base de datos.'))
            self.stdout.write(self.style.WARNING('Por favor, ejecuta primero: python manage.py load_predefined_topics'))
            return
        
        # 3. Crear tests
        self.create_tests(options)
        
        # Verificar que hay tests
        if not self.created_tests:
            self.stdout.write(self.style.WARNING('⚠️  No se crearon tests. Verifica los temas.'))
            return
        
        # 4. Crear preguntas y respuestas
        self.create_questions_and_answers(options)
        
        # 5. Crear resultados
        self.create_results(options)
        
        # Mostrar estadísticas finales
        self.show_statistics()
        
        self.stdout.write(self.style.SUCCESS('✅ Generación de datos completada exitosamente'))
    
    def clear_existing_data(self):
        """Limpia los datos existentes en orden correcto por FK"""
        self.stdout.write('🗑️  Limpiando datos existentes...')
        
        Result.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Test.objects.all().delete()
        
        # Opcional: No borrar usuarios para mantener sesiones
        keep_users = input('¿Deseas mantener los usuarios existentes? (s/n): ') == 's'
        if not keep_users:
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write('   Usuarios eliminados')
        else:
            self.stdout.write('   Usuarios mantenidos')
        
        self.stdout.write(self.style.SUCCESS('   Datos limpiados correctamente'))
    
    def create_users(self, options):
        """Crea usuarios con diferentes roles evitando duplicados"""
        self.stdout.write(f'👥 Creando {options["users"]} usuarios...')
        
        num_users = options['users']
        num_admins = int(num_users * options['admin_percentage'])
        num_guests = int(num_users * options['guest_percentage'])
        num_regular = num_users - num_admins - num_guests
        
        created_count = 0
        
        # Crear administradores
        admin_counter = 1
        while len([u for u in self.created_users if u.role == 'admin']) < num_admins and admin_counter < 100:
            username = f"admin_{admin_counter}"
            email = f"admin_{admin_counter}@example.com"
            
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password="admin123",
                        first_name=self.fake.first_name(),
                        last_name=self.fake.last_name(),
                        role='admin',
                        is_staff=True,
                        is_active=True
                    )
                    self.created_users.append(user)
                    self.stdout.write(f"   ✓ Admin: {user.username}")
                    created_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   Error creando admin {username}: {e}"))
            admin_counter += 1
        
        # Crear invitados
        guest_counter = 1
        while len([u for u in self.created_users if u.role == 'guest']) < num_guests and guest_counter < 100:
            username = f"guest_{guest_counter}"
            email = f"guest_{guest_counter}@example.com"
            
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password="guest123",
                        first_name=self.fake.first_name(),
                        last_name=self.fake.last_name(),
                        role='guest',
                        is_active=True
                    )
                    self.created_users.append(user)
                    self.stdout.write(f"   ✓ Guest: {user.username}")
                    created_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   Error creando guest {username}: {e}"))
            guest_counter += 1
        
        # Crear usuarios regulares
        user_counter = 1
        while len([u for u in self.created_users if u.role == 'user']) < num_regular and user_counter < 100:
            username = f"user_{user_counter}"
            email = f"user_{user_counter}@example.com"
            
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password="user123",
                        first_name=self.fake.first_name(),
                        last_name=self.fake.last_name(),
                        role='user',
                        is_active=True
                    )
                    self.created_users.append(user)
                    created_count += 1
                    if created_count % 10 == 0:
                        self.stdout.write(f"   ✓ Creados {created_count}/{num_users} usuarios")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   Error creando user {username}: {e}"))
            user_counter += 1
        
        # Si no se pudieron crear suficientes usuarios nuevos, usar algunos existentes
        if len(self.created_users) < num_users:
            needed = num_users - len(self.created_users)
            existing_users = User.objects.exclude(id__in=[u.id for u in self.created_users]).filter(is_active=True)[:needed]
            self.created_users.extend(existing_users)
            self.stdout.write(self.style.WARNING(f'   Usando {len(existing_users)} usuarios existentes para completar'))
        
        self.stdout.write(self.style.SUCCESS(f'   Total usuarios disponibles: {len(self.created_users)}'))
    
    def load_topics(self):
        """Carga todos los temas de la base de datos"""
        self.stdout.write('📚 Cargando temas...')
        
        topics_data = get_topics(include_predefined=True, force_refresh=True)
        
        # Aplanar la jerarquía para obtener todas las combinaciones
        for main_topic in topics_data:
            for sub_topic in main_topic['sub_topics']:
                for specific_topic in sub_topic['specific_topics']:
                    self.topics.append({
                        'main': main_topic['name'],
                        'sub': sub_topic['name'],
                        'specific': specific_topic
                    })
        
        self.stdout.write(self.style.SUCCESS(f'   Total temas encontrados: {len(self.topics)}'))
        
        # Mostrar algunos ejemplos
        if self.topics:
            self.stdout.write('   Ejemplo de temas:')
            for topic in self.topics[:3]:
                self.stdout.write(f'      - {topic["main"]} > {topic["sub"]} > {topic["specific"]}')
    
    def create_tests(self, options):
        """Crea tests basados en los temas"""
        if not self.topics:
            self.stdout.write(self.style.WARNING('   No hay temas para crear tests'))
            return
            
        self.stdout.write(f'📝 Creando tests...')
        
        # Parsear fechas
        start_date = datetime.strptime(options['test_start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(options['test_end_date'], '%Y-%m-%d')
        
        # Obtener administradores (o cualquier usuario si no hay admins)
        admin_users = [u for u in self.created_users if u.role == 'admin']
        if not admin_users:
            admin_users = self.created_users
            self.stdout.write(self.style.WARNING('   No hay administradores, usando usuarios regulares como creadores'))
        
        tests_created = 0
        levels = ['Principiante', 'Intermedio', 'Avanzado']
        
        for topic_idx, topic in enumerate(self.topics):
            for i in range(options['tests_per_topic']):
                # Verificar si ya existe un test similar para no duplicar
                test_title = f"{topic['specific']} - Nivel {levels[i % len(levels)]}"
                
                if Test.objects.filter(title=test_title, main_topic=topic['main']).exists():
                    self.stdout.write(f"   ⏭️  Test ya existe: {test_title}")
                    continue
                
                # Fecha aleatoria entre start_date y end_date
                random_days = random.randint(0, (end_date - start_date).days)
                created_at = start_date + timedelta(days=random_days)
                
                try:
                    test = Test.objects.create(
                        title=test_title,
                        description=self.fake.paragraph(nb_sentences=3),
                        main_topic=topic['main'],
                        sub_topic=topic['sub'],
                        specific_topic=topic['specific'],
                        level=levels[i % len(levels)],
                        created_by=random.choice(admin_users),
                        created_at=created_at,
                        updated_at=created_at,
                        is_active=True
                    )
                    self.created_tests.append(test)
                    tests_created += 1
                    
                    if tests_created % 20 == 0:
                        self.stdout.write(f"   ✓ Creados {tests_created} tests")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   Error creando test {test_title}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'   Total tests creados: {len(self.created_tests)}'))
    
    def create_questions_and_answers(self, options):
        """Crea preguntas y respuestas para cada test"""
        if not self.created_tests:
            self.stdout.write(self.style.WARNING('   No hay tests para crear preguntas'))
            return
            
        self.stdout.write(f'❓ Creando preguntas y respuestas...')
        
        questions_per_test = max(3, options['questions_per_test'])
        answers_per_question = max(2, options['answers_per_question'])
        
        total_questions = 0
        total_answers = 0
        
        for test_idx, test in enumerate(self.created_tests):
            # Verificar si el test ya tiene preguntas
            if test.questions.exists():
                self.stdout.write(f"   ⏭️  Test '{test.title}' ya tiene preguntas, saltando")
                continue
                
            # Crear preguntas para el test
            for q_num in range(questions_per_test):
                question = Question.objects.create(
                    test=test,
                    question_text=self.generate_question_text(test, q_num)
                )
                total_questions += 1
                
                # Crear respuestas para la pregunta
                correct_index = random.randint(0, answers_per_question - 1)
                
                for a_num in range(answers_per_question):
                    is_correct = (a_num == correct_index)
                    answer = Answer.objects.create(
                        question=question,
                        answer_text=self.generate_answer_text(question, a_num, is_correct),
                        is_correct=is_correct
                    )
                    total_answers += 1
            
            if (test_idx + 1) % 10 == 0:
                self.stdout.write(f"   ✓ Procesados {test_idx + 1}/{len(self.created_tests)} tests")
        
        self.stdout.write(self.style.SUCCESS(f'   Total preguntas: {total_questions}, Total respuestas: {total_answers}'))
    
    def generate_question_text(self, test, question_num):
        """Genera texto de pregunta realista"""
        templates = [
            f"¿Cuál es el concepto fundamental de {test.specific_topic}?",
            f"Explique cómo funciona {test.specific_topic} en el contexto de {test.main_topic}",
            f"¿Cuál de las siguientes afirmaciones sobre {test.specific_topic} es correcta?",
            f"En {test.sub_topic}, ¿qué relación tiene {test.specific_topic} con otros conceptos?",
            f"¿Qué herramienta/método se utiliza para resolver problemas de {test.specific_topic}?",
            f"¿Cuál es el error más común al aprender {test.specific_topic}?",
            f"¿Cómo se aplica {test.specific_topic} en casos prácticos de {test.main_topic}?",
            f"¿Qué característica distingue a {test.specific_topic} de otros temas similares?",
            f"¿Cuál es el resultado esperado al aplicar {test.specific_topic} correctamente?",
            f"¿Qué requisitos previos son necesarios para entender {test.specific_topic}?"
        ]
        return random.choice(templates)
    
    def generate_answer_text(self, question, answer_num, is_correct):
        """Genera texto de respuesta realista"""
        if is_correct:
            correct_templates = [
                "La respuesta correcta es esta opción por las siguientes razones...",
                "Esta es la definición estándar según la literatura del tema.",
                "Correcto. Esta opción describe exactamente el concepto.",
                "Sí, esta es la respuesta correcta que cumple con todos los criterios.",
                "Así es. Esta es la solución más apropiada en este contexto."
            ]
            return random.choice(correct_templates)
        else:
            incorrect_templates = [
                "Esta es una confusión común pero incorrecta.",
                "No, esta opción no refleja correctamente el concepto.",
                "Esta respuesta sería válida en otro contexto pero no aquí.",
                "Cuidado: esta es una falacia frecuente en este tema.",
                "Incorrecto. Revisa la definición básica del concepto."
            ]
            return random.choice(incorrect_templates)
    
    def create_results(self, options):
        """Crea resultados para los usuarios"""
        if not self.created_users or not self.created_tests:
            self.stdout.write(self.style.WARNING('   No hay usuarios o tests para crear resultados'))
            return
            
        self.stdout.write(f'📊 Creando resultados...')
        
        results_per_user = options['results_per_user']
        incomplete_percentage = options['incomplete_percentage']
        abandoned_percentage = options['abandoned_percentage']
        completed_percentage = 1 - incomplete_percentage - abandoned_percentage
        
        total_results = 0
        completed_count = 0
        abandoned_count = 0
        incomplete_count = 0
        
        for user_idx, user in enumerate(self.created_users[:20]):  # Limitar a 20 usuarios para no sobrecargar
            # Número de resultados para este usuario
            num_results = random.randint(1, results_per_user)
            available_tests = random.sample(self.created_tests, min(num_results, len(self.created_tests)))
            
            for test in available_tests:
                # Determinar status basado en porcentajes
                rand = random.random()
                if rand < completed_percentage:
                    status = 'completed'
                    completed_count += 1
                elif rand < completed_percentage + abandoned_percentage:
                    status = 'abandoned'
                    abandoned_count += 1
                else:
                    status = 'in_progress'
                    incomplete_count += 1
                
                # Generar fecha de inicio (posterior a la creación del test)
                min_start = test.created_at
                max_start = timezone.now() if test.created_at < timezone.now() else test.created_at + timedelta(days=1)
                
                if min_start >= max_start:
                    started_at = min_start
                else:
                    random_seconds = random.randint(0, int((max_start - min_start).total_seconds()))
                    started_at = min_start + timedelta(seconds=random_seconds)
                
                # Generar respuestas
                questions = list(test.questions.all())
                if not questions:
                    continue
                
                answers_dict = {}
                correct_count = 0
                wrong_count = 0
                
                # Determinar cuántas preguntas responder según el status
                if status == 'completed':
                    num_answered = len(questions)
                elif status == 'abandoned':
                    num_answered = random.randint(1, max(1, len(questions) // 2))
                else:  # in_progress
                    num_answered = random.randint(1, max(1, len(questions) - 1))
                
                # Seleccionar preguntas a responder
                answered_questions = random.sample(questions, min(num_answered, len(questions)))
                
                for question in answered_questions:
                    answers = list(question.answers.all())
                    if answers:
                        selected_answer = random.choice(answers)
                        answers_dict[str(question.id)] = selected_answer.id
                        
                        if selected_answer.is_correct:
                            correct_count += 1
                        else:
                            wrong_count += 1
                
                # Calcular tiempo tomado (15-60 segundos por pregunta respondida)
                time_taken = num_answered * random.randint(15, 60)
                
                try:
                    # Crear resultado
                    result = Result.objects.create(
                        user=user,
                        test=test,
                        correct_answers=correct_count,
                        wrong_answers=wrong_count,
                        time_taken=time_taken,
                        status=status,
                        answers=answers_dict,
                        started_at=started_at,
                        updated_at=started_at + timedelta(seconds=time_taken) if status == 'completed' else started_at
                    )
                    total_results += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   Error creando resultado: {e}"))
            
            if (user_idx + 1) % 5 == 0:
                self.stdout.write(f"   ✓ Procesados {user_idx + 1}/{min(20, len(self.created_users))} usuarios")
        
        self.stdout.write(self.style.SUCCESS(
            f'   Resultados creados: {total_results} '
            f'(Completados: {completed_count}, Abandonados: {abandoned_count}, En progreso: {incomplete_count})'
        ))
    
    def show_statistics(self):
        """Muestra estadísticas finales"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📈 ESTADÍSTICAS FINALES'))
        self.stdout.write('='*60)
        
        # Usuarios
        total_users = User.objects.count()
        admins = User.objects.filter(role='admin').count()
        guests = User.objects.filter(role='guest').count()
        regular = User.objects.filter(role='user').count()
        
        self.stdout.write(f'\n👥 Usuarios: {total_users}')
        self.stdout.write(f'   - Administradores: {admins}')
        self.stdout.write(f'   - Invitados: {guests}')
        self.stdout.write(f'   - Regulares: {regular}')
        
        # Tests
        total_tests = Test.objects.count()
        active_tests = Test.objects.filter(is_active=True).count()
        
        self.stdout.write(f'\n📝 Tests: {total_tests}')
        self.stdout.write(f'   - Activos: {active_tests}')
        
        if total_tests > 0:
            # Tests por nivel
            for level in ['Principiante', 'Intermedio', 'Avanzado']:
                count = Test.objects.filter(level=level).count()
                self.stdout.write(f'   - {level}: {count}')
        
        # Preguntas y respuestas
        total_questions = Question.objects.count()
        total_answers = Answer.objects.count()
        
        self.stdout.write(f'\n❓ Contenido:')
        self.stdout.write(f'   - Preguntas: {total_questions}')
        self.stdout.write(f'   - Respuestas: {total_answers}')
        if total_questions > 0:
            self.stdout.write(f'   - Promedio respuestas/pregunta: {total_answers/total_questions:.1f}')
        
        # Resultados
        total_results = Result.objects.count()
        if total_results > 0:
            completed = Result.objects.filter(status='completed').count()
            abandoned = Result.objects.filter(status='abandoned').count()
            in_progress = Result.objects.filter(status='in_progress').count()
            
            self.stdout.write(f'\n📊 Resultados: {total_results}')
            self.stdout.write(f'   - Completados: {completed} ({completed/total_results*100:.1f}%)')
            self.stdout.write(f'   - Abandonados: {abandoned} ({abandoned/total_results*100:.1f}%)')
            self.stdout.write(f'   - En progreso: {in_progress} ({in_progress/total_results*100:.1f}%)')
            
            # Score promedio - calcular manualmente ya que score_percentage es una property
            completed_results = Result.objects.filter(status='completed')
            if completed_results.exists():
                total_score = 0
                for result in completed_results:
                    total_score += result.score_percentage
                avg_score = total_score / completed_results.count()
                self.stdout.write(f'   - Score promedio (completados): {avg_score:.1f}%')
        else:
            self.stdout.write(f'\n📊 Resultados: 0')
        
        # Temas más usados
        if total_tests > 0:
            self.stdout.write(f'\n🏷️  Topics más usados:')
            from django.db import models
            top_topics = Test.objects.values('main_topic', 'sub_topic', 'specific_topic')\
                .annotate(count=models.Count('id'))\
                .order_by('-count')[:5]
            
            for topic in top_topics:
                self.stdout.write(f'   - {topic["specific_topic"]}: {topic["count"]} tests')
        
        self.stdout.write('\n' + '='*60)