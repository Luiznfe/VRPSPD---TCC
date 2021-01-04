class Teste:

    def teste_leitura(self):
        arq = open('C:/Users/luizn/Documents/GitHub/VRPSPD---TCC/c0530.txt')

        for linha in arq:
            print(linha)
            break

if __name__ == '__main__':
    t = Teste()
    t.teste_leitura()