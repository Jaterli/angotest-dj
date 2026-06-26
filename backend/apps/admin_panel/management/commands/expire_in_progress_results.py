# apps/admin_panel/management/commands/expire_in_progress_results.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from datetime import timedelta
import logging

from apps.results.models import Result
from apps.admin_panel.models import SystemConfig

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Marca los resultados in_progress como expired si superan los días configurados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la ejecución sin hacer cambios en la base de datos',
        )
        parser.add_argument(
            '--days',
            type=int,
            help='Número de días para considerar expirados (sobrescribe la configuración)',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        days_override = options.get('days')

        # Obtener el número de días de expiración
        expire_days = self._get_expire_days(days_override)

        if not expire_days or expire_days <= 0:
            self.stdout.write(
                self.style.WARNING(
                    f'MARK_IN_PROGRESS_AS_EXPIRED_AFTER_DAYS no configurado o inválido: {expire_days}. '
                    'No se realizará ninguna acción.'
                )
            )
            return

        self.stdout.write(f'Expirando resultados in_progress con más de {expire_days} días de antigüedad')

        # Calcular la fecha límite
        cutoff_date = timezone.now() - timedelta(days=expire_days)

        # Buscar resultados in_progress que excedan el límite
        expired_results = Result.objects.filter(
            status='in_progress',
            updated_at__lt=cutoff_date
        )

        count = expired_results.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No hay resultados in_progress para expirar'))
            return

        self.stdout.write(f'Se encontraron {count} resultados in_progress para expirar')

        if dry_run:
            self.stdout.write(self.style.WARNING('*** MODO DRY-RUN - No se realizarán cambios ***'))
            # Mostrar algunos ejemplos
            sample = expired_results[:10]
            for result in sample:
                self.stdout.write(
                    f'  - Result ID: {result.id}, Usuario: {result.user.username}, '
                    f'Test: {result.test.title}, Updated: {result.updated_at}'
                )
            if count > 10:
                self.stdout.write(f'  ... y {count - 10} más')
            return

        # Actualizar los resultados
        try:
            with transaction.atomic():
                updated = expired_results.update(
                    status='expired',
                    updated_at=timezone.now()
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Se actualizaron {updated} resultados a "expired"')
                )
                
                # Log de la operación
                logger.info(
                    f'Expired {updated} in_progress results older than {expire_days} days '
                    f'(cutoff: {cutoff_date})'
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al actualizar resultados: {str(e)}')
            )
            logger.error(f'Error expiring results: {str(e)}')
            raise

    def _get_expire_days(self, days_override=None):
        """
        Obtiene el número de días de expiración con prioridad:
        1. Sobrescritura por línea de comandos
        2. Valor en la base de datos (SystemConfig)
        3. Valor en settings.SYSTEM_CONFIG
        """
        # 1. Sobrescritura por línea de comandos
        if days_override is not None and days_override > 0:
            self.stdout.write(f'Usando días desde línea de comandos: {days_override}')
            return days_override

        # 2. Valor en la base de datos (SystemConfig)
        try:
            config = SystemConfig.objects.filter(key='MARK_IN_PROGRESS_AS_EXPIRED_AFTER_DAYS').first()
            if config and config.value:
                days = int(config.value)
                if days > 0:
                    self.stdout.write(f'Usando días desde SystemConfig: {days}')
                    return days
        except (SystemConfig.DoesNotExist, ValueError, TypeError):
            pass

        # 3. Valor en settings.SYSTEM_CONFIG
        try:
            days = settings.SYSTEM_CONFIG.get('MARK_IN_PROGRESS_AS_EXPIRED_AFTER_DAYS')
            if days is not None and days > 0:
                self.stdout.write(f'Usando días desde settings.SYSTEM_CONFIG: {days}')
                return days
        except (AttributeError, KeyError, ValueError, TypeError):
            pass

        self.stdout.write(
            self.style.WARNING('No se encontró configuración válida de días de expiración')
        )
        return None