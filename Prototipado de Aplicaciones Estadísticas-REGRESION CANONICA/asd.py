import matplotlib.pyplot as plt
import numpy as np

# Configurar el estilo del gráfico
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 8))

# Definir colores
azul = '#3498db'
verde = '#2ecc71'

# Crear datos de ejemplo para dos conjuntos de variables
np.random.seed(42)
n_variables = 6

# Conjunto 1 (izquierda) - Variables X
x_positions = np.ones(n_variables) * 1
y_positions_x = np.linspace(1, 6, n_variables)
labels_x = [f'X{i+1}' for i in range(n_variables)]

# Conjunto 2 (derecha) - Variables Y  
x_positions_y = np.ones(n_variables) * 5
y_positions_y = np.linspace(1, 6, n_variables)
labels_y = [f'Y{i+1}' for i in range(n_variables)]

# Dibujar las variables como círculos
# Conjunto X (azul)
scatter_x = ax.scatter(x_positions, y_positions_x, s=500, c=azul, 
                     alpha=0.8, edgecolors='white', linewidth=2, zorder=3)

# Conjunto Y (verde)
scatter_y = ax.scatter(x_positions_y, y_positions_y, s=500, c=verde, 
                     alpha=0.8, edgecolors='white', linewidth=2, zorder=3)

# Agregar etiquetas a las variables
for i, (x, y, label) in enumerate(zip(x_positions, y_positions_x, labels_x)):
    ax.text(x, y, label, ha='center', va='center', fontsize=12, 
            fontweight='bold', color='white', zorder=4)

for i, (x, y, label) in enumerate(zip(x_positions_y, y_positions_y, labels_y)):
    ax.text(x, y, label, ha='center', va='center', fontsize=12, 
            fontweight='bold', color='white', zorder=4)

# Crear líneas de correlación con diferentes intensidades
correlations = np.random.uniform(0.3, 1.0, (n_variables, n_variables))

for i in range(n_variables):
    for j in range(n_variables):
        # Intensidad de la línea basada en la correlación
        alpha = correlations[i, j] * 0.7
        width = correlations[i, j] * 3
        
        # Dibujar línea de conexión
        ax.plot([x_positions[i], x_positions_y[j]], 
                [y_positions_x[i], y_positions_y[j]], 
                color='gray', alpha=alpha, linewidth=width, zorder=1)

# Configurar el gráfico
ax.set_xlim(0, 6)
ax.set_ylim(0, 7)
ax.set_aspect('equal')

# Eliminar ejes y marcos
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Agregar títulos para los conjuntos
ax.text(1, 6.5, 'Conjunto X', ha='center', va='center', fontsize=16, 
        fontweight='bold', color=azul)
ax.text(5, 6.5, 'Conjunto Y', ha='center', va='center', fontsize=16, 
        fontweight='bold', color=verde)

# Título principal
plt.title('Correlación entre Dos Conjuntos de Variables', 
          fontsize=18, fontweight='bold', pad=20)

# Agregar una leyenda explicativa
legend_text = "Grosor de línea = Fuerza de correlación"
ax.text(3, 0.3, legend_text, ha='center', va='center', fontsize=10, 
        style='italic', color='gray')

plt.tight_layout()
plt.show()

# Opcional: Guardar como SVG
# plt.savefig('correlacion_variables.svg', format='svg', bbox_inches='tight')