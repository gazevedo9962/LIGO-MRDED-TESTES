import matplotlib.pyplot as plt

# Dados
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Criar gráfico
plt.plot(x, y)
plt.title("Exemplo de Gráfico no Codespaces")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")

# Salvar o gráfico como imagem
plt.savefig('grafico.png')
print("Gráfico salvo como grafico.png")
