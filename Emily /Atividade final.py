#Definindo a quantidade de imput
n = int(input("Quantos valores você quer inserir? "))
valores = []

for i in range(n):
    valor = input(f"Digite o valor {i + 1}: ")
    valores.append(valor)

print("Valores inseridos:", valores)

# Com uma palavra especifica para parar
valores = []
print("Digite os valores. Para encerrar basta digitar 'sair':")

while True:
    entrada = input("Digite um valor: ")
    
    if entrada.lower() == 'sair':
        break
    
    valores.append(entrada)


print(f"Você digitou {len(valores)} valores:", valores)
