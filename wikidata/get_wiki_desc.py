from wikidata.client import Client
import datetime

# 根据wikidata的id获取到对应的其label、description、instanceof
file_type = "test"
print(file_type)
wikidata = open(file_type + "_new.txt", encoding="utf-8")

wikidata_desc_cate = open("wikidata_desc_cate_" + file_type + ".txt", mode="a", encoding="utf-8")
print("start doing...")
j = 0

client = Client()
for i, line in enumerate(wikidata.readlines()):
    elems = line.split("	")
    e_1 = elems[0].split("entity/")[1].replace(">", "")
    e_2 = elems[2].split("entity/")[1].replace(">", "")
    for e in [e_1, e_2]:
        try:
            entity = client.get(e)
            # print("got entity..")
            label = str(entity.label)
            entity_attr = entity.attributes
            if "P31" in str(entity_attr):
                # print("there is P31")
                cate_id = entity.attributes.get("claims").get("P31")[0].get("mainsnak").get("datavalue").get(
                    "value").get(
                    "id")
                cate = str(client.get(cate_id).description)
            elif "P279" in str(entity_attr):
                # print("there is P279")
                cate_id = entity.attributes.get("claims").get("P279")[0].get("mainsnak").get("datavalue").get(
                    "value").get(
                    "id")
                cate = str(client.get(cate_id).description)
            else:
                print(e)
                cate = "<unk>"
            wikidata_desc_cate.write(
                e + "###" + str(label + "###" + str(entity.description) + "###" + cate).lower() + "\n")
            j = i
        except:
            print("something wrong." + e_1 + "#" + e_2)
            pass

print("END, total " + str(j))
wikidata.close()
wikidata_desc_cate.close()
print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
