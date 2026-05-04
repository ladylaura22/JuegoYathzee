# Evidencia De Aprendizaje 1: Simulación Estocástica Del Juego Yahtzee

## 📚 Información General

**Actividad:** Actividad 1  
**Curso:** Simulación  
**Título:** Evidencia De Aprendizaje 1: Simulación Estocástica Del Juego Yahtzee  

## 📖 Descripción

Este proyecto implementa una simulación completa del juego de **Yahtzee** utilizando el **Método de Montecarlo** para la toma de decisiones estratégicas automática. 

El programa simula partidas completas entre dos jugadores (controlados por inteligencia artificial) que utilizan una estrategia óptima basada en simulaciones estocásticas para decidir qué dados bloquear en cada turno.

## 🎮 Características Principales

- **Simulación Montecarlo:** Estima el valor esperado de cada posible decisión de bloqueo de dados mediante simulaciones aleatorias.
- **Estrategia Automática:** Los jugadores utilizan IA Montecarlo para elegir las mejores acciones en tiempo real.
- **Juego Completo:** Simula todas las 13 rondas de una partida de Yahtzee.
- **Estadísticas Detalladas:** Proporciona análisis de los resultados incluyendo distribuciones, promedios y yahtzees obtenidos.
- **Reproducibilidad:** Incluye semilla configurable para reproducir resultados (para propósitos de análisis académico).

## 🛠️ Funcionalidades Implementadas

### Núcleo de Montecarlo
- `lanzar_dado()`: Genera valores aleatorios uniformes en [1, 6]
- `lanzar_dados()`: Relanza dados no bloqueados
- `valor_esperado_mascara()`: Estima por Montecarlo el valor esperado de una estrategia de bloqueo

### Cálculo de Puntuación
- Validación de todas las categorías de Yahtzee
- Cálculo automático de puntos según las reglas del juego
- Selección inteligente de la mejor categoría disponible

### Gestión del Juego
- Sistema de turnos automáticos con estrategia Montecarlo
- Seguimiento de puntuaciones jugador por jugador
- Determinación del ganador con marcador final

## 📊 Parámetros Configurables

```python
SIMS_POR_MASCARA = 300   # Simulaciones por máscara de bloqueo (precisión)
SEED = 42                # Semilla para reproducibilidad (None = aleatorio)
```

## 🚀 Ejecución

Para ejecutar la simulación:

```bash
python main.py
```

## 📋 Salida del Programa

El programa genera:

1. **Detalles de cada ronda:** Tiradas, dados bloqueados y categorías seleccionadas
2. **Marcador final:** Tabla comparativa de puntos por categoría
3. **Estadísticas Montecarlo:**
   - Total de dados lanzados
   - Promedio observado (comparado con el teórico de 3.5)
   - Distribución de frecuencias de cada cara
   - Contador de Yahtzees por jugador

## 📚 Categorías de Yahtzee Implementadas

- Unos, Doses, Treses, Cuatros, Cincos, Seises
- Trío (3 iguales)
- Póker (4 iguales)
- Full House (3 + 2 iguales)
- Escalera Menor (4 consecutivos)
- Escalera Mayor (5 consecutivos)
- Yahtzee (5 iguales) - 50 puntos
- Oportunidad (suma total)

## 🔬 Propósito Académico

Esta actividad demuestra:
- La aplicación del **Método de Montecarlo** en la toma de decisiones
- La estimación de valores esperados mediante simulaciones estocásticas
- La optimización de estrategias en juegos con componentes aleatorios
- El análisis estadístico de resultados simulados

## ✨ Autor
LADY LAURA OLMOS

JORGE ANDRÉS HERNANDEZ

JUAN FELIPE PARRA

Curso de Simulación - Evidencia de Aprendizaje 1

