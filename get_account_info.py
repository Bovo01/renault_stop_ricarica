import aiohttp
from asyncio import get_event_loop
from json import load as json_load

from renault_api.renault_client import RenaultClient



async def main():
    with open('pass.json', 'r') as f:
        private_infos = json_load(f)
    async with aiohttp.ClientSession() as websession:
        client = RenaultClient(websession=websession, locale="it_IT")
        try:
            await client.session.login(private_infos['email'], private_infos['pass'])
        except:
            print("Devi inserire email e password validi nel file pass.json")
            exit(1)
        
        account = await client.get_api_account(private_infos['account_id'])
        try:
            vehicles = await account.get_vehicles()
        except:
            accounts = (await client.get_person()).accounts
            print(f'Sono presenti {len(accounts)} account, con id : {" ; ".join([account.accountId for account in accounts])}')
            exit(1)

        try:
            vehicle = await account.get_api_vehicle(private_infos['vin'])
            print(await vehicle.get_details())
        except:
            print(f'Sono presenti {len(vehicles.vehicleLinks)} veicoli, con : {" ; ".join([f"{{modello: {vehicle.vehicleDetails.model.label}, vin: {vehicle.vin}}}" for vehicle in vehicles.vehicleLinks])}')
            exit(1)

        print('Hai configurato correttamente i tuoi dati personali')
        exit(0)


loop = get_event_loop()
loop.run_until_complete(main())