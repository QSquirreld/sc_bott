from typing import Optional
from aiogram import types
from aiogram.filters import BaseFilter


class AccessChecker(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        username = message.from_user.username
        if not username:
            await self.handle_no_access(message)
            return False
            
        try:
            with open('data/whitelist.txt', 'r', encoding='utf-8') as file:
                allowed_users = [
                    line.strip() 
                    for line in file 
                    if line.strip() and not line.startswith('#')
                ]
                if f"@{username}" in allowed_users:
                    return True
                    
            await self.add_to_waitlist(message)
            await self.handle_no_access(message)
            return False
            
        except FileNotFoundError:
            print("Файл whitelist.txt не найден")
            return False

    async def add_to_waitlist(self, message: types.Message):
        try:
            username = f"@{message.from_user.username}"
            user_id = message.from_user.id # user_id не будет меняться, наверное лучше использовать его
            
            with open('data/wait_list.txt', 'a', encoding='utf-8') as file:
                file.write(f"{username},{user_id}\n")
        except Exception as e:
            print(f"Ошибка при добавлении в wait_list: {e}")

    async def handle_no_access(self, message: types.Message):
        await message.answer(
            "Бот находится в стадии тестирования.\n"
            "Мы уведомим Вас, когда бот станет доступен для всех пользователей!"
        )
