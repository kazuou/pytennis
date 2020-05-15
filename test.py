class Character:
    """キャラクターーオブジェクト"""
    def __init__(self):
        self.status = 0
        self.x = 999
        self.y = 0
        self.z = 0

    def on(self, x = 0, y = 0,z=10):
        self.status = 1
        self.x = x
        self.y = y
        self.z = z

def drowc(x):
    print(len(x))
    for i in x :
        print ("x=",i.x,"y=",i.y,"z=",i.z)
        

def drowx(x):
    print(x)
    print(len(x))
    for i in x :
        print(i)
        a,b = i
        print("a=",a,"b=",b)



def main():
    """ メインルーチン """
    print("HelloWorld")
    print("Hi")
    character = [Character() for i in range(50)]
    for i in range(len(character)):
        character[i].status = 0

    #自分を表示する
    character[0].on(10,11,0)
    character[1].on(20,21,0)
    character[2].on(30,31,0)
    character[3].on(40,41,0)

    #x=((10,11),(20,21))
    #drowx(x)
    x = (character[0],character[1])
    drowc(x)



if __name__ == '__main__':
    main()
