# Análise das harmônicas de um Retificador Monofásico Ponte Completa com Filtro Capacitivo em PYTHON

## Descrição do Projeto
Este projeto visa analisar os aspectos de um retificador monofásico ponte completa com filtro capacitivo. A análise inclui o cálculo do fator de potência, fator de deslocamento, THD (distorção harmônica total) da tensão e da corrente, e a identificação das componentes harmônicas ímpares. O objetivo principal é entender a influência das harmônicas em sistemas elétricos, comprovando resultados por meio de cálculos, gráficos e comparações.

## Estrutura do Projeto
- **Código Python**: Realiza os cálculos e plotagens dos gráficos necessários para a análise.
- **Arquivos CSV**: Contêm os dados de tensão e corrente, coletados via osciloscópio, usados nas simulações e cálculos.
- **Relatório de Análise**: Fornece uma visão detalhada dos resultados e conclusões obtidos a partir dos dados simulados.

## Funcionalidades Principais
1. **Análise no Domínio da Frequência**:
   - Cálculo e plotagem do espectro de frequência (Transformada de Fourier) para tensão e corrente, com foco nas harmônicas ímpares.
2. **Cálculo do Fator de Potência**:
   - Cálculo do fator de potência, com separação da potência ativa e aparente.
3. **THD da Tensão e Corrente**:
   - Cálculo da distorção harmônica total (THD) para ambas as formas de onda.
4. **Fator de Deslocamento**:
   - Determinação do fator de deslocamento da corrente em relação à tensão.

## Requisitos
- Python 3.x
- Bibliotecas:
  - `pandas`
  - `numpy`
  - `matplotlib`

## Como Usar
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Instale as bibliotecas necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script principal:
   ```bash
   python main.py
   ```

## Exemplo de Código
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados de tensão e corrente
tensaodf = pd.read_csv('F0001CH2.CSV - F0001CH2.CSV.csv', names=['A', 'B', 'C', 'D'])
correntedf = pd.read_csv('F0001CH1.CSV', names=['E', 'F', 'G', 'H'])

# Processamento dos dados e análise no domínio da frequência
# ... (continue com o código completo do projeto)
```

## Resultados Obtidos
- **Fator de Potência**: 0,7480
- **THD da Tensão**: 7,08%
- **THD da Corrente**: 75,58%
- **Fator de Deslocamento**: 0,9376

## Conclusão
Os resultados mostram que a tensão apresenta uma baixa distorção harmônica devido ao filtro capacitivo, enquanto a corrente tem uma distorção elevada, resultando em um baixo fator de potência. Esses resultados são esperados em retificadores com filtro capacitivo e refletem a importância de compensações harmônicas para aplicações reais.

## Licença
Este projeto é distribuído sob a licença MIT.
