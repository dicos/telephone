Если номер в поле "SIP" - неизвестен, звонок входящий, известен - звонок исходящий либо внутренний.
Известный номер - это внутренний номер типа 100, или номер на который устаовленна переадресация, на скринах везде это мой номер 79271028738.
Смотрим куда звонили, если номер неизвестный - значит звонок исходящий, если номер известный - звонок внутренний. Если запись многострочная - ищем строчку с Incoming определяем её статус - если неотвечен, значит звонок неотвеченый, если разговор - находим вторую строку со статусом разговор и и берём из неё номер ответа.


[3:10:08 PM | Edited 3:12:17 PM] Анатолий Кузнецов: Находим строку вида АТС - Номер А
[3:15:56 PM] Анатолий Кузнецов: Если этой строке не соответствует ни одна запись во второй таблице, значит это 100% калбек и должна быть ещё одна строка в интервале 15 секунд. Строка может быть двух видов  либо вида АТС-номер Б при этом ей должна обезательно соответствовать запись входящем звонке во второй таблице с упоминанием номера А и Б.
[3:17:34 PM] Анатолий Кузнецов: Второй вид строки Номер А - Номер Б,может вообще не иметь записи во втрой таблице либо иметь запись о входящем.
[3:19:48 PM] Анатолий Кузнецов: Если этой записи вида АТС - Номер А соответствует запись запись воходящем звонке во второй таблице, значит это тоже калбек, но второй строки в первой таблице он не имеет.
[3:20:57 PM] Анатолий Кузнецов: Если этой записи соответствует запись о исходящем звонке во втрой таблице, значит это обычный исходящий звонок.
[3:22:41 PM] Анатолий Кузнецов: При этом если запись второй таблица определяется как внутренний звонок, значит калбек является внутренним звонком. Тоже касается и исходящего звонка.
[3:25:36 PM] Анатолий Кузнецов: Понятно?
[3:26:13 PM] Dmitry Shepelev: как-то проще оказалось сложней)
[3:26:41 PM] Анатолий Кузнецов: В чём сложность?)
[3:29:35 PM] Dmitry Shepelev: в осознании этого всего)
[3:29:59 PM | Edited 3:42:36 PM] Анатолий Кузнецов: Если строка имеет вид АТС - номер, начинаем проверку не является ли она калбеком. калбеком она является в двух случаях.
[3:30:47 PM] Анатолий Кузнецов: Если ей нет соответствия во второй таблице, значит двустрочный калбек.
[3:31:32 PM] Анатолий Кузнецов: Если соответствие есть, это входящий. значит однострочный калбек.
[3:32:04 PM] Анатолий Кузнецов: Если соответствие есть - и это исходящий, значит это не калбек, а обычный исходящий звонок.
[3:34:05 PM] Dmitry Shepelev: ну вот. так проще) гораздо
[3:34:08 PM] Dmitry Shepelev: понятнее)
[3:36:49 PM] Анатолий Кузнецов: При первом варианте: двустрочный калбек. Он бывает двух видов в котором вторая строка(фактически она первая) имеет вид АТС - Номер Б, находим её её должна соответствовать запись о входящем звонке в которой содержится номер А. Если это так - значит всё это колбек(исходящий)
[3:40:40 PM | Edited 3:40:51 PM] Анатолий Кузнецов: Второй вид двустрочного калбека, это у которого вторая строка имеет вид Номер А - Номер Б, при этом эта страка может иметь соответствующий входящий во второй таблице, может не иметь. Если имеет, то записи должны упоминатся номера  А и Б.
[3:44:02 PM] Анатолий Кузнецов: Второй вариант и третий подробно описывать не стоит, там всё понятно.
[3:45:29 PM] Анатолий Кузнецов: тут ещё нужен алгоритм определения внутренних колбеков, боюсь писать, ты запутаешься)
[3:49:30 PM] Анатолий Кузнецов: В общем если в описаном выше алгоритме соответствующая запись во второй таблице определена как внутренний звонок, значит калбек имеет статус не исходящий, а внутренний.
