import redis
from parser import parseTsv

r = redis.Redis()
d = parseTsv("sample_edges.tsv", "sample_nodes.tsv")

for key in d.keys():
    r.mset({str(key): str(d[key])})

# Please modify this so that the user can query the disease id.
val = input("PLEASE TYPE A DISEASE ID: ") 
print(r.get(val)) # "Disease::DOID:0050156"