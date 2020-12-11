#include <stdio.h>

void escrevaInteiro(int inteiro) {
  printf("%d\n", inteiro);
  
}

void escrevaFlutuante(float flutuante) {
  printf("%f\n", flutuante);

}

int leiaInteiro() {
  int numero;

  scanf("%d", &numero);

  return numero;
}

float leiaFlutuante() {
  float numero;

  scanf("%f", &numero);

  return numero;
}