import json

def remove_words():
    # Read the remove_words.json file
    with open('data/remove_words.json', 'r', encoding='utf-8') as remove_file:
        words_to_remove = json.load(remove_file)
    
    ids_to_remove = {word['id'] for word in words_to_remove}
        
    with open('data/words.json', 'r', encoding='utf-8') as words_file:
        words = json.load(words_file)
            
    filtered_words = [word for word in words if word['id'] not in ids_to_remove]
    
    with open('data/words.json', 'w', encoding='utf-8') as output_file:
        json.dump(filtered_words, output_file, ensure_ascii=False, indent=2)
    
    print(f"Removed {len(words) - len(filtered_words)} words from words.json")
    print(f"Original count: {len(words)}")
    print(f"New count: {len(filtered_words)}")

if __name__ == "__main__":
    remove_words() 