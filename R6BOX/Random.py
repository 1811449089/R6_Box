'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2026-06-01 19:09:02
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2026-06-01 20:29:34
FilePath: \R6BOX\Random.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
ATK=["Sledge","Thatcher","Ash","Thermite","Twitch","Montagne","Glaz","Fuze","Blitz","IQ","Buck"
             ,"Blackbeard","Capitao","Hibana","Jackal","Ying","Zofia","Dokkaebi","Lion","Finka","Maverick",
             "Nomad","Gridlock","Nøkk","Amaru","Kali","Iana","Ace","Zero","Flores","Osa","Sens","Brava","Ram"
             ,"Deimos","Rauora","Solid Snake"]
DEF=["Smoke","Mute","Castle","Pulse","Doc","Rook","Kapkan","Tachanka","Jager","Bandit","Frost",
             "Valkyrie","Caveira","Echo","Mira","Lesion","Ela","Vigil","Maestro","Alibi","Clash",
             "Kaid","Mozzie","Warden","Goyo","Wamai","Oryx","Melusi","Aruni","Thunderbird","Azami","Solis"
             ,"Fenrir","Thron","Tubarão","Skopós","Denari"]
def Random(side):
    if side=="Attacker":
        return random.choice(ATK)
    elif side=="Defender":
        return random.choice(DEF)

def main():
    while  True:
        side=input("请选择你的阵营（Attacker/Defender）,输入'0'退出：") 
        if side == '1' or side.lower() == 'attacker' or side.lower() == 'a' or side.lower() == 'atk' or side.startswith('攻'):
            side = 'Attacker'
        elif side == '2' or side.lower() == 'defender' or side.lower() == 'd' or side.lower() == 'def' or side.startswith('防') or side.startswith('守'):
            side = 'Defender'
        elif side == '0':
            print("退出程序。")
            break
        else:
            print("输入无效，请重新选择。")
            continue
        operator = Random(side)
        print(f"你选择了{side}，随机分配的干员是：{operator}")

if __name__ == "__main__":   
    main()