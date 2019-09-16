import bisect


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

    def add_vizinho(self,vertice_a):
        nset = set(self.vizinhos)
        if vertice_a not in nset:
            self.vizinhos.append(vertice_a)
            self.vizinhos.sort(key=lambda x: x.id)
    def mostra_vizinho(self):
        for i in self.vizinhos:
           print(i.id,end=',')

        print('')





class Aresta(object):
    total_arestas = 0
    identificacao = 0

    def __init__(self, vertice_a, vertice_b, peso=1):
        vertice_a.grau += 1
        vertice_b.grau += 1
        vertice_a.add_vizinho(vertice_b)
        vertice_b.add_vizinho(vertice_a)
        self.vertice_pai = vertice_a
        self.vertice_mae = vertice_b
        self.peso = peso
        self.id = Aresta.identificacao
        Aresta.identificacao += 1

    def __str__(self):
        return "Aresta %s || Entre os vertices %s e %s" % (
            self.id, self.vertice_pai.id, self.vertice_mae.id
        )


#
class Grafo(object):

    def __init__(self):
        self.v_list = []
        self.a_list = []
        self.g_list = []

    def add_vertice(self, vertice_a):
        self.v_list.append(vertice_a)
        return "Vertice adicionado"

    def add_aresta(self, aresta_a):
        self.a_list.append(aresta_a)

        if (aresta_a.vertice_pai.grau) not in self.g_list:
            bisect.insort(self.g_list, aresta_a.vertice_pai.grau)
        if (aresta_a.vertice_mae.grau) not in self.g_list:
            bisect.insort(self.g_list, aresta_a.vertice_mae.grau)
        return "Aresta adicionada"

    def del_vertice(self, vertice_a):
        if vertice_a in self.v_list:
            self.v_list.remove(vertice_a)
            for aresta in self.a_list:
                if (aresta.vertice_mae.id == vertice_a.id) or (aresta.vertice_pai.id == vertice_a.id):
                    self.a_list.remove(aresta)
            return "Vertice removido"
        else:
            return "Vertice não encontrado"

    def del_aresta(self, aresta_a):
        if aresta_a in self.a_list:
            self.a_list.remove(aresta_a)
            return "Aresta removida"
        else:
            return "Aresta não encontrada"

    def vert_adj(self, vertice_a):
        res = list()
        if vertice_a in self.v_list:
            for aresta in self.a_list:
                if (aresta.vertice_mae.id == vertice_a.id):
                    res.append(aresta.vertice_pai.id)
                if (aresta.vertice_pai.id == vertice_a.id):
                    res.append(aresta.vertice_mae.id)

            return res
        else:
            return "Vertice nao encontrado"

    def show_v(self):
        for vertice in self.v_list:
            print(vertice)

    def show_a(self):
        for aresta in self.a_list:
            print(aresta)

    def min_max(self):
        res = [self.g_list[0], self.g_list[-1]]
        return res

    def avg_deg(self):
        avg = 0
        for vertice in self.v_list:
            avg += vertice.grau
        return avg / len(self.v_list)

    def adj_matrix(self):
        edge_list = []
        edge_u = list()
        edge_v = list()

        for edge in self.a_list:
            pair = tuple(
                (edge.vertice_pai.id, edge.vertice_mae.id)
            )
            reverse = pair[::-1]
            edge_list.append(pair)
            if reverse[0] != reverse[1]:
             edge_list.append(reverse)

        for pair in edge_list:
            edge_u.append(pair[0])
            edge_v.append(pair[1])

        print(edge_u)
        print(edge_v)
        n = len(self.v_list)

        # inicializando matriz com zero
        adjMatrix = [[0 for i in range(n)] for k in range(n)]

        for i in range(len(edge_u)):
            u = edge_u[i]
            v = edge_v[i]
            adjMatrix[u][v] += 1

        for i in range(len(adjMatrix)):
            for k in range(len(adjMatrix[0])):
                print(adjMatrix[i][k], " ", end='')
            print('')
        return adjMatrix
    #Busca em profundidade


    def dfs(self,vertice_a,visitados=None):
        if visitados == None:
            visitados = []
        visitados.append(vertice_a)
        for vertice_n in vertice_a.vizinhos:
            if vertice_n not in visitados:
                self.dfs(vertice_n,visitados)
        return visitados



# V0 = Vertice("V0")
# V1 = Vertice("V1")
# V2 = Vertice("V2")
# V3 = Vertice("V3")
# V4 = Vertice("V4")
#
# A0 = Aresta(V0, V1)
# A1 = Aresta(V0, V4)
# A2 = Aresta(V1, V4)
# A3 = Aresta(V1, V3)
# A4 = Aresta(V3, V4)
# A5 = Aresta(V1, V2)
# A6 = Aresta(V2, V3)
# A7 = Aresta(V0,V0)
#
#
#
# G = Grafo()
#
# G.add_vertice(V0)
# G.add_vertice(V1)
# G.add_vertice(V2)
# G.add_vertice(V3)
# G.add_vertice(V4)
#
# G.add_aresta(A0)
# G.add_aresta(A1)
# G.add_aresta(A2)
# G.add_aresta(A3)
# G.add_aresta(A4)
# G.add_aresta(A5)
# G.add_aresta(A6)
# G.add_aresta(A7)

V0 = Vertice("V0")
V1 = Vertice("V1")
V2 = Vertice("V2")
V3 = Vertice("V3")
V4 = Vertice("V4")
V5 = Vertice("V5")
V6 = Vertice("V6")


A0 = Aresta(V0,V1)
A1 = Aresta(V0,V2)
A2 = Aresta(V1,V3)
A3 = Aresta(V1,V4)
A4 = Aresta(V2,V5)
A5 = Aresta(V2,V6)

H = Grafo()

H.add_vertice(V0)
H.add_vertice(V1)
H.add_vertice(V2)
H.add_vertice(V3)
H.add_vertice(V4)
H.add_vertice(V5)
H.add_vertice(V6)

H.add_aresta(A0)
H.add_aresta(A1)
H.add_aresta(A2)
H.add_aresta(A3)
H.add_aresta(A4)
H.add_aresta(A5)


# G.show_v()
# G.show_a()

H.show_v()
H.show_a()