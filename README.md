# Trabalho C3 - Complexidade de Algoritmos

Projeto desenvolvido para comparar abordagens de algoritmos vistas na disciplina:

- Fibonacci recursivo puro.
- Fibonacci com programacao dinamica.
- Problema da Mochila 0/1 como exemplo de problema NP-Completo.

## Arquivos

- `fibonacci_comparacao.py`: codigo principal com os experimentos.

## Requisitos

O projeto usa apenas a biblioteca padrao do Python.

- Python 3.10 ou superior recomendado.

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python fibonacci_comparacao.py
```

Em alguns ambientes, o comando pode ser:

```bash
python3 fibonacci_comparacao.py
```

## O que o programa faz

### Parte 1 - Fibonacci

O codigo compara tres implementacoes:

1. **Recursiva pura**: implementacao direta da definicao matematica.
2. **Memoizacao**: versao recursiva com cache dos resultados ja calculados.
3. **Bottom-up**: versao iterativa com tabela preenchida do menor subproblema ate o maior.

A versao recursiva pura e executada apenas para valores pequenos, porque sua
complexidade cresce de forma exponencial. Para `fib(50)` e `fib(100)`, o
programa calcula uma estimativa com base no numero de chamadas esperado.

As versoes com programacao dinamica conseguem calcular valores maiores, como
`fib(500)` e `fib(1000)`, em tempo muito menor porque cada subproblema e
resolvido uma unica vez.

### Parte 2 - Mochila 0/1

O codigo tambem resolve uma instancia do Problema da Mochila 0/1 usando:

1. **Forca bruta**: testa todos os subconjuntos possiveis.
2. **Programacao dinamica**: monta uma tabela `dp[i][w]` com o melhor valor
   usando os primeiros `i` itens e capacidade `w`.

A saida mostra:

- valor otimo encontrado;
- tempo de execucao de cada abordagem;
- itens escolhidos pela solucao dinamica;
- resposta da versao de decisao;
- explicacao do certificado verificavel em tempo polinomial.

## Complexidades

| Problema | Abordagem | Complexidade |
| --- | --- | --- |
| Fibonacci | Recursao pura | `O(phi^n)` |
| Fibonacci | Memoizacao | `O(n)` |
| Fibonacci | Bottom-up | `O(n)` |
| Mochila 0/1 | Forca bruta | `O(2^n)` |
| Mochila 0/1 | Programacao dinamica | `O(n * W)` |

Na Mochila 0/1, `n` e a quantidade de itens e `W` e a capacidade da mochila.
A solucao por programacao dinamica e pseudopolinomial, pois depende do valor
numerico de `W`.

## Observacao sobre tempos

Os tempos de execucao podem variar conforme o computador. Por isso, para o
relatorio, o ideal e executar o script na maquina usada pelo grupo e registrar
os resultados obtidos localmente.
