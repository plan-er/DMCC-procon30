import json

def r_transform(path_receive):
    receive = open(path_receive,'r')
    transformed = json.load(receive)
    return transformed

#def t_transform(transmit):


if __name__ == "__main__":
    print(r_transform('フィールド情報_turn0.json'))
    print(r_transform('フィールド情報_turn1.json'))