from operator import attrgetter
from bisect import bisect_left


def busca_binaria(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


def printMatrix(matrix):
    for i in range(len(matrix)):
        for k in range(len(matrix[0])):
            print(matrix[i][k], " ", end='')
        print('')


class Vertice(object):
    total_vertices = 0
    identificacao = 0

    def __init__(self, nome):
        self.nome = nome
        self.id = Vertice.identificacao
        Vertice.identificacao += 1
        self.grau = 0
        self.vizinhos = list()

    def __str__(self):
        return "Vertice: %s || Grau: %s || Identificação: %s" % (self.nome, self.grau, self.id)

    def add_vizinho(self, vertice_a):
        nset = set(self.vizinhos)
        if vertice_a not in nset:
            self.vizinhos.append(vertice_a)
            self.vizinhos.sort(key=lambda x: x.id, reverse=True)

    def mostra_vizinho(self):
        for i in self.vizinhos:
            print(i.id, end=',')

        print('')


class Aresta(object):
    total_arestas = 0
    identificacao = 0

    def __init__(self, vertice_a, vertice_b, peso=1, direcional=False):
        vertice_a.grau += 1
        if vertice_a.id != vertice_b.id:
            vertice_b.grau += 1
        vertice_a.add_vizinho(vertice_b)
        vertice_b.add_vizinho(vertice_a)
        self.vertice_pai = vertice_a
        self.vertice_mae = vertice_b
        self.peso = peso
        self.id = Aresta.identificacao
        self.direcional = direcional
        Aresta.identificacao += 1

    def __str__(self):
        return "Aresta %s || Entre os vertices %s e %s" % (
            self.id, self.vertice_pai.id, self.vertice_mae.id
        )


#
class Grafo(object):
    grau_media = 0
    grau_min = 0
    grau_max = 0

    def __init__(self):
        self.v_list = []
        self.a_list = []

    def calc_medias(self):
        for vertice in self.v_list:
            self.grau_media += vertice.grau

        self.grau_media = self.grau_media / len(self.v_list)

        self.grau_min = min(self.v_list, key=attrgetter('grau'))
        self.grau_max = max(self.v_list, key=attrgetter('grau'))

    def add_vertice(self, vertice_a):
        self.v_list.append(vertice_a)
        self.calc_medias()
        return "Vertice adicionado"

    def add_aresta(self, aresta_a):
        self.a_list.append(aresta_a)
        return "Aresta adicionada"

    def _del_vertice(self, vertice_a):
        if vertice_a in self.v_list:

            # remove o vertice dos seus  abaixa o grau dos mesmos
            for v in vertice_a.vizinhos:
                v.vizinhos.remove(vertice_a)
                v.grau += -1

            # remove o vertice da lista de grafos
            self.v_list.remove(vertice_a)

            # remove as arestas ligadas ao vertice
            remover = []
            for aresta in self.a_list:
                if (aresta.vertice_mae.id == vertice_a.id) or (aresta.vertice_pai.id == vertice_a.id):
                    remover.append(aresta)
            for aresta in remover:
                self.a_list.remove(aresta)

            self.calc_medias()
            return "Vertice removido"
        else:
            return "Vertice não encontrado"

    def del_vertice(self, id):
        id_list = [x.id for x in self.v_list]
        posicao = busca_binaria(id_list, id)

        if posicao == -1:
            res = 'Vertice nao encontrado'
        else:
            res = self._del_vertice(self.v_list[posicao])
        return res

    def _del_aresta(self, aresta_a):
        if aresta_a in self.a_list:
            for vertice in self.v_list:
                if (vertice.id == aresta_a.vertice_mae.id) or (vertice.id == aresta_a.vertice_pai.id):
                    vertice.grau += -1
                if (vertice.id == aresta_a.vertice_mae.id):
                    vertice.vizinhos.remove(aresta_a.vertice_pai)
                if (vertice.id == aresta_a.vertice_pai.id and aresta_a.vertice_pai.id != aresta_a.vertice_mae.id):
                    vertice.vizinhos.remove(aresta_a.vertice_mae)

            self.a_list.remove(aresta_a)
            self.calc_medias()
            return "Aresta removida"
        else:
            return "Aresta não encontrada"

    def del_aresta(self, id):
        id_list = [x.id for x in self.a_list]
        x = bisect_left(id_list, id)
        res = 0
        if x != len(id_list) and id_list[x] == id:
            res = self._del_aresta(self.a_list[x])
        return res

    def cria_grafo(self, vertices, arestas):
        v_dict = {}

        for v in vertices:
            v_dict[v] = Vertice(v)
            self.add_vertice(v_dict[v])
        for a in arestas:
            v1, v2 = a
            vertice_a = v_dict[v1]
            vertice_b = v_dict[v2]
            self.add_aresta(Aresta(vertice_a, vertice_b))

    def show_v(self):
        for vertice in self.v_list:
            print(vertice)

    def show_a(self):
        for aresta in self.a_list:
            print(aresta)

    def show_all(self):
        self.show_v()
        self.show_a()

    def adj_matrix(self):
        n = len(self.v_list)

        adjMatrix = [[0 for i in range(n)] for k in range(n)]

        for i, u in enumerate(self.v_list):
            u_vizinhos = [x.id for x in u.vizinhos]

            for j, v in enumerate(self.v_list):
                if v.id in u_vizinhos:
                    adjMatrix[i][j] += 1

        printMatrix(adjMatrix)

    # Busca em profundidade
    def _dfs(self, vertice_a, visitados=None):
        if visitados == None:
            visitados = []
        visitados.append(vertice_a)
        for vertice_n in vertice_a.vizinhos:
            if vertice_n not in visitados:
                self._dfs(vertice_n, visitados)
        return visitados

    def dfs(self,id_vertice):
        id_list = [x.id for x in self.v_list]
        x = bisect_left(id_list, id_vertice)
        res = []
        if x != len(id_list) and id_list[x] == id_vertice:
            res = self._dfs(self.v_list[x])
        else:
            res = 'vertice nao encontrado'
        return res

    def conexo(self):
        res = self.dfs(0)
        return len(res) == len(self.v_list)

    def is_euler(self):
        n_grau_impar = 0
        euler = False
        for v in self.v_list:
            if v.grau % 2:
                n_grau_impar += 1
            if n_grau_impar >2:
                break
        if (n_grau_impar == 0 or n_grau_impar == 2) and self.conexo():
            euler = True

        return euler

G = Grafo()

g_vertices = ["V0", "V1", "V2", "V3", "V4"]
g_arestas = [("V0", "V1"), ("V0", "V4"), ("V1", "V4"), ("V1", "V3"), ("V3", "V4"), ("V1", "V2"), ("V2", "V3")]

G.cria_grafo(g_vertices, g_arestas)

G.show_all()

# H = Grafo()
#
#
# h_vertices = ["V0", "V1", "V2", "V3", "V4", "V5", "V6"]
#
# h_arestas = [("V0","V1"), ("V0","V2"), ("V1","V3"), ("V1","V4"), ("V2","V5"), ("V2","V6"),]
# H.cria_grafo(h_vertices,h_arestas)


# H.show_v()
# H.show_a()
