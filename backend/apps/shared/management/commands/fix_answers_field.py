# apps/results/management/commands/fix_answers_field.py
import json
from django.core.management.base import BaseCommand
from apps.results.models import Result

class Command(BaseCommand):
    help = 'Convierte el campo answers de string a dict para todos los Results'

    def handle(self, *args, **options):
        updated = 0
        for result in Result.objects.all():
            if isinstance(result.answers, str):
                try:
                    if result.answers.strip():
                        result.answers = json.loads(result.answers)
                    else:
                        result.answers = {}
                    result.save(update_fields=['answers'])
                    updated += 1
                except json.JSONDecodeError:
                    self.stdout.write(self.style.WARNING(
                        f'Result ID {result.id} tiene JSON inválido, se reseteará a {{}}'
                    ))
                    result.answers = {}
                    result.save(update_fields=['answers'])
                    updated += 1
        self.stdout.write(self.style.SUCCESS(f'✅ {updated} registros actualizados correctamente'))