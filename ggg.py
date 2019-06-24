KKK = 100
MMM = 200

class main:
    # global KKK
    # global MMM
    def __init__(self):
        # global KKK, MMM
        self.sss = 50
    def change(self):
        global KKK, MMM
        KKK += 1
        MMM += 1
        print(KKK)
        print(MMM)

print(KKK)
print(MMM)
aa=main()
aa.change()
