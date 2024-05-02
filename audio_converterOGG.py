import ffmpeg #pip install ffmpeg-python
import os

#1конвертируем amr в ogg

folder_path_search = 'audio'
folder_path_arch = 'audio'

def convert_ogg(file):
    file_name, _ = os.path.splitext(file)
    input_file = f"{folder_path_search}/{file}"
    output_file = f"{folder_path_arch}/{file_name}.ogg"
    ffmpeg.input(input_file).output(output_file, codec='libopus', ac=1).run(overwrite_output=True)
    os.remove(input_file)
    return file_name + ".ogg"