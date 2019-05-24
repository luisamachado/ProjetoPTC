#!/usr/bin/python3

from Enquadramento import *
from ARQ import *

class LD:

  def __init__(self, port, proto):
    self.enq = Enquadramento(port)
    self.arq = ARQ(self.enq, proto)


  def transmite(self):
    while(True):
      aux = input("Digite a informação para enviar: ")
      #aux = '~abcdef}1234567~'
      bufer = bytearray(aux, 'utf8')
      self.arq.envia(bufer)
      print('Enviando...')
      i = input("Transmitir mais informação? (1 - sim / 2 - não) \n")
      if (i == '2'):
        break
    print(' ')


  def recebe(self):
    bufer = self.arq.recebe()
    if (len(bufer) >= 1):
      return bufer
    return bytearray()
