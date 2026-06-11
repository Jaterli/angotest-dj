# shared/commands/load_predefined_topics.py
from django.core.management.base import BaseCommand
from apps.shared.models import insert_or_update_topic

class Command(BaseCommand):
    help = 'Carga temas predefinidos en la base de datos'
    
    def handle(self, *args, **options):
        predefined_topics = [
            # Matemáticas
            ("Matemáticas", "Álgebra", "Ecuaciones lineales"),
            ("Matemáticas", "Álgebra", "Ecuaciones cuadráticas"),
            ("Matemáticas", "Cálculo", "Derivadas"),
            ("Matemáticas", "Cálculo", "Integrales"),
            ("Matemáticas", "Geometría", "Trigonometría"),

            # Programación
            ("Programación", "Python", "Sintaxis básica"),
            ("Programación", "Python", "Funciones"),
            ("Programación", "Python", "Clases y objetos"),
            ("Programación", "JavaScript", "DOM Manipulation"),
            ("Programación", "JavaScript", "Async/Await"),

            # Ciencias
            ("Ciencias", "Física", "Mecánica clásica"),
            ("Ciencias", "Física", "Termodinámica"),
            ("Ciencias", "Química", "Química orgánica"),
            ("Ciencias", "Biología", "Genética"),

            # Historia
            ("Historia", "Historia Antigua", "Imperio Romano"),
            ("Historia", "Historia Antigua", "Antiguo Egipto"),
            ("Historia", "Historia Moderna", "Revolución Francesa"),
            ("Historia", "Historia Contemporánea", "Segunda Guerra Mundial"),

            # Idiomas
            ("Idiomas", "Inglés", "Gramática básica"),
            ("Idiomas", "Inglés", "Phrasal Verbs"),
            ("Idiomas", "Español", "Tiempos verbales"),
            ("Idiomas", "Francés", "Conversación básica"),

            # Tecnología
            ("Tecnología", "Blockchain", "Smart Contracts"),
            ("Tecnología", "Blockchain", "Tokens ERC-20"),
            ("Tecnología", "Cloud Computing", "AWS Fundamentals"),
            ("Tecnología", "Ciberseguridad", "Seguridad de redes"),

            # Economía
            ("Economía", "Finanzas Personales", "Presupuestos"),
            ("Economía", "Finanzas Personales", "Inversión básica"),
            ("Economía", "Macroeconomía", "Inflación"),
            ("Economía", "Mercados Financieros", "Acciones y bonos"),

            # Arte
            ("Arte", "Pintura", "Acuarela"),
            ("Arte", "Pintura", "Óleo"),
            ("Arte", "Dibujo", "Perspectiva"),
            ("Arte", "Historia del Arte", "Renacimiento"),

            # Música
            ("Música", "Teoría Musical", "Escalas musicales"),
            ("Música", "Teoría Musical", "Acordes"),
            ("Música", "Guitarra", "Acordes básicos"),
            ("Música", "Piano", "Lectura de partituras"),

            # Desarrollo Personal
            ("Desarrollo Personal", "Productividad", "Gestión del tiempo"),
            ("Desarrollo Personal", "Productividad", "Método Pomodoro"),
            ("Desarrollo Personal", "Comunicación", "Hablar en público"),
            ("Desarrollo Personal", "Liderazgo", "Trabajo en equipo"),
        ]
        
        for main, sub, specific in predefined_topics:
            insert_or_update_topic(main, sub, specific, is_predefined=True)
            self.stdout.write(f"Created: {main} > {sub} > {specific}")
        
        self.stdout.write(self.style.SUCCESS("Predefined topics loaded successfully"))