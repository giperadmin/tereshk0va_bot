import tests.utils.work_with_json_BETA as wwj

file_names = ['words_adjective.json',
              'words_salats.json',
              'words_letter.json',
              'words_stars_constellation.json'
              ]
fp = '../datas/'
for fn in file_names:
    data = wwj.read_from_json(folderpath=fp, filename=fn)
    data = list(data.keys())
    print(data)
    fn = fn.replace('words','list')
    fp = '../datas/'
    wwj.save_as_json(data, filename=fn, folderpath=fp)

