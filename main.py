import time
import multiprocessing
import random
import json

with open('config.json', encoding='UTF-8') as f:
    config = json.load(f)['config']


def lap(distance, veh, return_dict, i, repairTime):
    print(veh['vehType'])
    if veh['vehType'] == 'Мотоцикл':
        print(f"""Транспортное средство №{veh['id']} Тип транспортного средства: {veh['vehType']}
скорость транспортного средства: {veh['speed']}
вероятность прокола колеса: {veh['probabilityWheelPuncture']}
Коляска: {str(veh['wheelchair']).replace('false','Отсутствует').replace('True','Имеется')}""")
    elif veh['vehType'] == 'Грузовик':
        print(f"""Транспортное средство №{veh['id']} Тип транспортного средства: {veh['vehType']}
скорость транспортного средства: {veh['speed']}
вероятность прокола колеса: {veh['probabilityWheelPuncture']}
Вес груза: {veh['weight']}""")
    elif veh['vehType'] == 'Легковой автомобиль':
        print(f"""Транспортное средство №{veh['id']} Тип транспортного средства: {veh['vehType']}
скорость транспортного средства: {veh['speed']}
вероятность прокола колеса: {veh['probabilityWheelPuncture']}
Количество пассажиров: {veh['passengers']}""")

    while distance > 0:
        prob = random.choices(['Прокол', 'Нет'], weights=[veh['probabilityWheelPuncture'], 1-veh['probabilityWheelPuncture']])
        if prob[0] == 'Нет':
            print(f"Транспортное средство номер {veh['id']} расстояние до финиша {distance} м.\n")
            distance -= veh['speed']
            time.sleep(1)
        else:
            print(f"Транспортное средство номер {veh['id']} пробило колесо расстояние до финиша {distance} м.\n")
            time.sleep(repairTime)
    else:
        print(f"Транспортное средство {veh['id']} прибыло к финишу\n")
        return_dict[i] = str(veh['id'])


if __name__ == '__main__':
    while True:
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs = []
        for i in range(len(config['vehicles'])):
            p = multiprocessing.Process(target=lap, args=(config['distance'], config['vehicles'][i], return_dict, i, config['repairTime']))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()
        leaderBoard = return_dict.values()
        for i in range(len(leaderBoard)):
            print(f'Автомобиль номер {leaderBoard[i]} занял {i+1} место')
        if input('Повторить заезд? (y/n)') == 'n':
            break
