#Algoritmo para resolver uma equação polinomial do 2º grau
import math
print("Agora vamos resolver equações quadráticas!")
coef_a = float(input("Entre com o coeficiente a: "))
coef_b = float(input("Entre com o coeficiente b: "))
termo_c = float(input("Entre com o termo independente C: "))

delta = coef_b**2 - 4 * coef_a * termo_c

if delta > 0:
  x1 = (-coef_b + math.sqrt(delta)) / (2 * coef_a)
  x2 = (-coef_b - math.sqrt(delta)) / (2 * coef_a)

  print("Raízes reais e distintas: ")
  print(f"x1= {x1}")
  print(f"x2= {x2}")

elif delta == 0:
  x= (-coef_b + math.sqrt(delta)) / (2 * coef_a)
  print(f"Raízes reais e iguais: x = {x}")
else:
  print("Não existem raízes reais para esta equação.")
# A estrutura %7.2f" % serve para limitar o número de casas decimais em variáveis do tipo float.
#Nesse caso, suporta até 7 caracteres incluindo a vírgula. E o número 2 representa a quantidade total de casas decimais após a vírgula.
