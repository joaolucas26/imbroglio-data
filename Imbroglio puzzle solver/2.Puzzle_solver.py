import json
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple
import time

def load_puzzles(file_path: str) -> List[Dict]:
    """Carrega os puzzles do arquivo JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def can_form_word(letters: List[str], word: str) -> bool:
    """Verifica se uma palavra pode ser formada com as letras disponíveis"""
    letters_counter = Counter(letters)
    word_counter = Counter(word.lower())
    return all(letters_counter[letter] >= count for letter, count in word_counter.items())


def calculate_solution_score(solution_words: List[Dict]) -> int:
    """Calcula o score de uma solução usando as palavras normalizadas"""
    scores = [len(word['normalized']) ** 2 for word in solution_words]
    total = sum(scores)
    return total


def find_solutions(puzzle: Dict,
                   max_words: int = 3, 
                   time_limit: float = 7.0, 
                   max_solutions: int = 1000,
                   best_solutions: int = 15) -> List[List[Dict]]:
    """Encontra soluções para um puzzle usando as palavras já mapeadas"""
    letters = puzzle['letters']
    words = puzzle['words']
    start_time = time.time()
    
    possible_words = [word for word in words if can_form_word(letters, word['normalized'])]
    solutions = []
    used_solutions = set()    
    
    def try_combinations(remaining_letters: List[str], 
                         current_solution: List[Dict]) -> None:

        if time.time() - start_time > time_limit:
            return
            
        if not remaining_letters:
            # Verifica se a solução é única
            solution_key = tuple(sorted(word['normalized'] for word in current_solution))
            if solution_key not in used_solutions:
                solutions.append(current_solution.copy())
                used_solutions.add(solution_key)
            return
        
        if len(current_solution) >= max_words:
            return
        
        for word in possible_words:
            if can_form_word(remaining_letters, word['normalized']):
                new_remaining = remaining_letters.copy()
                for letter in word['normalized']:
                    new_remaining.remove(letter)
                
                current_solution.append(word)
                try_combinations(new_remaining, current_solution)
                current_solution.pop()
        
                if len(solutions) >= max_solutions:
                    return
    
    try_combinations(remaining_letters=letters, current_solution=[])
    
    # Ordena as soluções pelo score
    solutions.sort(key=calculate_solution_score, reverse=True)
    return solutions[:best_solutions] 

def process_puzzles(puzzles: List[Dict], num_final_solutions: int = 20) -> Dict[int, Dict]:
    """Processa todos os puzzles e retorna as soluções encontradas, sem repetição de palavras entre as soluções."""
    results = {}
    
    for puzzle in puzzles:
        puzzle_id = puzzle['id']
        print(f"\nProcessando puzzle {puzzle_id} ({puzzle['date']})...")
        start_time = time.time()
        solutions = find_solutions(puzzle, 
                                   max_words=3,
                                   time_limit=20, 
                                   max_solutions=3000,
                                   best_solutions=1000)
        end_time = time.time()

        # Filtra soluções para não repetir palavras entre elas
        used_words = set()
        filtered_solutions = []
        for solution in solutions:
            normalized_words = [word['normalized'] for word in solution]
            if all(word not in used_words for word in normalized_words):
                filtered_solutions.append(solution)
                used_words.update(normalized_words)
            if len(filtered_solutions) >= num_final_solutions:
                break

        # Calcula o score para cada solução
        solutions_with_scores = []
        for solution in filtered_solutions:
            score = calculate_solution_score(solution)
            solutions_with_scores.append({
                'words': [word['word'] for word in solution],  # Palavras originais com acentos
                'normalized_words': [word['normalized'] for word in solution],  # Palavras normalizadas
                'score': score
            })
        
        results[puzzle_id] = {
            'date': puzzle['date'],
            'letters': puzzle['letters'],
            'original_solution': puzzle['solution'],
            'found_solutions': solutions_with_scores,
            'processing_time': end_time - start_time,
            'total_solutions': len(filtered_solutions)
        }
        
        print(f"Tempo de processamento: {end_time - start_time:.2f} segundos")
        print(f"Total de soluções encontradas: {len(filtered_solutions)}")
        print(f"letras: {puzzle['letters']}")
        
        # Mostra as melhores soluções com seus scores
        if filtered_solutions:
            print(f"\nTop {num_final_solutions} melhores soluções:")
            lines = []
            for i, solution in enumerate(solutions_with_scores, 1):
                words = solution['words']
                normalized = solution['normalized_words']
                score = solution['score']
                line = f"{i}. {' + '.join(words)} (Score: {score})"
                print(line)
                lines.append(line)
            # Salva as melhores soluções de todos os puzzles em um único arquivo .txt
            txt_filename = "data/todos_top_solutions.txt"
            with open(txt_filename, 'a', encoding='utf-8') as txt_file:
                txt_file.write(f"==============================\n")
                txt_file.write(f"Puzzle ID: {puzzle_id} | Data: {puzzle['date']}\n")
                txt_file.write(f"Letras: {puzzle['letters']}\n")
                txt_file.write(f"Solução original: {' + '.join(puzzle['solution'])}\n")
                txt_file.write(f"Total de soluções encontradas: {len(filtered_solutions)}\n")
                txt_file.write(f"Top {min(15, num_final_solutions)} melhores soluções:\n")
                for line in lines[:15]:
                    txt_file.write(line + '\n')
                txt_file.write(f"==============================\n\n")
            print(f"Top 15 melhores soluções adicionadas em: {txt_filename}")
    
    return results

def save_results(results: Dict[int, Dict], output_file: str) -> None:
    """Salva os resultados em um arquivo JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResultados salvos em: {output_file}")

def main():
    # Carrega os puzzles
    puzzles = load_puzzles('data/daily_puzzles_6_with_words.json')
    
    # Processa os puzzles
    num_final_solutions = 20
    results = process_puzzles(puzzles, num_final_solutions=num_final_solutions)
    
    # Salva os resultados
    save_results(results, 'data/daily_puzzles_6_with_words_and_solutions2.json')

if __name__ == "__main__":
    main() 
    