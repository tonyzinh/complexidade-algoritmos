from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Callable


sys.setrecursionlimit(10_000)

REPETICOES_MEDICAO = 500
FIBONACCI_RECURSIVO_MEDIDO = [10, 15, 20]
FIBONACCI_RECURSIVO_ESTIMADO = [50, 100]
FIBONACCI_DINAMICO_MEDIDO = [20, 50, 100, 500, 1000]


class Fibonacci:
    """Implementacoes de Fibonacci usadas na comparacao."""

    def __init__(self) -> None:
        self.contador_chamadas = 0

    def recursivo(self, numero: int) -> int:
        """Calcula Fibonacci por recursao pura e conta chamadas."""
        self.contador_chamadas += 1

        if numero <= 1:
            return numero

        return self.recursivo(numero - 1) + self.recursivo(numero - 2)

    def memoizacao(self, numero: int, cache: dict[int, int] | None = None) -> int:
        """Calcula Fibonacci com recursao top-down e cache."""
        if cache is None:
            cache = {}

        if numero in cache:
            return cache[numero]

        if numero <= 1:
            cache[numero] = numero
            return numero

        cache[numero] = self.memoizacao(numero - 1, cache) + self.memoizacao(
            numero - 2, cache
        )
        return cache[numero]

    @staticmethod
    def iterativo(numero: int) -> int:
        """Calcula Fibonacci com programacao dinamica bottom-up."""
        if numero <= 1:
            return numero

        tabela = [0] * (numero + 1)
        tabela[1] = 1

        for indice in range(2, numero + 1):
            tabela[indice] = tabela[indice - 1] + tabela[indice - 2]

        return tabela[numero]

    @staticmethod
    def medir_tempo(
        metodo: Callable[[int], int], numero: int, repeticoes: int = REPETICOES_MEDICAO
    ) -> tuple[int, float]:
        """Retorna o resultado e o tempo medio de execucao."""
        inicio = time.perf_counter()

        for _ in range(repeticoes):
            resultado = metodo(numero)

        fim = time.perf_counter()
        return resultado, (fim - inicio) / repeticoes


@dataclass(frozen=True)
class ResultadoMochila:
    valor: int
    itens: list[int]
    peso_total: int


class Mochila:
    """Resolve uma instancia do Problema da Mochila 0/1."""

    def __init__(self, pesos: list[int], valores: list[int], capacidade: int) -> None:
        if len(pesos) != len(valores):
            raise ValueError("As listas de pesos e valores devem ter o mesmo tamanho.")

        self.pesos = pesos
        self.valores = valores
        self.capacidade = capacidade
        self.quantidade_itens = len(pesos)

    def forca_bruta(self) -> ResultadoMochila:
        melhor_valor = 0
        melhores_itens: list[int] = []
        melhor_peso = 0

        for mascara in range(1 << self.quantidade_itens):
            peso_total = 0
            valor_total = 0
            itens_escolhidos: list[int] = []

            for indice in range(self.quantidade_itens):
                if mascara & (1 << indice):
                    peso_total += self.pesos[indice]
                    valor_total += self.valores[indice]
                    itens_escolhidos.append(indice)

            if peso_total <= self.capacidade and valor_total > melhor_valor:
                melhor_valor = valor_total
                melhores_itens = itens_escolhidos
                melhor_peso = peso_total

        return ResultadoMochila(melhor_valor, melhores_itens, melhor_peso)

    def programacao_dinamica(self) -> ResultadoMochila:
        n = self.quantidade_itens
        tabela = [[0] * (self.capacidade + 1) for _ in range(n + 1)]

        for linha in range(1, n + 1):
            peso_item = self.pesos[linha - 1]
            valor_item = self.valores[linha - 1]

            for peso in range(self.capacidade + 1):
                sem_item = tabela[linha - 1][peso]
                com_item = 0

                if peso_item <= peso:
                    com_item = tabela[linha - 1][peso - peso_item] + valor_item

                tabela[linha][peso] = max(sem_item, com_item)

        return self._recuperar_solucao(tabela)

    def versao_decisao(self, limiar: int) -> tuple[bool, ResultadoMochila]:
        resultado = self.programacao_dinamica()
        return resultado.valor >= limiar, resultado

    def _recuperar_solucao(self, tabela: list[list[int]]) -> ResultadoMochila:
        itens: list[int] = []
        peso_atual = self.capacidade

        for linha in range(self.quantidade_itens, 0, -1):
            if tabela[linha][peso_atual] != tabela[linha - 1][peso_atual]:
                indice_item = linha - 1
                itens.append(indice_item)
                peso_atual -= self.pesos[indice_item]

        itens.reverse()
        valor_total = tabela[self.quantidade_itens][self.capacidade]
        peso_total = sum(self.pesos[indice] for indice in itens)

        return ResultadoMochila(valor_total, itens, peso_total)


def imprimir_cabecalho(titulo: str) -> None:
    print("=" * 65)
    print(titulo)
    print("=" * 65)


def imprimir_fibonacci_recursivo(fibonacci: Fibonacci) -> None:
    imprimir_cabecalho("PARTE 1 - Fibonacci recursivo puro")
    print(f"{'n':>4} | {'F(n)':>15} | {'chamadas':>14} | {'tempo (s)':>12}")
    print("-" * 55)

    for numero in FIBONACCI_RECURSIVO_MEDIDO:
        fibonacci.contador_chamadas = 0
        inicio = time.perf_counter()
        resultado = fibonacci.recursivo(numero)
        tempo = time.perf_counter() - inicio

        print(
            f"{numero:>4} | {resultado:>15} | "
            f"{fibonacci.contador_chamadas:>14,} | {tempo:>12.6f}"
        )

    tempo_base, chamadas_base = medir_base_recursiva(fibonacci)

    for numero in FIBONACCI_RECURSIVO_ESTIMADO:
        chamadas_estimadas = estimar_chamadas_recursivas(numero)
        tempo_estimado = tempo_base * (chamadas_estimadas / chamadas_base)
        valor = fibonacci.iterativo(numero)

        print(
            f"{numero:>4} | {valor:>15} | {chamadas_estimadas:>14,} | "
            f"~{tempo_estimado:>10.1f}s  [estimado]"
        )

    print()
    print("  Obs: fib(50) e fib(100) nao sao executados diretamente pois a")
    print("  versao recursiva pura tem complexidade O(phi^n). Os valores acima")
    print("  sao extrapolados a partir do tempo medido para fib(35).")


def medir_base_recursiva(fibonacci: Fibonacci, numero_base: int = 35) -> tuple[float, int]:
    fibonacci.contador_chamadas = 0
    inicio = time.perf_counter()
    fibonacci.recursivo(numero_base)
    tempo = time.perf_counter() - inicio

    return tempo, fibonacci.contador_chamadas


def estimar_chamadas_recursivas(numero: int) -> int:
    return (2 * Fibonacci.iterativo(numero + 1)) - 1


def imprimir_fibonacci_dinamico(fibonacci: Fibonacci) -> None:
    print()
    imprimir_cabecalho("PARTE 1 - Fibonacci com Programacao Dinamica")
    print(f"{'n':>5} | {'F(n)':>20} | {'memoizacao (s)':>16} | {'iterativo (s)':>14}")
    print("-" * 62)

    for numero in FIBONACCI_DINAMICO_MEDIDO:
        resultado_memo, tempo_memo = fibonacci.medir_tempo(fibonacci.memoizacao, numero)
        _, tempo_iterativo = fibonacci.medir_tempo(fibonacci.iterativo, numero)

        print(
            f"{numero:>5} | {resultado_memo:>20} | "
            f"{tempo_memo:>16.8f} | {tempo_iterativo:>14.8f}"
        )


def imprimir_mochila() -> None:
    pesos = [2, 3, 4, 5, 1, 6, 3, 7]
    valores = [3, 4, 5, 8, 2, 9, 4, 10]
    capacidade = 15
    limiar = 20

    mochila = Mochila(pesos, valores, capacidade)

    print()
    imprimir_cabecalho("PARTE 2 - Problema da Mochila 0/1 (NP-Completo)")
    print(
        f"\nInstancia: {mochila.quantidade_itens} itens, "
        f"capacidade = {capacidade}, limiar = {limiar}"
    )
    print(f"Pesos:   {pesos}")
    print(f"Valores: {valores}")

    inicio = time.perf_counter()
    resultado_bruto = mochila.forca_bruta()
    tempo_bruto = time.perf_counter() - inicio

    inicio = time.perf_counter()
    resultado_dp = mochila.programacao_dinamica()
    tempo_dp = time.perf_counter() - inicio

    resposta, certificado = mochila.versao_decisao(limiar)

    print(
        f"\n  Forca bruta  -> valor otimo: {resultado_bruto.valor} "
        f"| tempo: {tempo_bruto:.6f}s | complexidade: O(2^n)"
    )
    print(
        f"  DP bottom-up -> valor otimo: {resultado_dp.valor} "
        f"| tempo: {tempo_dp:.6f}s | complexidade: O(n*W)"
    )
    print(
        f"  Itens escolhidos pela DP: {resultado_dp.itens} "
        f"(peso = {resultado_dp.peso_total})"
    )

    print(
        f"\n  Versao de decisao: existe subconjunto com valor >= {limiar} "
        f"e peso <= {capacidade}?"
    )
    print(
        f"  Resposta: {'SIM' if resposta else 'NAO'} "
        f"(valor otimo encontrado = {certificado.valor})"
    )
    print()
    print("  Certificado: a propria lista de itens selecionados e o certificado.")
    print("  Dado um candidato a solucao (subconjunto de itens), podemos verificar")
    print("  em tempo polinomial O(n) que a soma dos pesos nao excede a capacidade")
    print("  e que a soma dos valores atinge o limiar. Isso confirma que o problema")
    print("  esta em NP. Nao se conhece algoritmo polinomial para encontrar esse")
    print("  subconjunto, por isso o problema e NP-Completo.")
    print()
    print("  Heuristicas e aproximacoes praticas:")
    print("  - Greedy por razao valor/peso: rapido, mas nao garante otimo.")
    print("  - FPTAS: garante solucao dentro de (1-epsilon) do otimo em O(n^2 / epsilon).")
    print("  - Branch and Bound: explora arvore de decisao com podas, exponencial no pior caso.")


def main() -> None:
    fibonacci = Fibonacci()

    imprimir_fibonacci_recursivo(fibonacci)
    imprimir_fibonacci_dinamico(fibonacci)
    imprimir_mochila()


if __name__ == "__main__":
    main()
