from main.datas.ingredients import INGREDIENTS
from tests.utils import work_with_json_BETA as wwjb

txt = ''
com_exit = 'выход' # команда для выхода
fp = 'datas/'
fn = 'words_singularity.json'
singularity_dict = wwjb.read_from_json(folderpath=fp,filename=fn)

for group in INGREDIENTS.keys():
    for i in range(len(INGREDIENTS.get(group)) - 1):
        txt = txt + ' ' + INGREDIENTS.get(group)[i]
        txt = txt.lower()
txt_list = txt.split()

for slovo in txt_list:
    print(slovo+' --> '+str(singularity_dict.get(slovo)))
    singularity = input()
    if not singularity in ['q','',com_exit]:
        singularity_dict[slovo] = singularity
        wwjb.save_as_json(singularity_dict, filename=fn, folderpath=fp, overwrite=False)
    if singularity == com_exit:
        print(wwjb.save_as_json(singularity_dict, filename=fn, folderpath=fp,overwrite=False))


