from json_creator import save_as_json
txt=''
data={}
while txt!='q':
    txt = input()
    norm_txt = txt.strip().lower()
    norm_txt = norm_txt.replace('"','')
    data[norm_txt]=''
print(str(data.keys()))
save_as_json(data,filename='words_salats.json',folderpath='datas/',overwrite=True)