prijsplafond = [  # maand, kWh, m3, dagen in maand
    [1, 339, 221, 31],
    [2, 280, 188, 28],
    [3, 267, 159, 31],
    [4, 207, 86, 30],
    [5, 181, 35, 31],
    [6, 159, 19, 30],
    [7, 161, 17, 31],
    [8, 176, 17, 31],
    [9, 199, 24, 30],
    [10, 266, 81, 31],
    [11, 306, 147, 30],
    [12, 356, 207, 31],
]

def check_prijsplafond_lijst():
    prijsplafond_kWh_jaar_totaal = 2897  # 2900
    prijsplafond_m3_jaar_toaal = 1201  # 1200

    prijsplafond_kWh_jaar = 0
    prijsplafond_m3_jaar = 0
    for maand_plafond in prijsplafond:
        prijsplafond_kWh_jaar += maand_plafond[1]
        prijsplafond_m3_jaar += maand_plafond[2]
    if prijsplafond_kWh_jaar != prijsplafond_kWh_jaar_totaal or prijsplafond_m3_jaar != prijsplafond_m3_jaar_toaal:
        print(f'FOUT IN TABEL PRIJSPLAFOND')
        return False

    return True
