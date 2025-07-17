from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# Configurar OpenAI con la nueva API
client = OpenAI(
    api_key="api-key"
)

# Contexto especializado para análisis canónico
SYSTEM_CONTEXT = """
Eres un asistente experto en análisis estadístico, específicamente en regresión canónica. 
Tu rol es ayudar a usuarios a:
1. Interpretar datos y seleccionar variables apropiadas
2. Explicar resultados de análisis canónico
3. Proporcionar interpretaciones estadísticas claras
4. Sugerir mejores prácticas en análisis multivariante

Mantén respuestas concisas, profesionales y enfocadas en el análisis canónico.
Si no tienes información sobre los datos específicos del usuario, pide que proporcionen más detalles.
Siempre responde de manera amigable y útil.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        chat_history = data.get('history', [])
        analysis_data = data.get('analysisData', {})
        
        print(f"Mensaje recibido: {user_message}")  # Debug
        
        # Construir contexto con información de análisis si está disponible
        context_info = ""
        if analysis_data:
            if 'currentData' in analysis_data and analysis_data['currentData']:
                context_info += f"El usuario tiene {len(analysis_data['currentData'])} registros cargados. "
            if 'currentColumns' in analysis_data and analysis_data['currentColumns']:
                context_info += f"Variables disponibles: {', '.join(analysis_data['currentColumns'])}. "
            if 'analysisResults' in analysis_data and analysis_data['analysisResults']:
                results = analysis_data['analysisResults']
                context_info += f"Análisis completado con correlación canónica principal de {results.get('canonicalCorrelations', [0])[0]:.3f}. "
        
        # Construir mensajes para la API
        messages = [
            {"role": "system", "content": SYSTEM_CONTEXT + " " + context_info}
        ]
        
        # Agregar historial de chat (últimos 10 mensajes)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent_history:
            if isinstance(msg, dict) and 'sender' in msg and 'message' in msg:
                role = "user" if msg['sender'] == 'user' else "assistant"
                messages.append({"role": role, "content": msg['message']})
        
        # Agregar mensaje actual
        messages.append({"role": "user", "content": user_message})
        
        print(f"Enviando {len(messages)} mensajes a OpenAI")  # Debug
        
        # Llamar a OpenAI con la nueva API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        print(f"Respuesta de OpenAI: {bot_response}")  # Debug
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
        
    except Exception as e:
        print(f"Error en chat: {str(e)}")  # Debug
        error_message = str(e)
        
        # Manejar errores específicos de OpenAI
        if "authentication" in error_message.lower():
            return jsonify({
                'success': False,
                'error': 'Error de autenticación con OpenAI. Verifica tu API key.'
            })
        elif "rate_limit" in error_message.lower():
            return jsonify({
                'success': False,
                'error': 'Límite de uso excedido. Intenta más tarde.'
            })
        elif "insufficient_quota" in error_message.lower():
            return jsonify({
                'success': False,
                'error': 'Cuota de OpenAI agotada. Revisa tu cuenta.'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error del servidor: {error_message}'
            })

@app.route('/health')
def health_check():
    """Endpoint para verificar el estado del servidor"""
    try:
        # Verificar si la API key está configurada
        api_key_configured = bool(client.api_key and client.api_key != "tu_api_key_aqui")
        
        return jsonify({
            'status': 'OK', 
            'openai_configured': api_key_configured,
            'api_key_present': bool(client.api_key)
        })
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'error': str(e),
            'openai_configured': False
        })

if __name__ == '__main__':
    # Verificar que la API key esté configurada
    if not client.api_key or client.api_key == "tu_api_key_aqui":
        print("⚠️  ADVERTENCIA: Reemplaza 'tu_api_key_aqui' con tu API key real de OpenAI")
    else:
        print("✅ OpenAI API Key configurada correctamente")
    
    print("🚀 Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)