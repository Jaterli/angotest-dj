# ai_services.py
import json
import os
from groq import Groq
from django.conf import settings
from ..test.models import Test, Question, Answer, Topic

class AITestGenerator:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    def generate_test(self, input_data, user_id):
        """Genera un test usando Groq API"""
        prompt = self._build_prompt(input_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=8000,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        ai_response = json.loads(content)
        
        return self._create_test_from_ai_response(ai_response, input_data, user_id)
    
    def _build_prompt(self, input_data):
        # Construir prompt similar al original en Go
        if input_data.get('generation_mode') == 'prompt':
            # Modo libre
            return f"""
            Genera un test educativo basado en esta descripción:
            {input_data.get('ai_prompt')}
            
            Especificaciones:
            - Nivel: {input_data.get('level')}
            - Número de preguntas: {input_data.get('num_questions')}
            - Opciones por pregunta: {input_data.get('num_answers')}
            """
        else:
            # Modo guiado
            return f"""
            Genera un test educativo sobre:
            - Tema principal: {input_data.get('main_topic')}
            - Subtema: {input_data.get('sub_topic')}
            - Tema específico: {input_data.get('specific_topic')}
            - Nivel: {input_data.get('level')}
            - Número de preguntas: {input_data.get('num_questions')}
            - Opciones por pregunta: {input_data.get('num_answers')}
            """
    
    def _create_test_from_ai_response(self, ai_response, input_data, user_id):
        """Crea el test en BD a partir de la respuesta de IA"""
        test = Test.objects.create(
            title=ai_response.get('title', f"Test de {input_data.get('main_topic', 'IA')}"),
            description=ai_response.get('description', ''),
            main_topic=ai_response.get('main_topic', input_data.get('main_topic', 'General')),
            sub_topic=ai_response.get('sub_topic', input_data.get('sub_topic', 'General')),
            specific_topic=ai_response.get('specific_topic', input_data.get('specific_topic', 'General')),
            level=input_data.get('level'),
            created_by_id=user_id,
            is_active=True
        )
        
        for q_data in ai_response.get('questions', []):
            question = Question.objects.create(
                test=test,
                question_text=q_data.get('question_text')
            )
            
            for a_data in q_data.get('answers', []):
                Answer.objects.create(
                    question=question,
                    answer_text=a_data.get('answer_text'),
                    is_correct=a_data.get('is_correct', False)
                )
        
        return test
    
    def _get_system_prompt(self):
        return """Eres un experto en creación de tests educativos.
        Genera preguntas y respuestas claras y concisas.
        Responde ÚNICAMENTE en formato JSON válido.
        La jerarquía de temas debe seguir: main_topic > sub_topic > specific_topic."""