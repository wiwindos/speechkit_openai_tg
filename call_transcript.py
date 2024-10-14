import sqlite3
from typing import Optional

def add_data_to_audio_files(phone_number: str, upload_date: str, duration: float, filepath: str) -> int:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    # upload_date (str): Дата загрузки в формате 'YYYY-MM-DD HH:MM:SS'
    c.execute("INSERT INTO AudioFiles (phone_number, upload_date, duration, filepath) VALUES (?, ?, ?, ?)", (phone_number, upload_date, duration, filepath))
    audio_file_id = c.lastrowid
    conn.commit()
    conn.close()
    return audio_file_id

def add_text_data(text: str, audio_file_id: int, conversion_date: str) -> int:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    c.execute("INSERT INTO TextData (text, audio_file_id, conversion_date) VALUES (?, ?, ?)", (text, audio_file_id, conversion_date))
    text_data_file_id = c.lastrowid
    conn.commit()
    conn.close()
    return text_data_file_id

def add_analysis_result(text_data_id: int, analysis_result: str, analysis_date: str) -> None:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    c.execute("INSERT INTO AnalysisResults (text_data_id, analysis_result, analysis_date) VALUES (?, ?, ?)", (text_data_id, analysis_result, analysis_date))
    conn.commit()
    conn.close()
def get_all_audio_files() -> str:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    c.execute("SELECT * FROM AudioFiles")
    data = c.fetchall()
    conn.close()
    return data

def get_all_text_data_files() -> str:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    c.execute("SELECT * FROM TextData")
    data = c.fetchall()
    conn.close()
    return data

def get_all_analysis_result_files() -> str:
    conn = sqlite3.connect('call_transcript.db')
    c = conn.cursor()
    c.execute("SELECT * FROM AnalysisResults")
    data = c.fetchall()
    conn.close()
    return data

def get_text_by_audioFileId(audio_file_id:int) -> Optional[str]:
    try:
        conn = sqlite3.connect('call_transcript.db')
        c = conn.cursor()
        c.execute("SELECT text FROM TextData WHERE audio_file_id = ?", (audio_file_id,))
        data = c.fetchone()

        if data:
            return data[0]  # Возвращаем значение text
        else:
            return None  # Если значение не найдено

    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
        return None

    finally:
    # Закрываем соединение с базой данных
        if conn:
            conn.close()

def get_analysis_result_by_AnalysisResults(text_data_file_id:int) -> Optional[str]:
    try:
        conn = sqlite3.connect('call_transcript.db')
        c = conn.cursor()
        c.execute("SELECT analysis_result FROM AnalysisResults WHERE text_data_id = ?", (text_data_file_id,))
        data = c.fetchone()

        if data:
            return data[0]  # Возвращаем значение text
        else:
            return None  # Если значение не найдено

    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
        return None

    finally:
    # Закрываем соединение с базой данных
        if conn:
            conn.close()


# text_data_files = get_all_text_data_files()
# print(text_data_files)
# audio_files = get_all_audio_files()
# print(audio_files)
# analysis_result_files = get_all_analysis_result_files()
# print(analysis_result_files)

