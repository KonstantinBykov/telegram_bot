### Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

### Берем токен который вы получили от BotFather
API_TOKEN = 'YOUR_BOT_TOKEN'

### Объект бота
bot = Bot(token=API_TOKEN)
### Диспетчер
dp = Dispatcher()

### Зададим имя базы данных
DB_NAME = 'quiz_bot.db'



### Создаем сборщика клавиатур типа Inline, в цикле создаем 4 Inline кнопки, а точнее Callback-кнопки

        def generate_options_keyboard(answer_options, right_answer):
            builder = InlineKeyboardBuilder()
            for option in answer_options:
                builder.add(types.InlineKeyboardButton(
                    text=option,
                    callback_data="right_answer" if option == right_answer else "wrong_answer")
                )
        
            builder.adjust(1)
            return builder.as_markup()

### Перехватчик колбэк запросов "right_answer"
        @dp.callback_query(F.data == "right_answer")
        async def right_answer(callback: types.CallbackQuery):
            # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
            await callback.bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )
        
            await callback.message.answer("Верно!")
            current_question_index = await get_quiz_index(callback.from_user.id)
            # Обновление номера текущего вопроса в базе данных
            current_question_index += 1
            await update_quiz_index(callback.from_user.id, current_question_index)
        
        
            if current_question_index < len(quiz_data):
                await get_question(callback.message, callback.from_user.id)
            else:
                await callback.message.answer("Это был последний вопрос. Квиз завершен!")


### Перехватчик колбэк запросов "wrong_answer"
        @dp.callback_query(F.data == "wrong_answer")
        async def wrong_answer(callback: types.CallbackQuery):
            await callback.bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )
        
            # Получение текущего вопроса из словаря состояний пользователя
            current_question_index = await get_quiz_index(callback.from_user.id)
            correct_option = quiz_data[current_question_index]['correct_option']
        
            await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
        
            # Обновление номера текущего вопроса в базе данных
            current_question_index += 1
            await update_quiz_index(callback.from_user.id, current_question_index)
        
        
            if current_question_index < len(quiz_data):
                await get_question(callback.message, callback.from_user.id)
            else:
                await callback.message.answer("Это был последний вопрос. Квиз завершен!")


### Хэндлер на команду /start
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

### Запрашиваем из базы вопрос
    async def get_question(message, user_id):
    
        # Получение текущего вопроса из словаря состояний пользователя
        current_question_index = await get_quiz_index(user_id)
        correct_index = quiz_data[current_question_index]['correct_option']
        opts = quiz_data[current_question_index]['options']
        kb = generate_options_keyboard(opts, opts[correct_index])
        await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

### Здесь мы из сообщения узнаем пользователя, сбрасываем счетчик вопросов в 0, и запрашиваем асинхронно следующий вопрос для отправки пользователю в чат.
    async def new_quiz(message):
        user_id = message.from_user.id
        current_question_index = 0
        await update_quiz_index(user_id, current_question_index)
        await get_question(message, user_id)

### Запрашиваем из базы текущий индекс для вопроса
    async def get_quiz_index(user_id):
         # Подключаемся к базе данных
         async with aiosqlite.connect(DB_NAME) as db:
            # Получаем запись для заданного пользователя
            async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
                # Возвращаем результат
                results = await cursor.fetchone()
                if results is not None:
                    return results[0]
                else:
                    return 0

### Функция, которая создаст запись в таблице quiz_state
    async def update_quiz_index(user_id, index):
        # Создаем соединение с базой данных (если она не существует, она будет создана)
        async with aiosqlite.connect(DB_NAME) as db:
            # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
            await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
            # Сохраняем изменения
            await db.commit()


### Хэндлер на команду /quiz
    @dp.message(F.text=="Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
    
        await message.answer(f"Давайте начнем квиз!")
        await new_quiz(message)


### Создание таблицы
    async def create_table():
        # Создаем соединение с базой данных (если она не существует, она будет создана)
        async with aiosqlite.connect(DB_NAME) as db:
            # Создаем таблицу
            await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
            # Сохраняем изменения
            await db.commit()



### Запуск процесса поллинга новых апдейтов
    async def main():
    
        # Запускаем создание таблицы базы данных
        await create_table()
    
        await dp.start_polling(bot)
    
    if __name__ == "__main__":
        asyncio.run(main())
