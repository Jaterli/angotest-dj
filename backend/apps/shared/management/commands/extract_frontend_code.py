# management/commands/extract_frontend_code.py

import os
import re
from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import fnmatch
import json


class Command(BaseCommand):
    """
    Comando Django para extraer código de archivos frontend (TypeScript, HTML, SCSS/CSS)
    Uso: python manage.py extract_frontend_code [opciones]
    """
    
    help = 'Extrae el contenido de archivos frontend (TypeScript, HTML, CSS/SCSS)'
    
    # Extensiones soportadas
    SUPPORTED_EXTENSIONS = {
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.js': 'JavaScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
    }
    
    # Directorios a ignorar (siempre)
    IGNORE_DIRS = [
        'node_modules',
        'dist',
        'build',
        '.git',
        '.vscode',
        '.idea',
        'coverage',
        '.angular',
        '.cache',
        'tmp',
        'temp',
        'e2e',
        'cypress',
        '.nyc_output',
        'vendor',
        'bower_components',
        'jspm_packages',
        'reset-password',
        'pages',
        'invitation',
        'login',   
        'register',
        'footer',
        'header',
        'services',
    ]
    
    # Archivos a ignorar (siempre)
    IGNORE_FILES = [
        '*.spec.ts',
        '*.test.ts',
        '*.spec.js',
        '*.test.js',
        '*.min.js',
        '*.bundle.js',
        '*.chunk.js',
        'polyfills.ts',
        'polyfills.js',
        'main.ts',
        'main.js',
        'index.ts',
        'index.js',
        'environment.ts',
        'environment.prod.ts',
        'environments.ts',
        '*.d.ts',
        'vendor.ts',
        'vendor.js',
        '*.map',
        '*.json',
        '*.lock',
        '*.log',
        '*.env',
        '*.example',
    ]

    # PATRONES DE RUTA a ignorar (nuevo)
    # Usa sintaxis fnmatch, puede incluir comodines y rutas relativas al frontend
    IGNORE_PATHS = [
        'app/user/',# Ignora todo dentro de app/user/
    ]
    
    # Patrones de archivos importantes por defecto
    DEFAULT_INCLUDE_PATTERNS = [
        '*.component.ts',
        '*.service.ts',
        '*.module.ts',
        '*.directive.ts',
        '*.pipe.ts',
        '*.guard.ts',
        '*.interceptor.ts',
        '*.resolver.ts',
        '*.component.html',
        '*.component.scss',
        '*.component.css',
        '*.component.less',
        'app-routing.module.ts',
        'app.module.ts',
        '*.controller.ts',  # NestJS
        '*.middleware.ts',  # NestJS
        '*.gateway.ts',     # NestJS
    ]
    
    def add_arguments(self, parser):
        """
        Añade argumentos para el comando
        """
        # Grupos de argumentos
        include_group = parser.add_argument_group('Inclusión de archivos')
        exclude_group = parser.add_argument_group('Exclusión de archivos')
        output_group = parser.add_argument_group('Opciones de salida')
        filter_group = parser.add_argument_group('Filtros específicos')
        
        # Argumentos de inclusión
        include_group.add_argument(
            '--include',
            '-i',
            nargs='+',
            help='Archivos específicos a incluir (ej: app.component.ts header.html)'
        )
        
        include_group.add_argument(
            '--include-pattern',
            '-p',
            nargs='+',
            help='Patrones de archivos a incluir (ej: *component.ts *service.ts)'
        )
        
        include_group.add_argument(
            '--include-all',
            action='store_true',
            help='Incluir todos los archivos frontend (excepto ignorados)'
        )
        
        include_group.add_argument(
            '--include-tests',
            '-t',
            action='store_true',
            help='Incluir archivos de tests (.spec.ts, .test.ts)'
        )
        
        include_group.add_argument(
            '--include-assets',
            action='store_true',
            help='Incluir archivos de assets (CSS, SCSS, imágenes, etc.)'
        )
        
        include_group.add_argument(
            '--component',
            '-c',
            type=str,
            help='Extraer solo un componente específico (ej: app-header)'
        )
        
        include_group.add_argument(
            '--module',
            '-m',
            type=str,
            help='Extraer solo módulos específicos (ej: admin, user)'
        )
        
        # Argumentos de exclusión
        exclude_group.add_argument(
            '--exclude',
            '-e',
            nargs='+',
            help='Archivos específicos a excluir'
        )
        
        exclude_group.add_argument(
            '--exclude-pattern',
            '-x',
            nargs='+',
            help='Patrones de archivos a excluir'
        )
        
        # Filtros específicos de frontend
        filter_group.add_argument(
            '--extension',
            '-ext',
            nargs='+',
            choices=['ts', 'html', 'css', 'scss', 'sass', 'less', 'js', 'jsx', 'tsx'],
            help='Extensiones específicas a incluir'
        )
        
        filter_group.add_argument(
            '--min-lines',
            '-l',
            type=int,
            default=0,
            help='Líneas mínimas para considerar un archivo (default: 0)'
        )
        
        filter_group.add_argument(
            '--max-size',
            type=int,
            default=0,
            help='Tamaño máximo en KB para incluir un archivo (0 = sin límite)'
        )
        
        # Argumentos de salida
        output_group.add_argument(
            '--output',
            '-o',
            type=str,
            default='frontend_code_extract.txt',
            help='Nombre del archivo de salida (default: frontend_code_extract.txt)'
        )
        
        output_group.add_argument(
            '--format',
            type=str,
            choices=['txt', 'md', 'json', 'html'],
            default='txt',
            help='Formato de salida: txt, md, json, o html (default: txt)'
        )
        
        output_group.add_argument(
            '--full-path',
            '-f',
            action='store_true',
            help='Mostrar rutas completas en lugar de relativas'
        )
        
        output_group.add_argument(
            '--group-by',
            type=str,
            choices=['type', 'folder', 'module', 'none'],
            default='type',
            help='Agrupar archivos por tipo, carpeta, módulo o ninguno'
        )
        
        # Debug (sin conflicto con -v de Django)
        parser.add_argument(
            '--debug',
            '-d',
            action='store_true',
            help='Mostrar información detallada durante la ejecución'
        )
    
    def handle(self, *args, **options):
        """
        Método principal del comando
        """
        self.verbosity = options.get('verbosity', 1)
        self.debug = options.get('debug', False)
        
        # Detectar directorio frontend
        self.frontend_path = self.detect_frontend_path()
        if not self.frontend_path:
            raise CommandError(
                'No se encontró un directorio de frontend. '
                'Asegúrate de que el proyecto tenga una estructura Angular, React o similar.'
            )
        
        self.output_file = Path(options['output'])
        self.format = options.get('format', 'txt')
        self.full_path = options.get('full_path', False)
        self.min_lines = options.get('min_lines', 0)
        self.max_size = options.get('max_size', 0) * 1024  # Convertir KB a bytes
        self.group_by = options.get('group_by', 'type')
        
        # Configurar inclusiones
        self.include_files = set(options.get('include', []) or [])
        self.include_patterns = options.get('include_pattern', []) or []
        self.include_all = options.get('include_all', False)
        self.include_tests = options.get('include_tests', False)
        self.include_assets = options.get('include_assets', False)
        self.specific_component = options.get('component')
        self.specific_module = options.get('module')
        
        # Configurar extensiones
        self.extensions = options.get('extension', [])
        if self.extensions:
            self.extensions = [f'.{ext}' if not ext.startswith('.') else ext 
                             for ext in self.extensions]
        
        # Configurar exclusiones
        self.exclude_files = set(options.get('exclude', []) or [])
        self.exclude_patterns = options.get('exclude_pattern', []) or []
        
        # Validar configuración
        self.validate_configuration()
        
        # Mensaje de inicio
        if self.verbosity >= 1:
            self.stdout.write(
                self.style.SUCCESS('🚀 Iniciando extracción de código Frontend')
            )
            self.stdout.write(f'📁 Frontend: {self.frontend_path}')
            self.stdout.write(f'🔍 Tipo detectado: {self.detect_framework()}')
            
            if self.specific_component:
                self.stdout.write(f'🎯 Componente específico: {self.specific_component}')
            
            if self.specific_module:
                self.stdout.write(f'📦 Módulo específico: {self.specific_module}')
        
        self.extract_code(options)
    


    def detect_frontend_path(self):
        """
        Detecta el directorio del frontend en el proyecto Django
        """
        # PRIMERO: Buscar en el directorio BASE_DIR (backend)
        base_path = Path(settings.BASE_DIR)
        
        # SEGUNDO: Buscar en el directorio PADRE (donde está backend y frontend)
        parent_path = base_path.parent  # Esto sube un nivel
        
        # Posibles nombres de directorios frontend
        possible_names = [
            'frontend',
            'client',
            'angular',
            'react',
            'vue',
            'front',
            'ui',
            'web',
            'app-frontend',
            'src-frontend',
        ]
        
        # Buscar en el directorio padre primero (donde está el frontend al mismo nivel que backend)
        for name in possible_names:
            if (parent_path / name).exists():
                self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {parent_path / name}'))
                return parent_path / name
        
        # Si no se encuentra en el padre, buscar en BASE_DIR (backend)
        for name in possible_names:
            if (base_path / name).exists():
                self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {base_path / name}'))
                return base_path / name
        
        # Buscar cualquier directorio con package.json, angular.json, etc. en el padre
        for item in parent_path.iterdir():
            if item.is_dir():
                if (item / 'package.json').exists() or \
                (item / 'angular.json').exists() or \
                (item / 'webpack.config.js').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item}'))
                    return item
                if (item / 'src' / 'app').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item / "src"}'))
                    return item / 'src'
                if (item / 'src' / 'main.ts').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item / "src"}'))
                    return item / 'src'
        
        # Buscar cualquier directorio con package.json, angular.json, etc. en BASE_DIR
        for item in base_path.iterdir():
            if item.is_dir():
                if (item / 'package.json').exists() or \
                (item / 'angular.json').exists() or \
                (item / 'webpack.config.js').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item}'))
                    return item
                if (item / 'src' / 'app').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item / "src"}'))
                    return item / 'src'
                if (item / 'src' / 'main.ts').exists():
                    self.stdout.write(self.style.SUCCESS(f'✅ Frontend encontrado en: {item / "src"}'))
                    return item / 'src'
        
        # Verificar si hay un directorio src en la raíz del padre
        if (parent_path / 'src' / 'app').exists():
            return parent_path / 'src'
        
        return None

    def detect_framework(self):
        """
        Detecta el framework frontend utilizado
        """
        if not self.frontend_path:
            return "Desconocido"
        
        # Buscar archivos característicos
        if (self.frontend_path / 'angular.json').exists():
            return "Angular"
        if (self.frontend_path / 'package.json').exists():
            try:
                with open(self.frontend_path / 'package.json', 'r') as f:
                    data = json.load(f)
                    dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    if '@angular/core' in dependencies:
                        return "Angular"
                    if 'react' in dependencies:
                        return "React"
                    if 'vue' in dependencies:
                        return "Vue.js"
                    if 'next' in dependencies:
                        return "Next.js"
                    if 'nuxt' in dependencies:
                        return "Nuxt.js"
            except:
                pass
        
        # Buscar por estructura de directorios
        if (self.frontend_path / 'app' / 'app.component.ts').exists():
            return "Angular"
        if (self.frontend_path / 'components' / 'App.tsx').exists() or \
           (self.frontend_path / 'App.tsx').exists():
            return "React"
        if (self.frontend_path / 'components' / 'App.vue').exists():
            return "Vue.js"
        
        return "Framework desconocido"
    
    def validate_configuration(self):
        """Valida la configuración de inclusión/exclusión"""
        # Si no se especifica nada, usar patrones por defecto
        if not self.include_all and not self.include_files and not self.include_patterns:
            if self.verbosity >= 1:
                self.stdout.write(
                    self.style.WARNING('⚠️ No se especificaron archivos a incluir.')
                )
                self.stdout.write(
                    self.style.WARNING('📝 Usando patrones por defecto para componentes y servicios')
                )
                self.stdout.write(
                    self.style.WARNING('💡 Use --include-all para incluir todos los archivos')
                )
            
            # Usar patrones por defecto
            self.include_patterns = self.DEFAULT_INCLUDE_PATTERNS.copy()
    
    def should_ignore_dir(self, dir_path):
        """Determina si un directorio debe ser ignorado"""
        dir_name = dir_path.name
        
        # Ignorar directorios por nombre (simple)
        if dir_name in self.IGNORE_DIRS:
            return True
        
        # Ignorar directorios ocultos
        if dir_name.startswith('.'):
            return True
        
        # Ignorar por PATRONES DE RUTA
        try:
            rel_path = dir_path.relative_to(self.frontend_path)
            rel_path_str = str(rel_path) + '/'  # Añadir slash para directorios

            for pattern in self.IGNORE_PATHS:
                self.stdout.write(f'Debug: Verificando {rel_path_str} contra patrón {pattern}')

                # 1. Coincidencia exacta con fnmatch (soporta comodines * y ?)
                if fnmatch.fnmatch(rel_path_str, pattern) or fnmatch.fnmatch(rel_path_str, pattern + '/'):
                    self.stdout.write(f'Debug: Ignorando directorio {rel_path_str} por patrón {pattern}')
                    return True

                # 2. Coincidencia sin slash al final (para patrones sin barra)
                if fnmatch.fnmatch(str(rel_path), pattern):
                    self.stdout.write(f'Debug: Ignorando directorio {rel_path_str} por patrón {pattern}')
                    return True

                # 3. NUEVO: el patrón está contenido en la ruta (subcadena)
                #    Esto cubre casos como "app/user/" dentro de "src/app/user/"
                if pattern in rel_path_str:
                    self.stdout.write(f'Debug: Ignorando directorio {rel_path_str} porque contiene el patrón {pattern}')
                    return True

        except ValueError:
            pass      

        # Si es un componente específico...
        if self.specific_component:
            try:
                rel_path = dir_path.relative_to(self.frontend_path)
                if self.specific_component not in str(rel_path):
                    return True
            except ValueError:
                return True
        
        # Si es un módulo específico
        if self.specific_module:
            try:
                rel_path = dir_path.relative_to(self.frontend_path)
                if self.specific_module not in str(rel_path):
                    return True
            except ValueError:
                return True
        
        return False
    
        
    def should_ignore_file(self, file_path):
        """
        Determina si un archivo debe ser ignorado basado en IGNORE_FILES y IGNORE_PATHS
        """
        file_name = file_path.name
        
        # Verificar si el archivo debe ser ignorado por nombre exacto o patrón simple
        if file_name in self.IGNORE_FILES:
            return True
        
        for pattern in self.IGNORE_FILES:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        
        # Verificar si el archivo coincide con algún patrón de ruta
        try:
            rel_path = file_path.relative_to(self.frontend_path)
            rel_path_str = str(rel_path)
            for pattern in self.IGNORE_PATHS:
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
        except ValueError:
            pass
        
        return False
    
    
    def should_include_file(self, file_path):
        """
        Determina si un archivo debe ser incluido en la extracción
        """
        # Verificar si es una extensión soportada
        if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
            return False
        
        # Verificar extensiones específicas
        if self.extensions and file_path.suffix not in self.extensions:
            return False
        
        # Verificar si el archivo está en IGNORE_FILES
        if self.should_ignore_file(file_path):
            return False
        
        # Obtener nombre del archivo y ruta relativa
        file_name = file_path.name
        rel_path = str(file_path.relative_to(self.frontend_path))
        
        # Verificar tamaño máximo
        if self.max_size > 0:
            try:
                file_size = file_path.stat().st_size
                if file_size > self.max_size:
                    return False
            except:
                pass
        
        # 1. VERIFICAR EXCLUSIONES (primero)
        # Excluir por nombre exacto
        if file_name in self.exclude_files:
            return False
        
        # Excluir por patrón
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return False
        
        # Excluir tests si no están habilitados
        if not self.include_tests:
            if '.spec.' in file_name or '.test.' in file_name:
                return False
            if file_name.endswith('.spec.ts') or file_name.endswith('.test.ts'):
                return False
        
        # Excluir assets si no están habilitados
        if not self.include_assets:
            if file_path.suffix in ['.css', '.scss', '.sass', '.less']:
                if 'component' not in file_name:  # Incluir estilos de componentes
                    return False
            
            if file_path.suffix in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']:
                return False
        
        # 2. VERIFICAR INCLUSIONES
        # Si --include-all está activado, incluir todo (excepto exclusiones)
        if self.include_all:
            return True
        
        # Incluir por nombre exacto
        if file_name in self.include_files:
            return True
        
        # Incluir por patrón
        for pattern in self.include_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        
        # Incluir por ruta relativa (patrones completos)
        for pattern in self.include_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        
        # 3. VERIFICAR LÍNEAS MÍNIMAS
        if self.min_lines > 0:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) < self.min_lines:
                        return False
            except Exception as e:
                if self.debug:
                    self.stderr.write(f'Error al leer {file_path}: {e}')
                return False
        
        # Si llegamos aquí, el archivo no coincide con ningún criterio de inclusión
        return False
    
    def extract_file_content(self, file_path):
        """Extrae el contenido de un archivo con metadatos"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.count('\n')
            
            if self.full_path:
                relative_path = str(file_path)
            else:
                try:
                    relative_path = str(file_path.relative_to(self.frontend_path))
                except ValueError:
                    relative_path = str(file_path)
            
            # Obtener estadísticas específicas del frontend
            extension = file_path.suffix
            file_type = self.SUPPORTED_EXTENSIONS.get(extension, 'Unknown')
            
            # Estadísticas específicas
            component_count = 0
            if extension == '.ts' or extension == '.tsx':
                # Contar componentes (decoradores, funciones, clases)
                component_count = len(re.findall(
                    r'@Component|@Directive|@Pipe|@Injectable|@NgModule',
                    content
                ))
            
            html_count = 0
            if extension == '.html':
                # Contar elementos HTML
                html_count = len(re.findall(r'<[^>]+>', content))
                component_count = len(re.findall(r'<app-[^>]+>', content))
            
            return {
                'file_path': relative_path,
                'file_name': file_path.name,
                'extension': extension,
                'file_type': file_type,
                'content': content,
                'lines': lines,
                'component_count': component_count,
                'html_elements': html_count,
                'size_kb': file_path.stat().st_size / 1024,
                'module': self.get_module_name(file_path),
                'component_name': self.get_component_name(file_path),
                'is_test': '.spec.' in file_path.name or '.test.' in file_path.name,
            }
            
        except Exception as e:
            if self.debug:
                self.stderr.write(f'Error al extraer {file_path}: {e}')
            return None
    
    def get_module_name(self, file_path):
        """Obtiene el nombre del módulo a partir de la ruta"""
        try:
            rel_path = file_path.relative_to(self.frontend_path)
            parts = rel_path.parts
            
            # Buscar patrones comunes de módulos
            for part in parts:
                if part.endswith('-module') or part.endswith('_module'):
                    return part
                if part.endswith('modules'):
                    return part
            
            # Buscar carpetas comunes
            for part in parts:
                if part in ['app', 'shared', 'core', 'features']:
                    return part
            
            if len(parts) > 1:
                return parts[0]
        except:
            pass
        return "unknown"
    
    def get_component_name(self, file_path):
        """Intenta extraer el nombre del componente del archivo"""
        name = file_path.stem
        
        # Remover sufijos comunes
        suffixes = ['.component', '.service', '.directive', '.pipe', '.module', 
                   '.guard', '.interceptor', '.resolver', '.controller', '.middleware']
        
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        
        # Remover prefijos comunes
        if name.startswith('app-'):
            name = name[4:]
        
        return name
    
    def get_file_category(self, file_path):
        """Categoriza el archivo para agrupación"""
        name = file_path.name
        
        if '.component.' in name:
            return 'components'
        if '.service.' in name:
            return 'services'
        if '.module.' in name:
            return 'modules'
        if '.directive.' in name:
            return 'directives'
        if '.pipe.' in name:
            return 'pipes'
        if '.guard.' in name:
            return 'guards'
        if '.interceptor.' in name:
            return 'interceptors'
        if '.resolver.' in name:
            return 'resolvers'
        if file_path.suffix == '.html':
            return 'templates'
        if file_path.suffix in ['.css', '.scss', '.sass', '.less']:
            return 'styles'
        if '.spec.' in name or '.test.' in name:
            return 'tests'
        
        return 'other'
    
    def extract_code(self, options):
        """Función principal para extraer código de todos los archivos"""
        
        if self.verbosity >= 1:
            self.stdout.write('-' * 80)
        
        all_files = []
        extracted_data = []
        total_files_scanned = 0
        total_ignored = 0
        
        # Recorrer todos los archivos
        for root, dirs, files in os.walk(self.frontend_path):
            root_path = Path(root)
            
            # Filtrar directorios a ignorar
            dirs[:] = [d for d in dirs if not self.should_ignore_dir(root_path / d)]
            
            # Procesar archivos
            for file in files:
                file_path = root_path / file
                total_files_scanned += 1
                
                if self.should_include_file(file_path):
                    all_files.append(file_path)
                else:
                    total_ignored += 1
        
        if self.verbosity >= 1:
            self.stdout.write(
                self.style.SUCCESS(f'📁 Escaneados {total_files_scanned} archivos')
            )
            self.stdout.write(
                self.style.SUCCESS(f'📄 Encontrados {len(all_files)} archivos relevantes')
            )
            self.stdout.write(
                self.style.WARNING(f'⏭️  Ignorados {total_ignored} archivos')
            )
            self.stdout.write('-' * 80)
        
        if self.debug:
            self.stdout.write('Archivos encontrados:')
            for file_path in all_files:
                self.stdout.write(f'  📄 {file_path.relative_to(self.frontend_path)}')
            self.stdout.write('-' * 80)
        
        # Si no hay archivos, mostrar advertencia
        if not all_files:
            self.stdout.write(
                self.style.WARNING('⚠️ No se encontraron archivos para extraer')
            )
            self.stdout.write('💡 Sugerencias:')
            self.stdout.write('  • Use --include-all para incluir todos los archivos')
            self.stdout.write('  • Use --include-pattern para patrones específicos')
            self.stdout.write('  • Use --include-tests para incluir archivos de pruebas')
            self.stdout.write('  • Use --include-assets para incluir estilos y assets')
            return
        
        # Extraer contenido de cada archivo
        if self.verbosity >= 2:
            self.stdout.write('Extrayendo contenido de archivos...')
        
        for i, file_path in enumerate(all_files, 1):
            if self.debug:
                self.stdout.write(f'Procesando: {file_path.relative_to(self.frontend_path)}')
            elif self.verbosity >= 2 and i % 10 == 0:
                self.stdout.write(f'Progreso: {i}/{len(all_files)} archivos')
            
            data = self.extract_file_content(file_path)
            if data:
                extracted_data.append(data)
        
        if self.verbosity >= 1:
            self.stdout.write('-' * 80)
        
        # Ordenar y agrupar
        extracted_data.sort(key=lambda x: x['file_name'])
        
        # Guardar en archivo según el formato
        if self.format == 'json':
            self.save_as_json(extracted_data, options)
        elif self.format == 'html':
            self.save_as_html(extracted_data, options)
        elif self.format == 'md':
            self.save_as_markdown(extracted_data, options)
        else:
            self.save_as_text(extracted_data, options)
        
        # Mostrar estadísticas finales
        total_lines = sum(d['lines'] for d in extracted_data)
        total_files = len(extracted_data)
        total_components = sum(d['component_count'] for d in extracted_data)
        
        if self.verbosity >= 1:
            self.stdout.write('-' * 80)
            self.stdout.write(self.style.SUCCESS('✅ Extracción completada!'))
            self.stdout.write(f'📊 Archivos procesados: {total_files}')
            self.stdout.write(f'📝 Líneas de código: {total_lines}')
            self.stdout.write(f'🧩 Componentes encontrados: {total_components}')
            self.stdout.write(f'💾 Guardado en: {self.output_file}')
            
            # Mostrar estadísticas por tipo
            self.stdout.write('\n📊 Estadísticas por tipo:')
            type_stats = {}
            for d in extracted_data:
                category = self.get_file_category(Path(d['file_path']))
                type_stats[category] = type_stats.get(category, 0) + 1
            
            for category, count in sorted(type_stats.items()):
                self.stdout.write(f'  📂 {category}: {count} archivos')
            
            self.stdout.write('-' * 80)
    
    def save_as_text(self, extracted_data, options):
        """Guarda los datos en formato TXT"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 100 + "\n")
            f.write(f"🎨 EXTRACCIÓN DE CÓDIGO FRONTEND\n")
            f.write(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📁 Frontend: {self.frontend_path}\n")
            f.write(f"🔍 Framework: {self.detect_framework()}\n")
            f.write(f"📄 Archivos extraídos: {len(extracted_data)}\n")
            f.write(f"📝 Líneas de código: {sum(d['lines'] for d in extracted_data)}\n")
            f.write(f"🧩 Componentes: {sum(d['component_count'] for d in extracted_data)}\n")
            
            if self.specific_component:
                f.write(f"🎯 Componente específico: {self.specific_component}\n")
            if self.specific_module:
                f.write(f"📦 Módulo específico: {self.specific_module}\n")
            if self.include_patterns:
                f.write(f"📌 Patrones incluidos: {', '.join(self.include_patterns)}\n")
            
            f.write("=" * 100 + "\n\n")
            
            # Índice agrupado
            f.write("📑 ÍNDICE DE ARCHIVOS\n")
            f.write("-" * 100 + "\n")
            
            if self.group_by == 'type':
                # Agrupar por tipo
                groups = {}
                for data in extracted_data:
                    category = self.get_file_category(Path(data['file_path']))
                    if category not in groups:
                        groups[category] = []
                    groups[category].append(data)
                
                for category, files in sorted(groups.items()):
                    f.write(f"\n📂 {category.upper()}\n")
                    f.write("-" * 80 + "\n")
                    for data in files:
                        self.write_file_index_entry(f, data)
            
            elif self.group_by == 'module':
                # Agrupar por módulo
                groups = {}
                for data in extracted_data:
                    module = data['module']
                    if module not in groups:
                        groups[module] = []
                    groups[module].append(data)
                
                for module, files in sorted(groups.items()):
                    f.write(f"\n📦 MÓDULO: {module.upper()}\n")
                    f.write("-" * 80 + "\n")
                    for data in files:
                        self.write_file_index_entry(f, data)
            
            else:
                # Lista plana
                for data in extracted_data:
                    self.write_file_index_entry(f, data)
            
            # Contenido de los archivos
            f.write("\n\n" + "=" * 100 + "\n")
            f.write("📝 CONTENIDO DE LOS ARCHIVOS\n")
            f.write("=" * 100 + "\n\n")
            
            for data in extracted_data:
                # Encabezado del archivo
                f.write(f"\n{'=' * 100}\n")
                f.write(f"📄 ARCHIVO: {data['file_path']}\n")
                f.write(f"📝 Líneas: {data['lines']}\n")
                f.write(f"🔤 Tipo: {data['file_type']}\n")
                if data['component_count'] > 0:
                    f.write(f"🧩 Componentes: {data['component_count']}\n")
                if data['html_elements'] > 0:
                    f.write(f"🏷️  Elementos HTML: {data['html_elements']}\n")
                if data['is_test']:
                    f.write("🧪 Archivo de prueba\n")
                f.write(f"📦 Módulo: {data['module']}\n")
                f.write(f"💾 Tamaño: {data['size_kb']:.2f} KB\n")
                f.write(f"{'=' * 100}\n\n")
                
                # Contenido del código
                f.write(data['content'])
                if not data['content'].endswith('\n'):
                    f.write('\n')
                f.write("\n\n")
    
    def write_file_index_entry(self, f, data):
        """Escribe una entrada en el índice"""
        f.write(f"📄 {data['file_path']} ")
        f.write(f"({data['lines']} líneas, ")
        f.write(f"{data['file_type']})")
        if data['component_count'] > 0:
            f.write(f" [🧩 {data['component_count']} componentes]")
        if data['is_test']:
            f.write(" [🧪]")
        f.write("\n")
    
    def save_as_markdown(self, extracted_data, options):
        """Guarda los datos en formato Markdown"""
        md_file = self.output_file.with_suffix('.md')
        
        with open(md_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write(f"# 🎨 Extracción de Código Frontend\n\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Frontend:** `{self.frontend_path}`\n\n")
            f.write(f"**Framework:** `{self.detect_framework()}`\n\n")
            f.write(f"**Archivos extraídos:** {len(extracted_data)}\n\n")
            f.write(f"**Líneas de código:** {sum(d['lines'] for d in extracted_data)}\n\n")
            f.write(f"**Componentes:** {sum(d['component_count'] for d in extracted_data)}\n\n")
            
            if self.specific_component:
                f.write(f"**Componente específico:** `{self.specific_component}`\n\n")
            if self.specific_module:
                f.write(f"**Módulo específico:** `{self.specific_module}`\n\n")
            
            f.write("---\n\n")
            
            # Índice
            f.write("## 📑 Índice de Archivos\n\n")
            
            if self.group_by == 'type':
                groups = {}
                for data in extracted_data:
                    category = self.get_file_category(Path(data['file_path']))
                    if category not in groups:
                        groups[category] = []
                    groups[category].append(data)
                
                for category, files in sorted(groups.items()):
                    f.write(f"### 📂 {category.upper()}\n\n")
                    for data in files:
                        self.write_markdown_index_entry(f, data)
            
            elif self.group_by == 'module':
                groups = {}
                for data in extracted_data:
                    module = data['module']
                    if module not in groups:
                        groups[module] = []
                    groups[module].append(data)
                
                for module, files in sorted(groups.items()):
                    f.write(f"### 📦 Módulo: {module.upper()}\n\n")
                    for data in files:
                        self.write_markdown_index_entry(f, data)
            
            else:
                for data in extracted_data:
                    self.write_markdown_index_entry(f, data)
            
            # Contenido de los archivos
            f.write("\n\n---\n\n")
            f.write("## 📝 Contenido de los Archivos\n\n")
            
            for data in extracted_data:
                # Encabezado del archivo
                f.write(f"\n### 📄 `{data['file_path']}`\n\n")
                f.write(f"**Líneas:** {data['lines']}  \n")
                f.write(f"**Tipo:** `{data['file_type']}`  \n")
                if data['component_count'] > 0:
                    f.write(f"**Componentes:** {data['component_count']}  \n")
                if data['html_elements'] > 0:
                    f.write(f"**Elementos HTML:** {data['html_elements']}  \n")
                if data['is_test']:
                    f.write(f"**🧪 Archivo de prueba**  \n")
                f.write(f"**Módulo:** `{data['module']}`  \n")
                f.write(f"**Tamaño:** {data['size_kb']:.2f} KB  \n")
                f.write("\n")
                
                # Contenido del código
                extension = data['extension'][1:] if data['extension'] else 'txt'
                f.write(f"```{extension}\n")
                f.write(data['content'])
                if not data['content'].endswith('\n'):
                    f.write('\n')
                f.write("```\n\n")
        
        self.output_file = md_file
    
    def write_markdown_index_entry(self, f, data):
        """Escribe una entrada en el índice markdown"""
        f.write(f"- `{data['file_path']}` ")
        f.write(f"({data['lines']} líneas, ")
        f.write(f"{data['file_type']})")
        if data['component_count'] > 0:
            f.write(f" *🧩 {data['component_count']} componentes*")
        if data['is_test']:
            f.write(f" *🧪*")
        f.write("\n")
    
    def save_as_json(self, extracted_data, options):
        """Guarda los datos en formato JSON"""
        json_file = self.output_file.with_suffix('.json')
        
        output_data = {
            'metadata': {
                'frontend_path': str(self.frontend_path),
                'framework': self.detect_framework(),
                'extraction_date': datetime.now().isoformat(),
                'total_files': len(extracted_data),
                'total_lines': sum(d['lines'] for d in extracted_data),
                'total_components': sum(d['component_count'] for d in extracted_data),
                'specific_component': self.specific_component,
                'specific_module': self.specific_module,
                'include_patterns': self.include_patterns,
                'include_tests': self.include_tests,
                'include_assets': self.include_assets,
                'min_lines': self.min_lines,
                'group_by': self.group_by
            },
            'files': extracted_data
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.output_file = json_file
    
    def save_as_html(self, extracted_data, options):
        """Guarda los datos en formato HTML"""
        html_file = self.output_file.with_suffix('.html')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            # Estilos y estructura HTML
            f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracción de Código Frontend</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            margin-top: 20px;
            margin-bottom: 10px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
        }
        .metadata {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .metadata-item {
            display: inline-block;
            margin-right: 20px;
        }
        .metadata-item strong {
            color: #2c3e50;
        }
        .file-section {
            margin: 30px 0;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }
        .file-header {
            background: #3498db;
            color: white;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .file-header:hover {
            background: #2980b9;
        }
        .file-header .file-info {
            flex: 1;
        }
        .file-header .file-stats {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .file-content {
            padding: 20px;
            background: #f8f9fa;
            display: none;
            max-height: 600px;
            overflow: auto;
        }
        .file-content.active {
            display: block;
        }
        .file-content pre {
            margin: 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
        }
        .index {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .index-item {
            padding: 5px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .index-item:last-child {
            border-bottom: none;
        }
        .index-item a {
            color: #3498db;
            text-decoration: none;
        }
        .index-item a:hover {
            text-decoration: underline;
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 5px;
        }
        .tag-test {
            background: #e74c3c;
            color: white;
        }
        .tag-component {
            background: #2ecc71;
            color: white;
        }
        .toggle-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 5px 15px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .toggle-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .code-language {
            background: #e0e0e0;
            padding: 2px 10px;
            border-radius: 3px;
            font-size: 0.8em;
        }
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            .metadata-item {
                display: block;
                margin-right: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
''')
            
            # Encabezado
            f.write(f'''
        <h1>🎨 Extracción de Código Frontend</h1>
        
        <div class="metadata">
            <div class="metadata-item"><strong>📅 Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div class="metadata-item"><strong>📁 Frontend:</strong> {self.frontend_path}</div>
            <div class="metadata-item"><strong>🔍 Framework:</strong> {self.detect_framework()}</div>
            <div class="metadata-item"><strong>📄 Archivos:</strong> {len(extracted_data)}</div>
            <div class="metadata-item"><strong>📝 Líneas:</strong> {sum(d['lines'] for d in extracted_data)}</div>
            <div class="metadata-item"><strong>🧩 Componentes:</strong> {sum(d['component_count'] for d in extracted_data)}</div>
        </div>
''')
            
            if self.specific_component:
                f.write(f'        <p><strong>🎯 Componente específico:</strong> <code>{self.specific_component}</code></p>\n')
            if self.specific_module:
                f.write(f'        <p><strong>📦 Módulo específico:</strong> <code>{self.specific_module}</code></p>\n')
            
            # Estadísticas rápidas
            f.write('''
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Archivos totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Líneas de código</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Componentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Módulos</div>
            </div>
        </div>
'''.format(
                len(extracted_data),
                sum(d['lines'] for d in extracted_data),
                sum(d['component_count'] for d in extracted_data),
                len(set(d['module'] for d in extracted_data))
            ))
            
            # Índice
            f.write('''
        <h2>📑 Índice de Archivos</h2>
        <div class="index">
''')
            
            for data in extracted_data:
                # Crear ID único para el archivo
                file_id = data['file_path'].replace('/', '_').replace('.', '_').replace(' ', '_')
                tags = []
                if data['is_test']:
                    tags.append('<span class="tag tag-test">🧪 Test</span>')
                if data['component_count'] > 0:
                    tags.append(f'<span class="tag tag-component">🧩 {data["component_count"]}</span>')
                
                f.write(f'''
            <div class="index-item">
                <a href="#file-{file_id}">📄 {data['file_path']}</a>
                ({data['lines']} líneas, {data['file_type']})
                {' '.join(tags)}
            </div>
''')
            
            f.write('''
        </div>
''')
            
            # Contenido de los archivos
            f.write('''
        <h2>📝 Contenido de los Archivos</h2>
''')
            
            for data in extracted_data:
                file_id = data['file_path'].replace('/', '_').replace('.', '_').replace(' ', '_')
                tags = []
                if data['is_test']:
                    tags.append('<span class="tag tag-test">🧪 Test</span>')
                if data['component_count'] > 0:
                    tags.append(f'<span class="tag tag-component">🧩 {data["component_count"]}</span>')
                
                f.write(f'''
        <div class="file-section" id="file-{file_id}">
            <div class="file-header" onclick="toggleFile(this)">
                <div class="file-info">
                    <strong>📄 {data['file_path']}</strong>
                    <span class="file-stats">
                        {data['lines']} líneas • {data['file_type']} • {data['size_kb']:.2f} KB
                        {' '.join(tags)}
                    </span>
                </div>
                <button class="toggle-btn">▼</button>
            </div>
            <div class="file-content">
                <pre><code class="{data['extension'][1:]}">{self.escape_html(data['content'])}</code></pre>
            </div>
        </div>
''')
            
            # Script para toggle
            f.write('''
    </div>
    <script>
        function toggleFile(header) {
            const content = header.nextElementSibling;
            const btn = header.querySelector('.toggle-btn');
            if (content.classList.contains('active')) {
                content.classList.remove('active');
                btn.textContent = '▼';
            } else {
                content.classList.add('active');
                btn.textContent = '▲';
            }
        }
        
        // Abrir el primer archivo por defecto
        document.addEventListener('DOMContentLoaded', function() {
            const firstContent = document.querySelector('.file-content');
            if (firstContent) {
                firstContent.classList.add('active');
                const btn = firstContent.previousElementSibling.querySelector('.toggle-btn');
                if (btn) btn.textContent = '▲';
            }
        });
    </script>
</body>
</html>
''')
        
        self.output_file = html_file
    
    def escape_html(self, text):
        """Escapa caracteres HTML especiales en el contenido"""
        import html
        return html.escape(text)