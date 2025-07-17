import os
from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "secret_key_fallback")

def init_game_state():
    """Initialize the game state with starting items"""
    return {
        'limones': 2,  # par de limones
        'chocolate': 2,  # par de chocolate
        'huevos': 2,  # par de huevos
        'caramelos': 0,
        'total_caramelos': 0  # contador total para estadísticas
    }

@app.route('/')
def index():
    """Main game page"""
    if 'game_state' not in session:
        session['game_state'] = init_game_state()
    
    return render_template('index.html', state=session['game_state'])

@app.route('/reset')
def reset_game():
    """Reset the game to initial state"""
    session['game_state'] = init_game_state()
    flash('¡Juego reiniciado! Comenzando con 3 pares iniciales.', 'success')
    return redirect(url_for('index'))

@app.route('/intercambio_principal', methods=['POST'])
def intercambio_principal():
    """Main exchange: 3 pairs for 1 candy + 2 individual items"""
    if 'game_state' not in session:
        session['game_state'] = init_game_state()
    
    state = session['game_state']
    
    # Verificar que tenemos al menos 3 pares (6 objetos individuales)
    pares_limones = state['limones'] // 2
    pares_chocolate = state['chocolate'] // 2
    pares_huevos = state['huevos'] // 2
    total_pares = pares_limones + pares_chocolate + pares_huevos
    
    if total_pares < 3:
        flash('¡Necesitas al menos 3 pares para realizar este intercambio!', 'error')
        return redirect(url_for('index'))
    
    # Obtener la selección de objetos del formulario
    objeto1 = request.form.get('objeto1')
    objeto2 = request.form.get('objeto2')
    
    if not objeto1 or not objeto2:
        flash('Debes seleccionar 2 objetos individuales para recibir.', 'error')
        return redirect(url_for('index'))
    
    # Quitar 3 pares (6 objetos)
    pares_a_quitar = 3
    
    # Priorizar quitar pares completos
    if pares_limones > 0 and pares_a_quitar > 0:
        pares_quitar = min(pares_limones, pares_a_quitar)
        state['limones'] -= pares_quitar * 2
        pares_a_quitar -= pares_quitar
    
    if pares_chocolate > 0 and pares_a_quitar > 0:
        pares_quitar = min(pares_chocolate, pares_a_quitar)
        state['chocolate'] -= pares_quitar * 2
        pares_a_quitar -= pares_quitar
    
    if pares_huevos > 0 and pares_a_quitar > 0:
        pares_quitar = min(pares_huevos, pares_a_quitar)
        state['huevos'] -= pares_quitar * 2
        pares_a_quitar -= pares_quitar
    
    # Agregar 1 caramelo
    state['caramelos'] += 1
    state['total_caramelos'] += 1
    
    # Agregar los 2 objetos seleccionados
    if objeto1 == 'limon':
        state['limones'] += 1
    elif objeto1 == 'chocolate':
        state['chocolate'] += 1
    elif objeto1 == 'huevo':
        state['huevos'] += 1
    
    if objeto2 == 'limon':
        state['limones'] += 1
    elif objeto2 == 'chocolate':
        state['chocolate'] += 1
    elif objeto2 == 'huevo':
        state['huevos'] += 1
    
    session['game_state'] = state
    
    flash(f'¡Intercambio realizado! Recibiste 1 caramelo y 2 objetos individuales.', 'success')
    return redirect(url_for('index'))

@app.route('/intercambio_caramelo', methods=['POST'])
def intercambio_caramelo():
    """Candy exchange: 1 candy for 3 pairs"""
    if 'game_state' not in session:
        session['game_state'] = init_game_state()
    
    state = session['game_state']
    
    if state['caramelos'] < 1:
        flash('¡No tienes caramelos suficientes para este intercambio!', 'error')
        return redirect(url_for('index'))
    
    # Obtener la selección de pares del formulario
    pares_limones = int(request.form.get('pares_limones', 0))
    pares_chocolate = int(request.form.get('pares_chocolate', 0))
    pares_huevos = int(request.form.get('pares_huevos', 0))
    
    total_pares_solicitados = pares_limones + pares_chocolate + pares_huevos
    
    if total_pares_solicitados != 3:
        flash('Debes seleccionar exactamente 3 pares para recibir.', 'error')
        return redirect(url_for('index'))
    
    # Quitar 1 caramelo
    state['caramelos'] -= 1
    
    # Agregar los pares solicitados
    state['limones'] += pares_limones * 2
    state['chocolate'] += pares_chocolate * 2
    state['huevos'] += pares_huevos * 2
    
    session['game_state'] = state
    
    flash(f'¡Intercambio realizado! Recibiste {total_pares_solicitados} pares por 1 caramelo.', 'success')
    return redirect(url_for('index'))

@app.route('/get_state')
def get_state():
    """API endpoint to get current game state"""
    if 'game_state' not in session:
        session['game_state'] = init_game_state()
    
    return jsonify(session['game_state'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
