# CustomLaTeXBot [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/fatmaann/CustomLaTeXBot/blob/main/README.en.md)<br>
<b>Курсовая работа - Генератор документации «Mentors Joy».<br>
Telegram - бот для создания PDF ГОСТ документации для сдачи дипломных и курсовых работ</b>.

## Актуальность

Документы часто содержат недостающие страницы, ошибки в шаблонах, неправильные отступы - полное непонимание основных элементов, необходимых для надлежащей
документации в курсовом / дипломном проекте.<br><br>В ответ на эту широко распространенную проблему был разработан `Telegram - бот`,
который предоставляет пользователям возможность воспользоваться конструктором для генерации `LaTeX` документов на основе заданных шаблонов формата `JSON`. После заполнения формы, на основе введённой информации и шаблона программа генерирует итоговый
`PDF` и присылает его пользователю.

## Архитектура Telegram - бота

### Основная библиотека - <a href="https://aiogram.dev"><em><b>Aiogram</b></em></a>

В данном проекте обработка обратных вызовов (<em>Callback Handling</em>) играет важную роль в взаимодействии пользователя и бота `Telegram`.
Обратный вызов — это взаимодействие, которое происходит, когда пользователь нажимает на кнопку со встроенной клавиатуры.
Все взаимодействие с пользователем до заполнения шаблона происходит с помощью встроенной клавиатуры.
<br>С помощью неё выбирается формат будущего документа, а также настраиваются главы и под главы.

<table align="center">
  <tr>
    <th colspan="3" align="left"">Выберите один из форматов:<br><br>1) Руководство оператора<br>2) Руководство программиста<br>3) Техническое задание<br>4) Пояснительная записка<br>5) Программа и методика испытаний<br>6) Текст программы<br><br></th>
  </tr>
  <tr>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="center">3</td>
  </tr>
  <tr>
    <td align="center">4</td>
    <td align="center">5</td>
    <td align="center">6</td>
  </tr>
  <tr>
    <th colspan="3" align="center">Назад</th>
  </tr>
</table>
<div align="center"><i>Определение плана документа</i></div><br>

<table align="center">
  <tr>
    <th colspan="2" align="left"">Структура документа:<br>❌ Титульный лист<br>❌ Аннотация<br>✅ Назначение программы<br>✅ Условие выполнение программы<br>✅ Выполнение программы<br>✅ Сообщения оператору<br>❌ Перечень терминов и сокращений<br><br>Если в начале строки стоит ✅, вы можете настроить (добавить или удалить) под главы в этой главе.<br>Главы со знаком ❌ не являются гибкими с точки зрения количества под глав.<br><br>Выберите главы, которые вы хотите изменить в документе, нажав соответствующие кнопки ниже.<br>Иначе можете сразу создать документ по выбранному формату.</th>
  </tr>
  <tr>
    <td align="center">Изменить</td>
    <td align="center">Создать</td>
  </tr>
  <tr>
    <th colspan="2" align="center">Назад</th>
  </tr>
</table>
<div align="center"><i>Меню выбора будущего формата документа</i></div><br>

Бот также принимает сообщения для заполнения выбранного шаблона - сообщения, содержащие файлы
формата `JSON`, используемвые для компиляции их в формат `PDF`.</b>

### Команды сервиса

* `/start` - команда, определяющее начало взаимодействия с ботом.
* `/main_menu` - команда, позволяющая быстро переместить к основному
меню интерфейса бота.
* `/choose_format` - команда, позволяющая быстро переместить к меню
выбора будущего формата документа.
* `/send_file` - команда, позволяющая быстро переместить к основному меню
отправки `JSON` формата.
* `/help` - команда, позволяющая получить сообщение с краткой поясняющей
информацией по боту.

### Хостинг 

<b><a href="https://ngrok.com/docs"><em>Ngrok</em></a></b> — мощный инструмент, который упрощает безопасное туннелирование
для доступа к локальным серверам в Интернете.<br>Позволяет временные общедоступные `URL-адреса` для доступа к своим локально размещенным приложениям или службам.<br>
Эта возможность оказывается особенно полезной при разработке веб-приложений или работе с веб-перехватчиками в таких средах, как <b><em>Aiogram</em></b>.

<b><em>Ngrok</em></b> предоставляет безопасный общедоступный `URL-адрес`, который перенаправляет входящие запросы из `Telegram` локальному боту <b><em>Aiogram</em></b>.


## Управление пользовательскими данными

Сервис предоставляет пользователю гибкий выбор по настройке будущего документа.<br>Необходимо продумать <ins><i>быструю и надёжную</i></ins> систему хранения пользовательских данных,<br>для отслеживания всех изменений, которые сделал
пользователь на пути к созданию файла.<br>Данные <ins><i>должны быть временными</i></ins>, так как нет необходимости хранить данные о пользователе, если он не возвращается.<br>
<b><br>Для такой цели отлично подходит системы базы данных <a href="https://redis.io"><em>Redis</em></a></b>.<br>

<b><em>Redis</em></b> предоставляет уникальную функцию, известную как `«expire»`. С помощью
этой функции разработчики могут установить время жизни (`TTL`) для каждой пары ключзначение в <b><em>Redis</em></b>. По истечении `TTL` <b><em>Redis</em></b> <i><ins>автоматически удаляет данные</i></ins> из базы
данных.<br><br>
<i><ins>Удаление или очищение</i></ins> профиля пользователя происходит, как только пользователю приходит готовый `PDF`, при выходе в главное
меню, а также при отсутствии взаимодействия программы с пользователем на протяжении
<i><ins>12 часов</i></ins>.<br><br>

## Компиляция PDF - документов

<b><a href="https://jeltef.github.io/PyLaTeX/latest/pylatex/pylatex.document.html"><em>PyLatex</em></a></b> - python библиотека, которая предоставляет удобный и интуитивно
понятный способ программного создания файлов `LaTeX`.

### Особенности и преимущества <b><em>Pylatex</b></em>
* Документ приобретает <b><i>сложную структуру</i></b>, включая разделоы, отделения, абзацы и многое другое.
* <b><i>Форматирование и стиль</i></b> - доступ к различным параметрам форматирования<br>(стили шрифтов, цвета, макеты страниц и настраиваемые колонтитулы и тд).
* <b><i>Математический набор</i></b> - использование выражений, символов, матриц и других математических конструкций.
* <b><i>Библиография и цитаты</i></b> - интеграция с BibTeX, что позволяет легко управлять библиографией и цитатами в документах `LaTeX`.
* <b><i>Вставка</i></b> изображений, таблиц и визуальных элементов в документы `LaTeX`.<br>

После заполнения объекта класса документа с помощью <b><em>PyLatex</em></b> общаемся к <ins><b>pdflatex.exe</b></ins> для компиляции `LaTeX` документа в `PDF`.

<b><em>PDF LaTeX</em></b> — расширение системы набора текста `LaTeX`, специально ориентированное на создание вывода в формате `PDF`.<br>
Файл <ins><b>pdflatex.exe</b></ins> является частью дистрибутивов: <b>MiKTeX, TeX Live, MacTeX</b>.<br>
