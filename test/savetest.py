tabel = "lol"
kolommen = ["lol_id", "datum", "aantal_hareims"]
waarden = ["1", "22-02-2019", "1"]

query_pre = "INSERT INTO `%s` ("
query_middel = ") VALUES ("
query_post = ")"
for kolom in kolommen:
    query_pre += "%s, "

for waarde in waarden:
    query_middel += "%s, "

query_waarden = [tabel]
for kolom in kolommen:
    query_waarden.append(kolom)
for waarde in waarden:
    query_waarden.append(waarde)

query = query_pre[:-2] + query_middel[:-2] + query_post

cursor.execute(query, query_waarden)