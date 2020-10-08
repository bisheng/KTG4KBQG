import networkx as nx

g = nx.Graph()

qa_train = "D:\\数据\\KBQG\\SimpleQuestions_v2\\SimpleQuestions_v2\\SimpleQuestions_v2\\annotated_fb_data_train.txt"
qa_test = "D:\\数据\\KBQG\\SimpleQuestions_v2\\SimpleQuestions_v2\\SimpleQuestions_v2\\annotated_fb_data_test.txt"
qa_valid = "D:\\数据\\KBQG\\SimpleQuestions_v2\\SimpleQuestions_v2\\SimpleQuestions_v2\\annotated_fb_data_valid.txt"

mqa = "D:\\数据\\KBQG\\30MQA\\30MQA_1\\fqFiltered.txt"
freebase = "D:\\数据\\freebase-rdf-latest\\freebase-rdf-latest"


def g_demo():
    f_train = open(qa_train, "r", encoding="utf-8")
    f_test = open(qa_test, "r", encoding="utf-8")
    f_valid = open(qa_valid, "r", encoding="utf-8")
    nodes = set()
    count = 0
    for line in f_train.readlines():
        try:
            count += 1
            elems = line.split("\t")

            nodes.add(elems[0].split("/m/")[1].replace(">", ""))
            nodes.add(elems[2].split("/m/")[1].replace(">", ""))

            g.add_edges_from([(elems[0].split("/m/")[1].replace(">", ""), elems[2].split("/m/")[1].replace(">", ""))])
        except:
            print(line)

    for line in f_test.readlines():
        try:
            count += 1
            elems = line.split("\t")

            nodes.add(elems[0].split("/m/")[1].replace(">", ""))
            nodes.add(elems[2].split("/m/")[1].replace(">", ""))

            g.add_edges_from([(elems[0].split("/m/")[1].replace(">", ""), elems[2].split("/m/")[1].replace(">", ""))])
        except:
            print(line)

    for line in f_valid.readlines():
        try:
            count += 1
            elems = line.split("\t")

            nodes.add(elems[0].split("/m/")[1].replace(">", ""))
            nodes.add(elems[2].split("/m/")[1].replace(">", ""))

            g.add_edges_from([(elems[0].split("/m/")[1].replace(">", ""), elems[2].split("/m/")[1].replace(">", ""))])
        except:
            print(line)

    # node_0 = "04whkz5"
    # for node in nodes:
    #     if nx.has_path(g, node_0, node):
    #         print(node)

    print("三个集合共有节点：", len(nodes))
    print("共有边：", g.number_of_edges())
    print("共有三元组：", count)

    largest_components = max(nx.connected_components(g), key=len)
    print("最大子图：", largest_components)
    print("最大子图节点数：", len(largest_components))

    count = 0
    for subg in nx.connected_components(g):
        if len(subg) > 2:
            count += 1
        # print(subg)
    print("共有子图数量：", count)


def get_freebase():
    f = open(freebase, "r", encoding="utf-8")
    line = f.readline()
    count = 0
    while line and count < 5000:
        print(line)
        count += 1
        line = f.readline()


def how_ask():
    h_entity = set()
    t_entity = set()

    wiki_entity = set([line.split()[0].split("/m.")[1].replace(">", "") for line in
                       open("D:\\数据\\freebase2wikidata\\fb2w.nt", "r", encoding="utf-8").readlines()])

    for line in open(qa_train, "r", encoding="utf-8").readlines():
        elems = line.split("\t")
        h_entity.add(elems[0].split("/m/")[1])
        t_entity.add(elems[2].split("/m/")[1])

    print("头实体数量：", len(h_entity))
    print("尾实体数量：", len(t_entity))

    print("头实体交集：", len(wiki_entity & h_entity))
    print("尾实体交集：", len(wiki_entity & t_entity))

def write_nt():
    # wikidata


if __name__ == "__main__":
    g_demo()
