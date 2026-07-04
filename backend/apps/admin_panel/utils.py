# apps/system_config/utils.py
from django.conf import settings
from typing import Optional

class SystemConfigManager:
    @staticmethod
    def get_all():
        """Obtener todas las configuraciones del sistema"""
        return settings.SYSTEM_CONFIG
    
    
    @staticmethod
    def get_value(key, default: Optional[int] = None) -> int:
        """
        Versión explícita que muestra claramente la prioridad.
        """
        # 1. Buscar en DB
        try:
            from apps.admin_panel.models import SystemConfig
            config = SystemConfig.objects.get(key=key)
            return int(config.value)
        except (SystemConfig.DoesNotExist, ValueError, TypeError):
            pass
       
        # 2. Buscar en settings
        try:
            value = settings.SYSTEM_CONFIG.get(key)
            if value is not None:
                return int(value)
        except (AttributeError, ValueError, TypeError):
            pass  # Error en settings, continuar
        
        # 3. Usar default
        return default if default is not None else 1

    @staticmethod
    def to_dict():
        """Convertir a diccionario para usar en APIs"""
        config = settings.SYSTEM_CONFIG
        if hasattr(config, 'to_dict'):
            return config.to_dict()
        return {key: getattr(config, key) for key in dir(config) if not key.startswith('_')}