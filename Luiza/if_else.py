#Condicional if/else
#Exemplo 3: Escreva um script que lê dois números e imprime o maior deles.
x = int(input("Digite um número para x: "))
y = int(input("Digite um número para y: "))
if y > x:
  print(f"{y} é maior que {x}")
else:
  if y<x:
    print(f"{y} é menor que {x}")
  else:
    if x==y:

      print(f"{x} é igual a {y}")
