import json
from collections import Counter

def can_form_word(letters, word):
    letters_counter = Counter(letters)
    
    word_counter = Counter(word.lower())
    for letter, count in word_counter.items():
        if letters_counter[letter] < count:
            return False
    return True


def find_possible_words(letters, words_data):
    possible_words = []
    for word_obj in words_data:
        if can_form_word(letters, word_obj['normalized']):
            possible_words.append(word_obj)
    possible_words.sort(key=lambda x: (-len(x['word']), x['word']))
    
    return possible_words



def main():
    with open('data/daily_puzzles_6.json', 'r', encoding='utf-8') as f:
        puzzles = json.load(f)
    
    with open('data/words.json', 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    for puzzle in puzzles:
        print(f"\nPuzzle {puzzle['id']} ({puzzle['date']})")
        print(f"Letras: {', '.join(puzzle['letters']).upper()}")
        
        possible_words = find_possible_words(puzzle['letters'], words_data)        
        puzzle['words'] = possible_words        
        
        print(f"Total de palavras: {len(possible_words)}")        
        if possible_words:  
            longest_word = max(possible_words, key=lambda x: len(x['word']))
            print(f"Maior palavra: {longest_word['word']} ({len(longest_word['word'])} letras)")
    
    output_file = 'data/daily_puzzles_6_with_words.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, ensure_ascii=False, indent=2)      
        
    print(f"\nArquivo salvo em: {output_file}")

if __name__ == "__main__":
    main()