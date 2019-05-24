#!/usr/bin/python3

from LD import *
import sys

argumentos = sys.argv[1:]

if (len(argumentos) != 2):
  print('Para executar o App é preciso digitar: ')
  print('   - A porta da serial: /dev/pts/6')
  print('   - O Proto: 5')
  sys.exit(1)

port = argumentos[0] #'/dev/pts/6'
proto = int(argumentos[1])

print('----------------------------------------------------------------------------')
print(' ')
print('Protocolo de Enlace LD')
print(' ')
print('----------------------------------------------------------------------------')
print(' ')
print('Iniciando o Receptor:')
print(' ')
print('Aguardando dado...')
print(' ')
print('----------------------------------------------------------------------------')
bufer = bytearray()
print('Dado recebido:')
while(True):
  app = LD(port, proto)
  bufer = app.recebe()
  print(' ')
  print(bufer)
print(' ')
print('----------------------------------------------------------------------------')
print('Recepção encerrada.')
print('----------------------------------------------------------------------------')
