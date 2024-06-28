'''
						   _               _       _              
						  | |             | |     | |             
  _ __   ___ _ __ ___  ___| |__   ___  ___| | __ _| |_ ___  _ __  
 | '_ \ / _ \ '__/ _ \/ __| '_ \ / _ \/ __| |/ _` | __/ _ \| '__| 
 | |_) |  __/ | |  __/ (__| | | |  __/\__ \ | (_| | || (_) | |    
 | .__/ \___|_|  \___|\___|_| |_|\___||___/_|\__,_|\__\___/|_|    
 | |                       | |                                    
 |_|_  __ _ _ __ ___  _ __ | | ___                                
 / __|/ _` | '_ ` _ \| '_ \| |/ _ \                               
 \__ \ (_| | | | | | | |_) | |  __/                               
 |___/\__,_|_| |_| |_| .__/|_|\___|                               
					 | |                                          
					 |_|                                          
'''



import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled

from aiogram.types import InputFile 

import string, random


bot = Bot(token='TOKEN', parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

from pytonapi import Tonapi
from pytonapi.utils import nano_to_amount


###### Ton

# Api ключ
API_KEY = "your_api"  # noqa
ACCOUNT_ID = "your_wallet_address"  # noqa
wallet = '2-1391203'




async def anti_flood(*args, **kwargs):
	m = args[0]
	await m.answer("⚠Не так быстро!")

@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood,rate=0.01)
async def start(msg: types.Message):
    tonapi = Tonapi(api_key=API_KEY)
    result = tonapi.blockchain.get_account_transactions(account_id=ACCOUNT_ID, limit=1000)
    random_comment = [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in range(10)]

    await msg.answer(wallet)

    async for transaction in result.transactions:
        print(transaction)
        print(f"Отправленно TON: {nano_to_amount(transaction.in_msg.value)}\n")

        if transaction.in_msg.decoded_op_name == random_comment:
            print(f"Комментарий: {transaction.in_msg.decoded_body['text']}")
            await msg.delete()
            await msg.answer('Успешно!!')
    
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
