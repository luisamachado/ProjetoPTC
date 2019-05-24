#!/usr/bin/python3
 
import serial
import crc
from enum import Enum

class Enquadramento():
  estados = Enum('estados','ocioso rx recepcao esc')


  def __init__(self, port, bytes_min = 8, bytes_max = 256):
    self.min_bytes = bytes_min
    self.max_bytes = bytes_max
    self.n = 0
    self.ser = serial.Serial(port, 9600, dsrdtr = True, rtscts = True)
    self.estado = self.estados.ocioso
    self.bufer = bytearray()


  def envia(self, bufer, bytes):
    self.bufer = bytearray()
    fcs = crc.CRC16(bufer)
    msg = fcs.gen_crc()
    self.bufer.append(0x7E)
    for n in range(len(msg)):
      if (chr(msg[n]) == '~'): #7E
        self.bufer.append(0x7D)
        self.bufer.append(msg[n] ^ 0x20)
      elif (chr(msg[n]) == '}'): #7D
        self.bufer.append(0x7D)
        self.bufer.append(msg[n] ^ 0x20)
      else:
        self.bufer.append(msg[n])
    self.bufer.append(0x7E)
    return self.ser.write(self.bufer)


  def ocioso(self, byte):
    if (byte == b'~'): #7E
      self.bufer = bytearray()
      self.estado = self.estados.rx
    else:
      self.estado = self.estados.ocioso


  def rx(self, byte):
    if (byte == b'~'): #7E
      self.estado = self.estados.rx
    elif (byte == b'}'): #7D
      self.estado = self.estados.esc
    else:
      self.bufer.append(ord(byte))
      self.estado = self.estados.recepcao


  def recepcao(self, byte):
    if (byte == b'~'): #7E
      self.estado = self.estados.ocioso
    elif (byte == b'}'): #7D
      self.estado = self.estados.esc
    else:
      self.bufer.append(ord(byte))
      self.estado = self.estados.recepcao


  def esc(self, byte):
    if (byte == b'~' or byte == b'}'): # aqui vem o timeout também
      self.bufer = bytearray() # zera o buffer
      self.estado = self.estados.ocioso
    else:
      byte_novo = ord(byte.decode()) ^ 0x20
      self.bufer.append(byte_novo)
      self.estado = self.estados.recepcao


  def recebe(self):
    while(True):
      bt_recebido  = self.ser.read()
      if (self.n > self.max_bytes or bt_recebido == b''):
        self.n = 0
        return 0
      self.n = self.n + 1
      if (self.handle(bt_recebido) == True):
        fcs = crc.CRC16(self.bufer)
        if (fcs.check_crc() == True):
          return self.bufer[0:-2]
        else:
          self.bufer = bytearray()
          pass


  def handle(self, byte):
    # estado ocioso
    if (self.estado == self.estados.ocioso):
      self.ocioso(byte)
    # estado rx
    elif (self.estado == self.estados.rx):
      self.rx(byte)
      if (self.estado == self.estados.ocioso):
        return True
    # estado recepcao
    elif (self.estado == self.estados.recepcao): 
      self.recepcao(byte)
      if (self.estado == self.estados.ocioso):
        return True
    # estado esc
    elif (self.estado == self.estados.esc): 
      self.esc(byte)
      if (self.estado == self.estados.ocioso):
        return True
    return False
