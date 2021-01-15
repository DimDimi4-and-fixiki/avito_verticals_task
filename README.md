# JSON API для Avito Verticals  
**Методы сервиса:**  
* **/add_room:**  
Добавляет новый номер в базу данных.  
  Принимает на вход описание номера `description`(string) и цену за ночь `price` (float)  
  *Пример вызова с помощью `curl`:*  
  `curl -X POST "http://127.0.0.1:8000/add_room" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"description\":\"room description\",\"price\":2000}"`  
  То есть добавить комнату с описанием равным `room description` и ценой за ночь равной `2000`.  
  Такой запрос вернет результат (это просто пример, `id` может быть и другое):  
  JSON RESPONSE:  
  `{"id": 1 }`  
  
* **/get_rooms:**  
Возвращает список номеров, есть возможность задать сортировку.  
  Принимает на вход параметр сортировки (`price` или `added_at`, можно ничего не указывать, тогда сортировки просто не будет)  
  Также принимает направление сортировки (`ASC` или `DESC`)  
  *Пример работы с `curl`:*
  `curl -X GET "http://127.0.0.1:8000/get_rooms?sort_parameter=added_at&sort_direction=DESC" -H  "accept: application/json"`  
  Это запрос на получение всех комнат, отсортированных по дате добавления `added_at` в порядке убывания `DESC`  
  Результат будет такого вида:  
  `[
  {
  "room_id": 2,
  "description": "second room",
  "price": 3000,
  "added_at": "2021-01-15T18:36:50.596668"
  },
  {
  "room_id": 1,
  "description": "room description",
  "price": 2000,
  "added_at": "2021-01-15T18:21:50.343530"
  }
  ]`
  
* **/add_booking:**  
Добавить информацию о броне номера  
  Принимает на вход `room_id` номера, дату начала брони `start_date` и дату окончания брони `end_date`. Даты в формате `YYYY-MM-DD`  
  *Пример работы с `curl`:*  
  `curl -X POST "http://127.0.0.1:8000/add_booking" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"room_id\":1,\"start_date\":\"2021-01-03\",\"end_date\":\"2021-01-10\"}"`  
  Такой запрос вернет результат вида:  
  `{
  "id": 1
  }`  
* **/get_bookings:**  
Возвращает список броней для номера, отсортированные по дате начала брони  
  Принимает ID комнаты `room_id`  
  *Пример работы с `curl`:*  
  `curl -X GET "http://127.0.0.1:8000/get_bookings?room_id=1" -H  "accept: application/json"`  
  Такой запрос вернет результат вида:  
  `[
  {
  "booking_id": 1,
  "start_date": "2021-01-03",
  "end_date": "2021-01-10"
  },
  {
  "booking_id": 2,
  "start_date": "2021-01-05",
  "end_date": "2021-01-17"
  }
  ]`  
* **/delete_room:**  
Удаляет информацию о номере и его бронях 
  Принимает ID номера `room_id`  
  *Пример использования `curl`:*  
  `curl -X POST "http://127.0.0.1:8000/delete_room?room_id=1" -H  "accept: application/json" -d ""`  
  Запрос ничего не вернет в случае правильной работы, просто удалит информацию  

* **/delete_booking:**  
Удаляет информацию о броне номера  
  Принимает ID брони `booking_id`  
  *Пример использования `curl`:*  
  `curl -X POST "http://127.0.0.1:8000/delete_booking?booking_id=1" -H  "accept: application/json" -d ""`  
  Запрос удалит информацию о броне c id = 1  
  