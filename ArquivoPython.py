import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados de tensão e corrente
tensaodf = pd.read_csv('F0001CH2.CSV - F0001CH2.CSV.csv', names=['A', 'B', 'C', 'D'])
correntedf = pd.read_csv('F0001CH1.CSV', names=['E', 'F', 'G', 'H'])

# Extrair os dados de tempo e tensão/corrente
tempo_tensao = tensaodf['C']
tensao = tensaodf['D']
tempo_corrente = correntedf['F']
corrente = correntedf['G'] * 10  # Escala de corrente aplicada

# Transformada Rápida de Fourier (FFT) para tensão e corrente
fft_tensao_meio = np.fft.fft(tensao)
fft_corrente_meio = np.fft.fft(corrente/10)

fft_correnteT = []
fft_tensaoT = []

for i in range(0, len(fft_corrente_meio), 1):
    
    termox2 = fft_corrente_meio[i] * 2
    fft_correnteT.append(termox2)

for i in range(0, len(fft_tensao_meio), 1):
    
    termox2 = fft_tensao_meio[i] * 2
    fft_tensaoT.append(termox2)

# Número total de pontos na FFT
nT = len(tensao)
nI = len(corrente)

# Ajuste das magnitudes dividindo pelo número de pontos
fft_tensao = np.abs(fft_tensaoT) / nT
fft_corrente = np.abs(fft_correnteT) / nI

# Frequências associadas (assumindo intervalos de tempo uniformes)
frequencia_tensao = np.fft.fftfreq(len(tempo_tensao), d=(tempo_tensao[1] - tempo_tensao[0]))
frequencia_corrente = np.fft.fftfreq(len(tempo_corrente), d=(tempo_corrente[1] - tempo_corrente[0]))

# Filtrar apenas as frequências positivas até os limites desejados
limite_tensao = (frequencia_tensao >= 0) & (frequencia_tensao <= 780)
limite_corrente = (frequencia_corrente >= 0) & (frequencia_corrente <= 3060)

# Configurar o estilo de gráfico
plt.style.use('dark_background')

# Plotar o gráfico da forma de onda (domínio do tempo)
plt.figure(figsize=(14, 6))
plt.plot(tempo_tensao, tensao, label='Tensão', color='blue')
plt.plot(tempo_corrente, corrente, label='Corrente 10x', color='yellow')
plt.title('Gráfico da Forma de Onda')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.show()

# Plotar o espectro de frequência (limitado às frequências de interesse e apenas frequências positivas)
plt.figure(figsize=(14, 12))  # Aumentamos a altura para 12 para mais espaço vertical

# Gráfico do espectro de tensão
plt.subplot(2, 1, 1)
plt.plot(frequencia_tensao[limite_tensao], np.abs(fft_tensao[limite_tensao]), color='blue')
plt.title('Harmônicas da tensão (Até 13°)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')

# Identificação das harmônicas ímpares até a 13°
fundamental_freq = 60  # Frequência fundamental
harmonicas_impares = [fundamental_freq * n for n in range(1, 14, 2) if fundamental_freq * n <= 800]
identificacao_harmonica = ["1°", "3°", "5°", "7°", "9°", "11°", "13°"]

for h, label in zip(harmonicas_impares, identificacao_harmonica):
    plt.axvline(x=h, color='white', linestyle='--', linewidth=0.3)  # Linha vertical mais fina e branca
    plt.text(h, 0.05 * np.max(np.abs(fft_tensao[limite_tensao])), label, color='white', ha='center', va='bottom', fontsize=10)  # Rótulo da harmônica no topo do gráfico

plt.subplot(2, 1, 2)
plt.plot(frequencia_corrente[limite_corrente], np.abs(fft_corrente[limite_corrente]), color='yellow')
plt.title('Harmônicas da corrente (Até 51°)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')

# Identificação das harmônicas ímpares até a 51°
harmonicas_impares_corrente = [fundamental_freq * n for n in range(1, 52, 2) if fundamental_freq * n <= 3060]
identificacao_harmonica_corrente = [f"{n}°" for n in range(1, 52, 2)]

for h, label in zip(harmonicas_impares_corrente, identificacao_harmonica_corrente):
    plt.axvline(x=h, color='white', linestyle='--', linewidth=0.3)  # Linha vertical mais fina e branca
    plt.text(h, 0.05 * np.max(np.abs(fft_corrente[limite_corrente])), label, color='white', ha='center', va='bottom', fontsize=10)  # Rótulo da harmônica no topo do gráfico

plt.tight_layout()
plt.show()

#===============FATOR DE POTENCIA==========================
tensao.reset_index(drop=True, inplace=True)
corrente.reset_index(drop=True, inplace=True)

# Verificar se os tamanhos das séries são compatíveis
min_length = min(len(tensao), len(corrente))
tensao = tensao[:min_length]
corrente = corrente[:min_length]

V_RMS = np.sqrt(np.mean(tensao**2))  
I_RMS = np.sqrt(np.mean((corrente/10)**2))  

P = np.mean(tensao*corrente/10) 

S = V_RMS * I_RMS  

FP = P / S



print(f'Valor RMS da Tensão: {V_RMS:.4f} V')
print(f'Valor RMS da Corrente: {I_RMS:.4f} A')
print(f"Potência Ativa (P): {P:.4f} W")
print(f"Potência Aparente (S): {S:.4f} VA")
print(f"Fator de Potência (FP): {FP:.4f}")

#===============THD TENSAO E CORRENTE==========================
def calcular_thd(fft_result, frequencias, fundamental_freq, escala=1):
    # Calcular a magnitude da componente fundamental
    idx_fundamental = np.argmin(np.abs(frequencias - fundamental_freq))
    v1 = np.abs(fft_result[idx_fundamental]) * escala  # Ajustar pela escala

    # Calcular a soma das harmônicas ímpares
    harmônicas = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
    
    # Armazenar magnitudes das harmônicas
    magnitudes_harmônicas = []

    for h in harmônicas:
        harm_freq = fundamental_freq * h
        idx_harmonica = np.argmin(np.abs(frequencias - harm_freq))
        magnitude_h = np.abs(fft_result[idx_harmonica])
        magnitudes_harmônicas.append(magnitude_h)

    # Calcular a soma das harmônicas
    i = 0
    somaHarmonicas = 0
    while i < len(magnitudes_harmônicas):
        magn = magnitudes_harmônicas[i]**2
        somaHarmonicas = somaHarmonicas + magn
        i = i + 1
    
    # Calcular THD
    thd = np.sqrt(somaHarmonicas) / v1 if v1 > 0 else 0  # Prevenir divisão por zero
    return thd

# Calcular THD para tensão e corrente
thd_tensao = calcular_thd(fft_tensao, frequencia_tensao, 60)  # 60 Hz
thd_corrente = calcular_thd(fft_corrente, frequencia_corrente, 60)  # Ajustando pela escala da corrente

# Passando para porcentagem

thd_tensao_prc = thd_tensao * 100
thd_corrente_prc = thd_corrente * 100

# Exibir os resultados
print(f'THD da Tensão: {thd_tensao_prc:.4f} %')
print(f'THD da Corrente: {thd_corrente_prc:.4f} %')

#===============FATOR DE DESLOCAMENTO==========================
fator_distorcao = 1 / np.sqrt(1 + thd_corrente**2)

# Cálculo do fator de deslocamento
fator_deslocamento = FP / fator_distorcao

# Resultados
print(f"Fator de deslocamento da corrente em relação à tensão: {fator_deslocamento:.4f}")