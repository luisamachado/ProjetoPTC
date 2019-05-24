#!/usr/bin/python3

import time
from enum import Enum

class ARQ:
  estados = Enum('estados','primeiro segundo')
  tipoEvento = Enum('tipoEvento','payload quadro timeout')


  def __init__(self, enquad, proto):
    self.enq = enquad
    self.ptr = proto
    self.bufer = bytearray()
    self.m = 0
    self.n = 0
    self.estado = self.estados.primeiro
    self.tipo = 0
    self.quadrotx = bytearray()
    self.quadrorx = bytearray()


  def enviaQuadro(self): 
    self.quadrotx = bytearray() # limpa buffer
    # 0000 0000 = pacote 0
    # 0000 1000 = pacote 1
    if (self.n == 0):
      controle = 0b00000000
    else:
      controle = 0b00001000
    # quadrotx = (controle + id + payload)
    self.quadrotx.append(controle)
    self.quadrotx.append(self.ptr)
    self.quadrotx = self.quadrotx + self.bufer
    #print(self.quadrotx)
    return self.enq.envia(self.quadrotx, len(self.quadrotx))


  def enviaACK(self, seq):
    ack = bytearray()
    if (seq == 0):
      controle = 0b10000000
    else:
      controle = 0b10001000
    # ack = (controle + id)
    ack.append(controle)
    #time.sleep(10)
    self.enq.envia(ack, len(ack))


  def estado_primeiro(self): 
    if (self.tipo == self.tipoEvento.payload): # recebe payload
      i = self.enviaQuadro() # envia o quadro
      # seta o timeout
      self.estado = self.estados.segundo # troca de estado
      
    elif(self.tipo == self.tipoEvento.quadro): # recebe um dado da funcão recebe do enq
      #print('dado recebido')
      #print(self.quadrorx)
      if(((self.quadrorx[0] & 0b10000000) >> 7) != 1): # verifica se recebeu um dado 00000000
        if(((self.quadrorx[0] & 0b00001000) >> 3) == self.m): # verifica se controle igual a m
          self.enviaACK(int(self.m))
          self.m = int(not(self.m))
          self.estado = self.estados.primeiro
        else: # senão
          self.enviaACK(int(not(self.m)))
          self.estado = self.estados.primeiro


  def estado_segundo(self):
    if (self.tipo == self.tipoEvento.payload): # recebe payload
      self.quadrorx = self.enq.recebe()
      if (self.quadrorx == b''):
        return
      elif(((self.quadrorx[0] & 0b10000000) >> 7) == 1): # verifica se recebeu um ack
        if(((self.quadrorx[0] & 0b00001000) >> 3) != self.n): # se timeout ou recebeu ack do not(n)
          self.enq.envia(self.quadrotx, len(self.quadrotx)) # reenvia o quadrotx
          # seta o timeout
          self.estado = self.estados.segundo
        else: # se recebe ack do n
          # cancela timeout
          self.n = int(not(self.n))
          self.estado = self.estados.primeiro # troca de estado
    
    elif(self.tipo == self.tipoEvento.quadro): # recebe um dado da funcão recebe do enq
      #print('dado recebido')
      if(((self.quadrorx[0] & 0b10000000) >> 7) != 1): # verifica se recebeu um dado 00000000
        if(((self.quadrorx[0] & 0b00001000) >> 3) == self.m): # verifica se controle igual a m
          self.enviaACK(int(self.m))
          self.m = int(not(self.m))
          self.estado = self.estados.primeiro
        else: # senão
          self.enviaACK(int(not(self.m)))
          self.estado = self.estados.primeiro


  def envia(self, bufer):
    self.bufer = bufer
    if (bufer == b''):
      print('Buffer vazio.')
      return bytearray()
    else:
      # evento do tipo payload
      self.tipo = self.tipoEvento.payload
      if (self.handle() == True):
        pass
      while(self.estado != self.estados.primeiro):
        self.handle()
    return


  def recebe(self):
    self.tipo = self.tipoEvento.quadro
    while(True):
      self.quadrorx = self.enq.recebe()
      if (self.quadrorx == b''):
        return bytearray()
      if (self.handle() == True):
        return self.quadrorx[2:]


  #def setTimeout(self, tout):


  def handle(self):
    # estado primeiro
    if (self.estado == self.estados.primeiro):
      self.estado_primeiro()
      return True
    # estado segundo
    elif (self.estado == self.estados.segundo):
      self.estado_segundo()
      return False
