from datetime import datetime
from colored import fg, attr

import meterstanden_lijst
import prijsplafond_lijst


# ==================================================================================================================
def green(text):
    return f"{fg('green')}{text}{attr('reset')}"


# ==================================================================================================================
def yellow(text):
    return f"{fg('yellow')}{text}{attr('reset')}"


# ==================================================================================================================
def blue(text):
    return f"{fg('light_blue')}{text}{attr('reset')}"


# ==================================================================================================================
def green_yellow(text):
    return f"{fg('green_yellow')}{text}{attr('reset')}"


# ==================================================================================================================
def red(text):
    return f"{fg('red')}{text}{attr('reset')}"


# ==================================================================================================================
def print_green(text, end=None):
    if end == None:
        print(green(text))
    else:
        print(green(text), end=end)


# ==================================================================================================================
def print_yellow(text, end=None):
    if end == None:
        print(yellow(text))
    else:
        print(yellow(text), end=end)


# ==================================================================================================================
def print_blue(text, end=None):
    if end == None:
        print(blue(text))
    else:
        print(blue(text), end=end)


# ==================================================================================================================
def print_green_yellow(text, end=None):
    if end == None:
        print(green_yellow(text))
    else:
        print(green_yellow(text), end=end)


# ==================================================================================================================
def print_red(text, end=None):
    if end == None:
        print(red(text))
    else:
        print(red(text), end=end)


# ==================================================================================================================
def verschil(stand_oud, stand_nieuw):

    datetime_oud = datetime.strptime(stand_oud[0], '%d-%m-%Y %H:%M')
    datetime_nieuw = datetime.strptime(stand_nieuw[0], '%d-%m-%Y %H:%M')

    aantal_dagen = datetime_nieuw - datetime_oud
    aantal_dagen = aantal_dagen.days + aantal_dagen.seconds / (60 * 60 * 24)

    if stand_nieuw[1] and stand_oud[1]:
        verschil_en = stand_nieuw[1] - stand_oud[1]
    else:
        verschil_en = 0

    if stand_nieuw[2] and stand_oud[2]:
        verschil_et = stand_nieuw[2] - stand_oud[2]
    else:
        verschil_et = 0

    if stand_nieuw[3] and stand_oud[3]:
        verschil_g = stand_nieuw[3] - stand_oud[3]
    else:
        verschil_g = 0

    return aantal_dagen, verschil_en, verschil_et, verschil_g


# ==================================================================================================================
def main():

    if not prijsplafond_lijst.check_prijsplafond_lijst():
        exit(-1)

    meterstanden = meterstanden_lijst.meterstanden
    prijsplafond = prijsplafond_lijst.prijsplafond

    meterstanden = [stand for stand in meterstanden if stand[0] != '']

    start_meter_stand = None
    vorige_meter_stand = None
    for stand_index, meter_stand in enumerate(meterstanden):

        if not meter_stand[0]:
            continue

        print_yellow(f'{meter_stand[0]:12s}', end='')
        print_blue(f'{meter_stand[1]:6d} kWh ', end='')
        print_blue(f'{meter_stand[2]:6d} kWh ', end='')
        print_green_yellow(f'{meter_stand[3]:10.3f} m3 ', end='')
        print_yellow(f'{meter_stand[4]:7s} ', end='')

        if vorige_meter_stand:

            dagen, en, et, g = verschil(vorige_meter_stand, meter_stand)
            print_yellow(f' >> {dagen:4.1f} d ', end='')
            print_blue(f'netto {en - et:3d} kWh ({en:3d}-{et:3d}) | {(en - et) / dagen:4.1f} kWh/dag ', end='')
            print_green_yellow(f'{g:4.1f} m3 | {g / dagen:4.1f} m3/dag ', end='')

        vorige_meter_stand = meter_stand

        maand_nr = 0
        if meter_stand[4] == 'periode':
            # nieuwe maand
            dag_nr = int(meter_stand[0].split('-')[0])
            maand_nr = int(meter_stand[0].split('-')[1])
            if dag_nr < 5:
                # deze meterstand is al in de nieuwe periode, neem plafond van vorige maand
                if maand_nr == 1:
                    maand_nr = 12
                else:
                    maand_nr = maand_nr - 1

        elif stand_index == len(meterstanden) - 1:
            # einde van meterstanden lijst
            maand_nr = int(meter_stand[0].split('-')[1])

        if maand_nr and start_meter_stand:

            dagen, en, et, g = verschil(start_meter_stand, meter_stand)
            if dagen:
                if meter_stand[4] == 'periode':
                    print_yellow(f' >> HELE PERIODE {maand_nr:02d} {dagen:4.1f} d ', end='')
                else:
                    print_yellow(f' >> DEEL PERIODE    {dagen:4.1f} d ', end='')
                print_blue(f'{en - et:6.1f} kWh ', end='')
                print_blue(f'{(en - et) / dagen:5.1f} kWh/dag', end='')
                print_green_yellow(f'{g:6.1f} m3 ', end='')
                # print_yellow(f'({en / dagen:4.1f} kWh/dag - {et / dagen:4.1f} kWh/dag) = ', end='')
                print_green_yellow(f'{g / dagen:5.1f} m3/dag ', end='')

                periode_dagen = prijsplafond[maand_nr - 1][3]
                schatting_kwh = ((en - et) / dagen) * periode_dagen
                schatting_m3 = (g / dagen) * periode_dagen
                if meter_stand[4] == 'periode':
                    print_yellow(f'\n{" ":132s} >> CORRECTIE      {periode_dagen:5.1f} d ', end='')
                else:
                    print_yellow(f'\n{" ":132s} >> SCHATTING      {periode_dagen:5.1f} d ', end='')

                print_blue(f'{schatting_kwh:6.1f} kWh/periode ', end='')
                print_green_yellow(f'     {schatting_m3:6.1f} m3/periode', end='')

                prijsplafond_kwh = prijsplafond[maand_nr - 1][1]
                prijsplafond_m3 = prijsplafond[maand_nr - 1][2]
                print_yellow(f'\n{" ":132s} >> PRIJSPLAFOND           ', end='')
                print_blue(f'{prijsplafond_kwh:6.1f} kWh/periode      ', end='')
                print_green_yellow(f'{prijsplafond_m3:6.1f} m3/periode', end='')

                verschil_kwh = schatting_kwh - prijsplafond_kwh
                verschil_m3 = schatting_m3 - prijsplafond_m3
                print_yellow(f'\n{" ":132s}                           -----------------------------------------')
                print_yellow(f'{" ":132s} >> VERSCHIL               ', end='')
                if verschil_kwh <= 0:
                    print_green(f'{verschil_kwh:6.1f} kWh/periode      ', end='')
                else:
                    print_red(f'{verschil_kwh:6.1f} kWh/periode      ', end='')
                if verschil_m3 <= 0:
                    print_green(f'{verschil_m3:6.1f} m3/periode', end='')
                else:
                    print_red(f'{verschil_m3:6.1f} m3/periode', end='')

        if meter_stand[4] == 'periode':
            start_meter_stand = meter_stand

        print()


# ==================================================================================================================
if __name__ == '__main__':
    main()
