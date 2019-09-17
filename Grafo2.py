from operator import attrgetter


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
            self.vizinhos.sort(key=lambda x: x.id,reverse=True)
    def mostra_vizinho(self):
        for i in self.vizinhos:
           print(i.id,end=',')

        print('')





class Aresta(object):
    total_arestas = 0
    identificacao = 0

    def __init__(self, vertice_a, vertice_b, peso=1,direcional=False):
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
            self.grau_media += vertice.grau;

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

    def del_vertice(self, vertice_a):
        if vertice_a in self.v_list:

            #remove o vertice dos seus  abaixa o grau dos mesmos
            for v in vertice_a.vizinhos:
                v.vizinhos.remove(vertice_a)
                v.grau += -1

            #remove o vertice da lista de grafos
            self.v_list.remove(vertice_a)

            #remove as arestas ligadas ao vertice
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

    def del_aresta(self, aresta_a):
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


    def cria_grafo(self,vertices,arestas):
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




G = Grafo()

g_vertices = ["V0","V1","V2","V3","V4"]
g_arestas = [("V0","V1"),("V0","V4"),("V1","V4"),("V1","V3"),("V3","V4"),("V1","V2"),("V2","V3")]

G.cria_grafo(g_vertices,g_arestas)

G.show_v()
G.show_a()


# H = Grafo()
#
#
# h_vertices = ["V0", "V1", "V2", "V3", "V4", "V5", "V6"]
#
# h_arestas = [("V0","V1"), ("V0","V2"), ("V1","V3"), ("V1","V4"), ("V2","V5"), ("V2","V6"),]
# H.cria_grafo(h_vertices,h_arestas)




# H.show_v()
# H.show_a()

