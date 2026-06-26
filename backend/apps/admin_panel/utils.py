# apps/system_config/utils.py
from django.conf import settings

class SystemConfigManager:
    @staticmethod
    def get_all():
        """Obtener todas las configuraciones del sistema"""
        return settings.SYSTEM_CONFIG
    
    @staticmethod
    def get(key, default=None):
        """Obtener una configuración específica"""
        return getattr(settings.SYSTEM_CONFIG, key, default)
    
    @staticmethod
    def to_dict():
        """Convertir a diccionario para usar en APIs"""
        config = settings.SYSTEM_CONFIG
        if hasattr(config, 'to_dict'):
            return config.to_dict()
        return {key: getattr(config, key) for key in dir(config) if not key.startswith('_')}