# read_translated_message.py

# Read the translated message from the file
def translation_result():
    with open('translated_message.txt', 'r') as file:
        translated_message = file.read()
        print(f'Translated Message: {translated_message}')
        return translated_message


