import eel
import sqlite3

# Инициализация Eel
eel.init("web")

# Подключение к базе данных SQLite
def db_start():
    global conn, cur
    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY, 
                        note TEXT, 
                        text TEXT)""")
        conn.commit()
        print("База данных успешно инициализирована.")
    except sqlite3.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        raise

# Функция для добавления заметки
@eel.expose
def add_note(note, text=""):
    try:
        cur.execute("INSERT INTO notes (note, text) VALUES (?, ?)", (note, text))
        conn.commit()
        print(f"Заметка '{note}' добавлена.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении заметки: {e}")

# Функция для получения всех заметок с их ID
@eel.expose
def get_notes():
    try:
        cur.execute("SELECT id, note FROM notes")
        notes = cur.fetchall()
        print(f"Заметки загружены: {notes}")
        return [{'id': note[0], 'note': note[1]} for note in notes]
    except sqlite3.Error as e:
        print(f"Ошибка при получении заметок: {e}")
        return []

# Функция для удаления заметки по ID
@eel.expose
def delete_note(note_id):
    try:
        cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        print(f"Заметка с ID {note_id} удалена.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении заметки: {e}")

# Функция для получения полного текста заметки по ID
@eel.expose
def get_note_text(note_id):
    try:
        cur.execute("SELECT text FROM notes WHERE id=?", (note_id,))
        result = cur.fetchone()
        return result[0] if result else ''
    except sqlite3.Error as e:
        print(f"Ошибка при получении текста заметки: {e}")
        return ''

# Функция для обновления текста заметки
@eel.expose
def update_note_text(note_id, new_text):
    try:
        cur.execute("UPDATE notes SET text=? WHERE id=?", (new_text, note_id))
        conn.commit()
        print(f"Заметка с ID {note_id} обновлена.")
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении заметки: {e}")

# Закрытие соединения с базой данных
def close_db():
    try:
        conn.close()
        print("Соединение с базой данных закрыто.")
    except sqlite3.Error as e:
        print(f"Ошибка при закрытии базы данных: {e}")

# Запуск базы данных
db_start()

# Запуск веб-интерфейса
eel.start("index.html", size=(1000, 800), block=False)

# Закрытие базы данных при завершении приложения
@eel.expose
def on_close():
    print("Закрытие приложения...")
    close_db()
    exit()

# Используем правильный метод sleep
while True:
    eel.sleep(10)
