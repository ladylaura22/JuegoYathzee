
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# ───────────────────────────────────────────────────────────
# PARÁMETROS MONTECARLO
# ───────────────────────────────────────────────────────────
SIMS_POR_MASCARA = 300   # Simulaciones por máscara de bloqueo
SEED = 42                # Semilla para reproducibilidad (None = aleatorio)

if SEED is not None:
    random.seed(SEED)

# ───────────────────────────────────────────────────────────
# CATEGORIAS
# ───────────────────────────────────────────────────────────
CATEGORIAS = [
    "unos", "doses", "treses", "cuatros", "cincos", "seises",
    "trio", "poker", "full_house", "escalera_menor",
    "escalera_mayor", "yahtzee", "oportunidad"
]

NOMBRE = {
    "unos": "Unos", "doses": "Doses", "treses": "Treses",
    "cuatros": "Cuatros", "cincos": "Cincos", "seises": "Seises",
    "trio": "Trio", "poker": "Poker", "full_house": "Full House",
    "escalera_menor": "Escalera Menor", "escalera_mayor": "Escalera Mayor",
    "yahtzee": "Yahtzee", "oportunidad": "Oportunidad"
}

CARAS = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}

# ───────────────────────────────────────────────────────────
# NUCLEO MONTECARLO
# ───────────────────────────────────────────────────────────
def lanzar_dado() -> int:
    """Genera un entero uniforme en [1, 6]. Nucleo del metodo Montecarlo."""
    return random.randint(1, 6)

def lanzar_dados(valores: List[int], bloqueados: List[bool]) -> None:
    """Relanza in-place los dados no bloqueados."""
    for i, bloqueado in enumerate(bloqueados):
        if not bloqueado:
            valores[i] = lanzar_dado()

def tiene_secuencia(valores: List[int], largo: int) -> bool:
    """Verifica si existe una secuencia consecutiva de longitud 'largo'."""
    unicos = sorted(set(valores))
    if not unicos:
        return False
    maximo = actual = 1
    for i in range(1, len(unicos)):
        if unicos[i] == unicos[i - 1] + 1:
            actual += 1
            maximo = max(maximo, actual)
        else:
            actual = 1
    return maximo >= largo

# ───────────────────────────────────────────────────────────
# CALCULO DE PUNTUACION
# ───────────────────────────────────────────────────────────
def calcular_puntuacion(categoria: str, dados: List[int]) -> int:
    conteo = Counter(dados)
    frecuencias = list(conteo.values())
    total = sum(dados)

    if categoria in ("unos", "doses", "treses", "cuatros", "cincos", "seises"):
        num = CATEGORIAS.index(categoria) + 1
        return conteo.get(num, 0) * num
    if categoria == "trio":
        return total if any(f >= 3 for f in frecuencias) else 0
    if categoria == "poker":
        return total if any(f >= 4 for f in frecuencias) else 0
    if categoria == "full_house":
        return 25 if (2 in frecuencias and 3 in frecuencias) else 0
    if categoria == "escalera_menor":
        return 30 if tiene_secuencia(dados, 4) else 0
    if categoria == "escalera_mayor":
        return 40 if tiene_secuencia(dados, 5) else 0
    if categoria == "yahtzee":
        return 50 if any(f == 5 for f in frecuencias) else 0
    if categoria == "oportunidad":
        return total
    return 0

def mejor_categoria(dados: List[int], disponibles: List[str]) -> Tuple[str, int]:
    """Devuelve (categoria, puntos) con la mayor puntuacion posible."""
    mejor_cat, mejor_pts = None, -1
    for cat in disponibles:
        pts = calcular_puntuacion(cat, dados)
        if pts > mejor_pts:
            mejor_pts = pts
            mejor_cat = cat
    return mejor_cat, mejor_pts

# ───────────────────────────────────────────────────────────
# ESTRATEGIA MONTECARLO
# ───────────────────────────────────────────────────────────
def generar_mascaras() -> List[List[bool]]:
    """Genera las 32 mascaras posibles de bloqueo para 5 dados."""
    return [[(m >> i) & 1 == 1 for i in range(5)] for m in range(32)]

def valor_esperado_mascara(
    valores: List[int],
    mascara: List[bool],
    tiradas_restantes: int,
    disponibles: List[str],
    sims: int
) -> float:
    """
    Estima por Montecarlo el valor esperado si se bloquean los dados segun 'mascara'
    y se relanza el resto 'tiradas_restantes' veces mas.
    """
    if tiradas_restantes <= 0:
        _, pts = mejor_categoria(valores, disponibles)
        return float(pts)

    no_bloqueados = [i for i, b in enumerate(mascara) if not b]
    total = 0.0
    for _ in range(sims):
        temp = valores[:]
        for _ in range(tiradas_restantes):
            for i in no_bloqueados:
                temp[i] = lanzar_dado()
        _, pts = mejor_categoria(temp, disponibles)
        total += pts
    return total / sims if sims > 0 else 0.0

def elegir_mascara_montecarlo(
    valores: List[int],
    tiradas_restantes: int,
    disponibles: List[str],
    sims: int = SIMS_POR_MASCARA
) -> List[bool]:
    """Devuelve la mascara de bloqueo con mayor valor esperado estimado."""
    mejor_mascara = None
    mejor_ev = -1.0
    for mascara in generar_mascaras():
        ev = valor_esperado_mascara(valores, mascara, tiradas_restantes - 1, disponibles, sims)
        if ev > mejor_ev:
            mejor_ev = ev
            mejor_mascara = mascara
    return mejor_mascara

# ───────────────────────────────────────────────────────────
# ESTRUCTURAS DE DATOS
# ───────────────────────────────────────────────────────────
@dataclass
class Jugador:
    nombre: str
    puntuaciones: Dict[str, Optional[int]] = field(
        default_factory=lambda: {c: None for c in CATEGORIAS}
    )
    total: int = 0
    yahtzees: int = 0

    def disponibles(self) -> List[str]:
        return [c for c, v in self.puntuaciones.items() if v is None]

    def registrar(self, categoria: str, puntos: int) -> None:
        self.puntuaciones[categoria] = puntos
        self.total = sum(v for v in self.puntuaciones.values() if v is not None)
        if categoria == "yahtzee" and puntos == 50:
            self.yahtzees += 1


@dataclass
class EstadisticasJuego:
    total_lanzamientos: int = 0
    histograma: Counter = field(default_factory=Counter)

    def registrar(self, valores: List[int], bloqueados: List[bool]) -> None:
        activos = [v for v, b in zip(valores, bloqueados) if not b]
        self.total_lanzamientos += len(activos)
        self.histograma.update(activos)

# ───────────────────────────────────────────────────────────
# TURNO AUTOMATICO (IA Montecarlo)
# ───────────────────────────────────────────────────────────
def turno_automatico(jugador: Jugador, stats: EstadisticasJuego, ronda: int):
    """Ejecuta un turno completo de forma automatica usando estrategia Montecarlo."""
    dados = [0] * 5
    bloqueados = [False] * 5
    tiradas_restantes = 3

    sep = "-" * 58
    print(f"\n{sep}")
    print(f"  Ronda {ronda:>2}/13  |  {jugador.nombre}")
    print(sep)

    # Tirada inicial
    lanzar_dados(dados, bloqueados)
    stats.registrar(dados, bloqueados)
    tiradas_restantes -= 1
    print(f"  Tirada 1 -> {dados}")

    # Hasta 2 rerolls con estrategia MC
    while tiradas_restantes > 0:
        mascara = elegir_mascara_montecarlo(dados, tiradas_restantes, jugador.disponibles())

        if all(mascara):
            print(f"  IA decide plantarse.")
            break

        bloqueados = mascara[:]
        bloq_idx = [i + 1 for i, b in enumerate(bloqueados) if b]
        lanzar_dados(dados, bloqueados)
        stats.registrar(dados, bloqueados)
        tiradas_restantes -= 1

        tirada_num = 3 - tiradas_restantes
        print(f"  Tirada {tirada_num} -> {dados}  (bloqueados: D{bloq_idx})")

    # Elegir mejor categoria disponible
    cat, pts = mejor_categoria(dados, jugador.disponibles())
    jugador.registrar(cat, pts)
    print(f"  -> Categoria: {NOMBRE[cat]:<18} {pts:>3} pts  | Total: {jugador.total}")

# ───────────────────────────────────────────────────────────
# JUEGO COMPLETO
# ───────────────────────────────────────────────────────────
def jugar():
    jugadores = [Jugador("Jugador 1"), Jugador("Jugador 2")]
    stats = EstadisticasJuego()

    print("\n" + "=" * 58)
    print(f"{'YAHTZEE - SIMULACION MONTECARLO':^58}")
    print("=" * 58)
    print(f"  Semilla: {SEED}  |  Sims/mascara: {SIMS_POR_MASCARA}")
    print("=" * 58)

    for ronda in range(1, 14):
        for jugador in jugadores:
            turno_automatico(jugador, stats, ronda)

    return jugadores, stats

# ───────────────────────────────────────────────────────────
# MOSTRAR RESULTADOS
# ───────────────────────────────────────────────────────────
def mostrar_marcador(jugadores: List[Jugador]):
    print("\n" + "=" * 58)
    print(f"{'MARCADOR FINAL':^58}")
    print("=" * 58)
    print(f"{'Categoria':<22}", end="")
    for j in jugadores:
        print(f"{j.nombre:^18}", end="")
    print()
    print("-" * 58)
    for cat in CATEGORIAS:
        print(f"{NOMBRE[cat]:<22}", end="")
        for j in jugadores:
            v = j.puntuaciones.get(cat)
            print(f"{str(v if v is not None else 0):^18}", end="")
        print()
    print("-" * 58)
    print(f"{'TOTAL':<22}", end="")
    for j in jugadores:
        print(f"{j.total:^18}", end="")
    print()
    print("=" * 58)

    if jugadores[0].total > jugadores[1].total:
        ganador = jugadores[0].nombre
    elif jugadores[1].total > jugadores[0].total:
        ganador = jugadores[1].nombre
    else:
        ganador = "EMPATE"
    print(f"\n  GANADOR: {ganador}")


def mostrar_estadisticas(jugadores: List[Jugador], stats: EstadisticasJuego):
    total = sum(stats.histograma.values())
    promedio = sum(k * v for k, v in stats.histograma.items()) / total if total > 0 else 0

    print("\n" + "=" * 58)
    print(f"{'ESTADISTICAS MONTECARLO':^58}")
    print("=" * 58)
    print(f"  Total de dados lanzados        : {stats.total_lanzamientos}")
    print(f"  Promedio observado por dado     : {promedio:.4f}  (teorico: 3.5000)")
    print(f"  Desviacion del valor esperado   : {abs(promedio - 3.5):.4f}")
    print()
    print("  Distribucion de caras:")
    for cara in range(1, 7):
        c = stats.histograma.get(cara, 0)
        pct = (c / total * 100) if total > 0 else 0
        barra = "#" * int(pct / 2)
        print(f"    [{cara}]  {c:>5} veces  ({pct:5.2f}%)  {barra}")
    print()
    for j in jugadores:
        print(f"  Yahtzees de {j.nombre:<12}: {j.yahtzees}")
    print("=" * 58)


# ───────────────────────────────────────────────────────────
# ENTRADA PRINCIPAL
# ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    jugadores, stats = jugar()
    mostrar_marcador(jugadores)
    mostrar_estadisticas(jugadores, stats)