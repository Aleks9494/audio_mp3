Для запуска:
 - создать в корне проекта папку logs
 - docker-compose build
 - docker-compose up 
 - docker-compose exec app alembic upgrade head

В папке file находится файл для тестирования

Пример запроса:
 - api/v1/create_user. Тип application/json. Метод Post с телом json: 
{
  "username": "User1" (тип string)
}

 - api/v1/upload_wav. Тип mupltipart/from-data. Метод Post с данными формы: 
file - "загрузить файл"  (тип UploadFile),
user_id - 1              (тип int),
user_token - a5fb5b62-7fb6-4264-b6a2-5c810e95a2b   (тип UUID4)

 - api/v1/record. Метод GET с параметрами пути.
id - 8e6661c0-80de-4e67-8382-f1aae802d07e   (тип UUID4)
user - 1              (тип int)

Пример ответа:
 - api/v1/create_user:
{
  "success": true,
  "id": 1 (тип int),
  "token": a5fb5b62-7fb6-4264-b6a2-5c810e95a2b (тип UUID4)
}

 - api/v1/upload_wav:
{
  "success": true,
  "url": "http://0.0.0.0:8010/api/v1/record?id=ce7b3472-55cb-444d-bfa2-49b056671b05&user=3" (тип HttpUrl)
}

 - api/v1/record:
Ответ с кодом 200 и возможностью скачать файл в SWAGGER.

Для входа в контейнер с БД:
 - docker-compose exec -it db bash
 - psql -U postgres
 - \connect audio

Для доступа в SWAGGER:
 - http://0.0.0.0:8010/docs
