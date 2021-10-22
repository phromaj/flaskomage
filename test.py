# toto = 'Massif de l’Aubrac (Aveyron, Cantal et Lozère)'
# yaya = toto.split('(')[1]
# char_to_remove = [",", "et", ")"]
# for i in char_to_remove:
#     yaya = yaya.replace(i, '')
# yaya = yaya.split(' ')
# for y in yaya:
#     if y == "":
#         yaya.remove(y)
# print(yaya)

# d = "Aveyron, Cantal et Lozère"
# chars_to_remove = [",", "et"]
# for i in chars_to_remove:
#     d = d.replace(i, '')
# final_result = d.split(' ')
# for y in final_result:
#     if y == "":
#         final_result.remove(y)
# print(final_result)

fromage = {
    "nom": "fefe",
    "departement": "fef",
    "dwd": "dwd"
}
keys = ["nom", "departement", "annee_aoc", "pate", "lait"]
hasKey = True
for key in fromage.keys():
    if not key in keys:
        hasKey = False
if(hasKey):
    print("ok")
        
