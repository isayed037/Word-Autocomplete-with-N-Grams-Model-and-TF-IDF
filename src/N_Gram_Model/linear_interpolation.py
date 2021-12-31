'''
Take a trigram model and total words counts.
For any given 2 words, stores the probabilities of the 3rd word in a max heap. 
'''

from heapq import heappop, heappush, heapify

class Calculate_Linear_Interpolation:
    def __init__(self, unigram, bigram, trigram, words_count, END_SYMBOL="<STOP>", START_SYMBOL='<*>') -> None:
        # Class variables
        self.unigram = unigram
        self.bigram = bigram
        self.trigram = trigram
        self.words_count = words_count
        self.end_symbol = END_SYMBOL
        self.start_symbol = START_SYMBOL
        
        self.words = None
        self.heap = None
    
    def probability(self, word, word2, word1):
        '''
        Return the probability of q(word|word2, word1)
        Return the probability of "word2 word1 word" apperaing in a sentence
        '''
        lambda_1 = 0.8
        lambda_2 = 0.15
        lambda_3 = 0.05
        
        # Trigram maximum-likelihood estimate:
        trigram_numerator_key = f'{word2} {word1} {word}'
        trigram_denominator_key = f'{word2} {word1}'
        numerator = self.trigram.get(trigram_numerator_key, 0)
        denominator = self.bigram.get(trigram_denominator_key, 0)
        if numerator == 0 or denominator == 0: 
            trigram_likelihood = 0
        else:
            trigram_likelihood = lambda_1 * (numerator / denominator)
        
        # Bigram maximum-likelihood estimate:
        bigram_numerator_key = f'{word1} {word}'
        numerator = self.bigram.get(bigram_numerator_key, 0)
        denominator = self.unigram.get(word1, 0)
        if numerator == 0 or denominator == 0: 
            bigram_likelihood = 0
        else:
            bigram_likelihood = lambda_2 * (numerator / denominator)
        
        # Unigram maximum-likehood estimate:
        numerator = self.unigram.get(word, 0)
        denominator = self.words_count
        if numerator == 0 or denominator == 0: 
            unigram_likelihood = 0
        else:
            unigram_likelihood = lambda_3 * (numerator / denominator)
        
        # Linear Interpolation:
        probability = trigram_likelihood + bigram_likelihood + unigram_likelihood
        
        return probability
    
    def show_next_word(self, name, show_top, word1, word2):
        '''
        Given 2 words, predicts the next word. Prints the word and the probability
        '''
        
        print(f'\n\tUsing "{name}" trigram model for this linear interpolation')
        
        self.predict_next_words(word1, word2)
        
        self.print_word_and_probability(show_top, word1, word2)
    
    def predict_next_words(self, word2, word1):
        """
        Goes through all the words in the unigram and calculates the probability of that word appearing after "word2 word1". 
        Stores the probability of the words appearing in a max heap.
        Uses the self.words dict() to store the probability as it's keys and a list of word with that probability for it's values.
        """
        self.words = {}
        self.heap = []
        heapify(self.heap)
        
        for key in self.unigram:
            probability = self.probability(key, word2, word1)
            
            heappush(self.heap, -1 * probability)
            if probability in self.words:
                self.words[probability].append(key)
            else:
                self.words[probability] = [key]
    
    def print_word_and_probability(self, show_top, word1, word2):
        """
        Prints the word and probability with the highest probability.
        """
        if not self.heap or not self.words: return
        
        print(f'\n\tThe next word after: "{word1} {word2} ()" is:')
        
        while self.heap:
            if show_top == 0: break
            
            p, word = self.get_highest_probabilities()
            p = round(p, 4)
            
            # We don't want to show the END_SYMBOL or START_SYMBOL, this way it will always suggest a word
            if word != self.end_symbol and word != self.start_symbol:
                print(f'\t\t"{word1} {word2} ({word})", with probability: {p*100}%\n')
                show_top -= 1
    
    def get_highest_probabilities(self):
        """
        Returns the word and probability with the highest probability.
        Removes those words and probability from the heap and self.words values.
        """
        probability = -1 * heappop(self.heap)
        
        words_list = self.words[probability]
        word = words_list.pop()
         
        return probability, word
    
    