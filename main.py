from aiohttp import ClientSession
from asyncio import new_event_loop, set_event_loop
from json import load as json_load
from time import sleep
from datetime import datetime, timedelta
from traceback import format_exc

from renault_api.renault_client import RenaultClient
from renault_api.kamereon.enums import PlugState
from renault_api.renault_vehicle import RenaultVehicle
from renault_api.kamereon.models import ChargeSchedule, ChargeDaySchedule

from logger import log as logger_log


with open('options.json', 'r') as f:
    options = json_load(f)
# Limite di carica
LIMIT_PERCENTAGE = options['limite_percentuale']
# Schedule che va modificata dal programma che blocca la ricarica
SCHEDULE_INDEX = options['schedule_utilizzato']
# Tempo di sleep tra una richiesta e l'altra
_1_MINUTE = 60
SLEEP_TIME = _1_MINUTE * options['frequenza_aggiornamento']
# Formato data per logs
STRING_FORMAT = '%Y%m%d_%H.%M'


async def main():
    with open('pass.json', 'r') as f:
        private_infos = json_load(f)

    while True:
        try:
            async with ClientSession() as websession:
                # Login
                client = RenaultClient(websession=websession, locale="it_IT")
                await client.session.login(private_infos['email'], private_infos['pass'])
                # Get account
                account = await client.get_api_account(private_infos['account_id'])
                # Get vehicle
                vehicle = await account.get_api_vehicle(private_infos['vin'])

                print('Programma avviato. Non chiudere questa finestra altrimenti il programma verrà arrestato.')
                # Program execution
                await stay_awake(vehicle)
        except BaseException as e:
            print(e)
        finally:
            sleep(SLEEP_TIME)


async def stay_awake(vehicle: RenaultVehicle):
    global LIMIT_PERCENTAGE, SLEEP_TIME

    DATE_STRING = datetime.now().strftime(STRING_FORMAT)
    PERCENTAGE_ERROR = options['errore_percentuale']
    while True:
        try:
            if LIMIT_PERCENTAGE > 0: # Condition to be active
                batteryStatus = await vehicle.get_battery_status()
                if batteryStatus.get_plug_status() == PlugState.PLUGGED:
                    if batteryStatus.batteryLevel < LIMIT_PERCENTAGE - (PERCENTAGE_ERROR if LIMIT_PERCENTAGE < 80 else PERCENTAGE_ERROR / 2):
                        await vehicle.set_charge_mode('always_charging')
                    else:
                        await block_charge(vehicle)
                else:
                    await vehicle.set_charge_mode('always_charging')

        except BaseException as e:
            logger_log(DATE_STRING, STRING_FORMAT, format_exc(e))
        except:
            logger_log(DATE_STRING, STRING_FORMAT, 'Unknown error occured')
            raise
        finally:
            sleep(SLEEP_TIME)



def set_all_schedules(schedule: ChargeSchedule, daySchedule: ChargeDaySchedule):
    schedule.monday = daySchedule
    schedule.tuesday = daySchedule
    schedule.wednesday = daySchedule
    schedule.thursday = daySchedule
    schedule.friday = daySchedule
    schedule.saturday = daySchedule
    schedule.sunday = daySchedule

async def block_charge(vehicle: RenaultVehicle):
    global SCHEDULE_INDEX

    OFFSET = 60
    DURATION = OFFSET / 2
    chargeMode = await vehicle.get_charging_settings()
    schedules = chargeMode.schedules

    now = (datetime.now() - timedelta(minutes=OFFSET)).strftime("T%H:%MZ")

    dailySchedule = ChargeDaySchedule(raw_data={'startTime': now, 'duration': DURATION}, startTime=now, duration=DURATION)

    editableSchedule = schedules[SCHEDULE_INDEX]
    set_all_schedules(editableSchedule, dailySchedule)
    schedules[SCHEDULE_INDEX] = editableSchedule
    await vehicle.set_charge_schedules(schedules)

if __name__ == '__main__':
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()