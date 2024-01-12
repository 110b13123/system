import json
import math

class Printer:
    @staticmethod
    def print_header():
        print(" %-10s %-20s %-15s %-15s %-15s %-17s" %
              ('行號', '位置', '指令', '運算數', '目標代碼', ''))

    @staticmethod
    def print_line(line):
        print(" %-10s %-20s %-15s %-15s %-15s %-17s" % tuple(line))


# 定義相關字典和函數...
def Dec2Hex(Dec: int):
    Hex = ''
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16

    Hex = (HexDict[Dec] + Hex)
    return Hex

def Hex2Dec(Hex: str):
    Dec = 0
    times = 0
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]
        times += 1

    return Dec

def Bin2Hex(Bin):
    Hex = ''
    if (len(Bin) > 4):
        fill = (4 - (len(Bin) % 4))
        if (fill == 4):
            fill = (fill - 4)

        Bin = ('0'*fill + Bin)

        for i in range(0, len(Bin), 4):
            Hex += Bin2Hex(Bin[i:(i*4+4)])
    else:
        Dec = 0
        for i, digit in enumerate(Bin):
            Dec += (int(digit) * math.pow(2, (3-i)))
        Hex = Dec2Hex(Dec)

    return Hex

def BYTE(parms):
    mode = parms[0]
    data = parms[2:-1]
    objCode = ''
    if (mode == 'C'):
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
    elif (mode == 'X'):
        objCode += data
    else:
        print('BYTE Error')

    location_add = (len(objCode)//2)
    return location_add, objCode

def WORD(parms):
    if (int(parms) >= 0):
        objCode = Dec2Hex(int(parms)).zfill(6)
    else:
        full_hex = Hex2Dec('1000000')
        objCode = Dec2Hex(full_hex + int(parms)).zfill(6)
    location_add = (len(objCode)//2)
    return location_add, objCode

def RESB(parms):
    objCode = ' '
    location_add = int(parms)
    return location_add, objCode

def RESW(parms):
    objCode = ' '
    location_add = (int(parms) * 3)
    return location_add, objCode


class Register:
    A = False
    X = False
    L = False
    B = False
    S = False
    T = False
    F = False
    PC = False
    SW = False

    def Load(self, instrucet, parms):
        if (instrucet == 'LDA'):
            self.A = parms
        elif (instrucet == 'LDX'):
            self.X = parms
        elif (instrucet == 'LDL'):
            self.L = parms
        elif (instrucet == 'LDB'):
            self.B = parms
        elif (instrucet == 'LDS'):
            self.S = parms
        elif (instrucet == 'LDT'):
            self.T = parms
        elif (instrucet == 'LDF'):
            self.F = parms

    def Clear(self, parms):
        if (parms == 'A'):
            self.A = 0
        elif (parms == 'X'):
            self.X = 0
        elif (parms == 'L'):
            self.L = 0
        elif (parms == 'B'):
            self.B = 0
        elif (parms == 'S'):
            self.S = 0
        elif (parms == 'T'):
            self.T = 0
        elif (parms == 'F'):
            self.F = 0
        elif (parms == 'PC'):
            self.PC = 0
        elif (parms == 'SW'):
            self.SW = 0

    def Location_of_rigster(self):
        if self.A:
            self.A = self.Parms_computing(self.A)
        elif self.X:
            self.X = self.Parms_computing(self.X)
        elif self.L:
            self.L = self.Parms_computing(self.L)
        elif self.B:
            self.B = self.Parms_computing(self.B)
        elif self.S:
            self.S = self.Parms_computing(self.S)
        elif self.T:
            self.T = self.Parms_computing(self.T)
        elif self.F:
            self.F = self.Parms_computing(self.F)

    def Parms_computing(self, parms):
        if (parms[0] == '#'):
            parms = parms[1:]
            return function_[parms]

# 導入所需的模組
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

file_path = './Input.txt'

# 讀取文件
with open(file_path, 'r') as f:
    input_lines = f.readlines()

# 初始化 information 列表
information = []

# 創建 Register 實例
register = Register()

# 初始化 line 變數
line = 5

# 定義寄存器和十六進制轉換字典
num_of_register = {'A': 0, 'X': 1, 'L': 2, 'B': 3,
                   'S': 4, 'T': 5, 'F': 6, 'PC': 8,}
