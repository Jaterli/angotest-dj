# shared/commands/load_predefined_topics.py
from django.core.management.base import BaseCommand
from shared.models import insert_or_update_topic

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
        ]
        
        for main, sub, specific in predefined_topics:
            insert_or_update_topic(main, sub, specific, is_predefined=True)
            self.stdout.write(f"Created: {main} > {sub} > {specific}")
        
        self.stdout.write(self.style.SUCCESS("Predefined topics loaded successfully"))