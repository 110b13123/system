import json
import math
#導入所需的模組：json 用於處理 JSON 文件，math 用於數學運算

# 定義寄存器和十六進制轉換字典
num_of_register = {'A': 0, 'X': 1, 'L': 2, 'B': 3,
                   'S': 4, 'T': 5, 'F': 6, 'PC': 8, 'SW': 9}
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

# 定義二進制轉十六進制的函數
def Bin2Hex(Bin):
    Hex = ''#空格字符
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

#定義了十進制轉十六進制的函數Dec2Hex
def Dec2Hex(Dec: int):
    Hex = ''
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16

    Hex = (HexDict[Dec] + Hex)
    return Hex

#定義了十六進制轉十進制的函數Hex2Dec
def Hex2Dec(Hex: str):
    Dec = 0
    times = 0
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]
        times += 1

    return Dec

# 定義BYTE指令的函數
def BYTE(parms):
    mode = parms[0] #提取 parms 中的第一個字符，表示 BYTE 指令的類型，可能是 'C' 或 'X'。
    data = parms[2:-1]
    objCode = ''
    if (mode == 'C'):#if (mode == 'C'):如果 BYTE 指令的類型是 'C'，則進入這個分支。對於每個字符 i 在 data 中，使用 ord(i) 獲取其 ASCII 值，然後轉換為十六進制表示，最後使用 zfill(2) 進行填充，並添加到 objCode 中
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
    elif (mode == 'X'):# 如果 BYTE 指令的類型是 'X'，則進入這個分支。直接將 data 添加到 objCode 中
        objCode += data
    else:
        print('BYTE Error')#: 如果 BYTE 指令的類型既不是 'C' 也不是 'X'，則打印錯誤信息。

    location_add = (len(objCode)//2)#計算目標代碼的長度，除以 2 取整，得到 BYTE 指令的地址增量。
    return location_add, objCode#返回計算的地址增量和最終的目標代碼。


def WORD(parms):#def WORD(parms):: 定義了一個函數 WORD，接受一個參數 parms
    if (int(parms) >= 0):#檢查 parms 是否為非負數。如果是非負數，進入這個分支。
        objCode = Dec2Hex(int(parms)).zfill(6)# 把 parms 轉換為十六進制表示，然後用 zfill(6) 進行填充，得到長度為 6 的目標代碼。
    else:
        full_hex = Hex2Dec('1000000')#十六進制字符串 轉換為十進制。
        objCode = Dec2Hex(full_hex + int(parms)).zfill(6)#將 parms 與 full_hex 相加，然後轉換為十六進制表示，再用 zfill(6) 進行填充，得到長度為 6 的目標代碼。
    location_add = (len(objCode)//2)#計算目標代碼的長度，除以 2 取整，得到 WORD 指令的地址增量。
    return location_add, objCode#返回計算的地址增量和最終的目標代碼。
  #定義了處理 BYTE 指令的函數 BYTE


def RESB(parms):#定義了一個函數 RESB，接受一個參數 parms，用於處理 RESB 指令。
    objCode = ' '
    location_add = int(parms)#
    return location_add, objCode# 把 parms 轉換為十六進制表示，然後用 zfill(6) 進行填充，得到長度為 6 的目標代碼。


def RESW(parms):
    objCode = ' '
    location_add = (int(parms) * 3)
    return location_add, objCode


class Register():
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


register = Register()

f = open('./Input.txt', 'r')
Input = f.readlines()
f.close()

with open('./instrucetion_SICXE.json', 'r', encoding='utf-8') as j:
    instrucetion = json.load(j)

function_ = {}

temp = Input[0].replace('\n', '').split(' ')
if (len(temp) == 3):
    information = [[5, temp[2].zfill(4), temp[0], temp[1], temp[2], ' ']]
    function_[temp[0]] = Hex2Dec(information[0][4])
else:
    information = [[5, temp[2].zfill(4), '', temp[0], temp[1], ' ']]

line = 10
location = Hex2Dec(information[0][4])
for i in Input[1:]:
    line += 5

    if (i[0] == '.'):
        information.append([line, '', '.', i.replace(
            '.', '').replace('\n', ''), '', ' '])
        continue

    i = i.replace('\n', '').split(' ')

    if (len(i) == 1):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], '', ''])
    elif (len(i) == 2):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], i[1], ''])
    elif (len(i) == 3):
        information.append(
            [line, Dec2Hex(location).zfill(4), i[0], i[1], i[2], ''])

        function_[i[0]] = Dec2Hex(location).zfill(4)

    if (information[-1][3][0] == '+'):
        location += 4
    elif (information[-1][3] not in instrucetion['pseudo']):
        location += int(instrucetion['instrucetion'][information[-1][3]][1])

        if (information[-1][3] == 'CLEAR'):
            register.Clear(information[-1][4])
    else:
        if (information[-1][3] == 'BYTE'):
            location_add, objectCode = BYTE(information[-1][4])
        elif (information[-1][3] == 'RESB'):
            location_add, objectCode = RESB(information[-1][4])
        elif (information[-1][3] == 'RESW'):
            location_add, objectCode = RESW(information[-1][4])
        elif (information[-1][3] == 'WORD'):
            location_add, objectCode = WORD(information[-1][4])
        elif (information[-1][3] == 'BASE'):
            register.Load(information[-2][3], information[-2][4])
            information[-1][1] = ''
            information[-1][5] = ' '
            continue
        elif (information[-1][3] == 'END'):
            information[-1][1] = ''
            objectCode = ' '

        location += location_add
        information[-1][-1] = objectCode

register.Location_of_rigster()

for now_index, infor in enumerate(information):
    infor = infor.copy()
    next_index = now_index
    if infor[5] == '':
        if (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '2'):
            infor[4] = infor[4].split(',')
            if (len(infor[4]) == 2):
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}{num_of_register[infor[4][1]]}'
            else:
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}0'

        elif (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '3'):
            if (infor[3] == 'RSUB'):
                information[now_index][5] = '4F0000'
                continue

            next_index += 1
            while information[next_index][1] == '':
                next_index += 1

            register.PC = information[next_index][1]

            if (infor[4][0] == '@'):
                infor[4] = infor[4][1:]
                n, i = 1, 0
            elif (infor[4][0] == '#'):
                infor[4] = infor[4][1:]
                n, i = 0, 1
            else:
                n, i = 1, 1

            if ',X' in infor[4]:
                infor[4] = infor[4].replace(',X', '')
                x = 1
            else:
                x = 0

            if (infor[3][0] == '+'):
                infor[3] = infor[3][1:]
                e = 1
            else:
                e = 0

            opcode = f'{instrucetion["instrucetion"][infor[3]][0]}0'

            b, p = 0, 0
            if e:
                if (not n and i and (infor[4].isdigit())):
                    address = Dec2Hex(int(infor[4])).zfill(5)
                else:
                    address = function_[infor[4]].zfill(5)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{address}'

            else:
                if (not n and i and (infor[4].isdigit())):
                    disp = Dec2Hex(int(infor[4])).zfill(3)
                else:
                    disp = (
                        Hex2Dec(function_[infor[4]]) - Hex2Dec(register.PC))

                    if x:
                        disp -= register.X

                    if ((disp >= 4096) or ((disp <= -4096))):
                        b, p = 1, 0
                        disp = (
                            Hex2Dec(function_[infor[4]]) - Hex2Dec(register.B))

                        if x:
                            disp -= register.X
                    else:
                        b, p = 0, 1

                    if (disp < 0):
                        disp = Dec2Hex(disp + Hex2Dec('1000')).zfill(3)
                    else:
                        disp = Dec2Hex(disp).zfill(3)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{disp[-3:]}'


print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
      ('Line', 'Location', '', 'O
