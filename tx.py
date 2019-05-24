#!/usr/bin/python3

from LD import *
import sys 

argumentos = sys.argv[1:]

if (len(argumentos) != 2):
  print('Para executar o App é preciso digitar: ')
  print('   - A porta da serial: /dev/pts/19')
  print('   - O Proto: 5')
  sys.exit(1)

port = argumentos[0] #'/dev/pts/19'
proto = int(argumentos[1])

print('----------------------------------------------------------------------------')
print(' ')
print('Protocolo de Enlace LD')
print(' ')
print('----------------------------------------------------------------------------')
print(' ')
print('Iniciando o Transmissor:')
print(' ')
app = LD(port, proto)
app.transmite()
print('----------------------------------------------------------------------------')
print('Transmissão encerrada.')
print('----------------------------------------------------------------------------')
