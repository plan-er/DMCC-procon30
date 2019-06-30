import json

def r_transform(path_receive):
    receive = open(path_receive,'r')
    transformed = json.load(receive)
    return transformed

def t_transform(path_transmit,actions):
    with open(path_transmit,'w') as f:
        json.dump(actions,f,indent=4)                

if __name__ == "__main__":
    print(r_transform('フィールド情報_turn0.json'))
    print(r_transform('フィールド情報_turn1.json'))