# LIGO-MRDED-TESTES

Simulações, Testes da Teoria Mecânica e Discreta da Gravitação.

# MRDED — Modelo de Rede Dinâmica Espaço-Deformável

## 📌 Descrição

O **MRDED (Modelo de Rede Dinâmica Espaço-Deformável)** propõe que o espaço-tempo é uma rede discreta dinâmica, onde:

* Matéria = compressão da rede
* Tempo = taxa de oscilação das células
* Gravidade = gradiente de deformação

---

## 🎯 Objetivo deste repositório

Investigar uma assinatura observacional da teoria:

> **ecos gravitacionais em ondas detectadas pelo LIGO Scientific Collaboration**

---

## 🔬 Metodologia

1. Modelagem do sinal padrão (Relatividade Geral)
2. Introdução de ecos gravitacionais (MRDED)
3. Comparação via estatística χ²
4. Teste com dados reais (ex: GW150914)
5. Simulação Monte Carlo para detectabilidade

---

## ⚙️ Modelo MRDED Avançado

Inclui:

* dispersão de frequência
* amortecimento progressivo
* fase de reflexão
* atenuação não linear

---

## 📊 Resultado Principal

A análise de detectabilidade mostra:

$$
R_{\text{crit}} \approx 0.2
$$

---

## 🧠 Interpretação

* Para (R < 0.2): ecos não detectáveis
* Para (R > 0.2): ecos detectáveis

---

## 🔥 Conclusão

> A ausência de ecos observáveis não descarta a teoria MRDED, mas impõe restrições físicas ao coeficiente de reflexão da rede.

---

## 📁 Estrutura

* `fit_mrded.py` → ajuste inicial
* `fit_mrded_v2.py` → versão física (ringdown)
* `detectability_test.py` → teste básico
* `final_detectability_plot.py` → resultado final

---

## 🚀 Status

| Etapa           | Status       |
| --------------- | ------------ |
| Modelagem       | ✔            |
| Teste com dados | ✔            |
| Detectabilidade | ✔            |
| Limite físico   | ✔            |
| Publicação      | em andamento |

---

## 📌 Próximos passos

* testar múltiplos eventos
* refinar dinâmica da rede
* derivar equações fundamentais


