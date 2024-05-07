import ffmpeg #pip install ffmpeg-python
import os

#1конвертируем amr в ogg

def convert_ogg(file: str, path_for_conversion: str) -> str:
    file_name, _ = os.path.splitext(file)
    input_file = f"{path_for_conversion}/{file}"
    output_file = f"{path_for_conversion}/{file_name}.ogg"
    ffmpeg.input(input_file).output(output_file, codec='libopus', ac=1).run(overwrite_output=True)
    os.remove(input_file)
    return file_name + ".ogg"

def move_to_archive(file_name: str, folder_path_search: str, folder_path_arch: str) -> None:
    source_path = os.path.join(folder_path_search, file_name)
    target_path = os.path.join(folder_path_arch, file_name)
    os.rename(source_path, target_path)

def get_audio_duration(filepath: str) -> int:
    try:
        probe = ffmpeg.probe(filepath)
        audio_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
        duration = float(audio_info['duration'])
        return duration
    except Exception as e:
        print("Ошибка при получении информации о длительности аудиофайла:", e)
        return None