from random import randint 

rand=randint(1,100)
sayac=0


while True:
    sayac+=1
    sayi=int(input("1 ila 100 arasında değerler giriniz(0 çıkış):"))
    if(sayi==0):
        print("oyunu iptal ettiniz")
        break
    elif sayi < rand:
        print("daha yüksek sayı giriniz")
        continue
    elif sayi > rand:
        print("daha düşük sayı giriniz")
        continue
    else:
        print("rastgele seçilen sayı {0}!".format(rand))
        print("tahmin sayınız {0}".format(sayac))
6
