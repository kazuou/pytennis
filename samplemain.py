# main.py
from moduleA import A  # moduleAからクラスAをインポート
from moduleB import B  # moduleBからクラスBをインポート

# クラス A のインスタンスを作成
a = A(5, 10)

# クラス B のインスタンスを作成し、クラス A のインスタンスと追加の変数 c を渡す
b = B(a, 20)

# クラス B のメソッドで x と y を +1 する
b.increment_xy()  # 出力: x: 6, y: 11
b.increment_xy()  # 出力: x: 7, y: 12


###########################
# moduleA.py
class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y

###########################

# moduleB.py
from moduleA import A  # モジュールAからクラスAをインポート

class B:
    def __init__(self, a_instance, c):
        self.a_instance = a_instance
        self.c = c  # 追加の変数 c を初期化


    def increment_xy(self):
        self.a_instance.x += 1
        self.a_instance.y += 1
        print(f"x: {self.a_instance.x}, y: {self.a_instance.y}")

    