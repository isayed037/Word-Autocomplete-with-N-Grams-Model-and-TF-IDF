'''
Given a 2d list of sentence and all words in the sentence, it count all words, unigram, bigram, and trigram.
"*" and "STOP" are special symbols to represents the start and end of a sentence and must be give when the class is initialized.
'''

class Trigram_Model:
    def __init__(self, model_name="", start_symbol="<*>", end_symbol="<STOP>") -> None:
        # Class variables
        self.model_name = model_name
        
        self.START_SYMBOL = start_symbol
        self.END_SYMBOL = end_symbol
        
        # All words count including all "end_symbol"
        self.all_words_count = 0
        
        # Keys are 'word word word' and values are counts
        self.trigram_count = dict()
        
        # Keys are 'word word' and values are counts
        self.bigram_count = dict()
        
        # Keys are 'word' and values are counts
        self.unigram_count = dict()
    
    def get_model_information(self):
        """ 
        Returns a list with current models information where:
        list[0] = model_name
        list[1-3] = unigram, bigram, trigram
        list[4] = all_words_count
        """
        info = [self.model_name, self.unigram_count, self.bigram_count, self.trigram_count, self.all_words_count]
        
        return info
    
    def add_sentences_to_model(self, sentences):
        """
        Takes a 2d list of all sentence and words. Counts and adds unigram, bigram, and trigram to the model.
        """
        for sentence in sentences:
            self.update_model_with_sentence(sentence)
    
    def update_model_with_sentence(self, sentence):
        """
        Takes a list of words that represents one sentences.
        When calculating the trigram model adds "START_SYMBOL START_SYMBOL" to the start of the sentence.
        """
        previous_word = self.START_SYMBOL
        previous_2nd_word = self.START_SYMBOL
                
        for index, word in enumerate(sentence):
            # Unigram counts and all words count(including all self.END_SYMBOL)
            self.all_words_count += 1
            self.unigram_count[word] = self.unigram_count.get(word, 0) + 1
            
            # Bigram and trigram counts
            if index == 0:
                self.add_one_bigram_trigram(previous_2nd_word, previous_word, word)
                
                previous_word = word
            else:
                self.add_one_bigram_trigram(previous_2nd_word, previous_word, word)
                
                previous_2nd_word = previous_word
                previous_word = word

    def add_one_bigram_trigram(self, second_previous, previous, word):
        bigram_key = f'{previous} {word}'
        self.bigram_count[bigram_key] = self.bigram_count.get(bigram_key, 0) + 1
        
        trigram_key = f'{second_previous} {previous} {word}'
        self.trigram_count[trigram_key] = self.trigram_count.get(trigram_key, 0) + 1
    
    def add_all_counts(self, unigram_count, bigram_count, trigram_count, all_words_count):
        """
        Takes unigram_count, bigram_count, and trigram_count where key is the n-gram and value is the count.
        Takes all_words_count which is int and is the count of all words.
        Adds all of these to the trigram model.
        """
        self.all_words_count += all_words_count
        
        for word, count in unigram_count.items():
            self.unigram_count[word] = self.unigram_count.get(word, 0) + count
        
        for bigram, count in bigram_count.items():
            self.bigram_count[bigram] = self.bigram_count.get(bigram, 0) + count
        
        for trigram, count in trigram_count.items():
            self.trigram_count[trigram] = self.trigram_count.get(trigram, 0) + count
            
    def save_model_to_file(self, paths_to_all_files):
        """
        Saves this trigram model to a txt file based on path_to_file path.
        """  
        if self.model_name not in paths_to_all_files: return  
        
        # Get the output file path for the current model
        current_trigram_model_file_path = paths_to_all_files[self.model_name]
            
        # Create a file and save it to where the output file path is.
        with open(current_trigram_model_file_path, 'w') as output_file:
            line = "<MODEL_NAME>" + '\t' + str(self.model_name) + '\n'
            output_file.write(line)  
            
            self.save_n_gram_to_file(output_file)
            
            line = "<MODEL_WORD_COUNT>" + '\t' + str(self.all_words_count)
            output_file.write(line)  
             
            
            print(f'\t\t- Added "{self.model_name}" model to the file "{current_trigram_model_file_path}"')
    
    def save_n_gram_to_file(self, output_file):
        """
        Saves this models unigram, bigram, and trigram counts to the output_file
        """
        for word, count in self.unigram_count.items():
            line = word + '\t' + str(count) + '\n'
            
            output_file.write(line)
        
        for bigram, count in self.bigram_count.items():
            line = bigram + '\t' + str(count) + '\n'
            output_file.write(line)
        
        for trigram, count in self.trigram_count.items():
            line = trigram + '\t' + str(count) + '\n'
            output_file.write(line)
            
    def get_model_from_file(self, file_path):
        """
        Gets the trigram model from the file_path. Adds the unigram, bigram, trigram, model name, and model word count from the file to the current Trigram_Model object.
        """
        with open(file_path) as file:
            for line in file:
                self.model_from_file(line)
                
        return self.model_name
    
    def model_from_file(self, line):
        """
        Takes one line from the trigram model file. Splits the line and adds all the information from the line to the current instance.
        """
        n_gram = line.split("\t")
        line = line.split()
        line_length = len(line)
        
        # Adds models information
        if line[0] == '<MODEL_NAME>':
            self.model_name = line[1]
        elif line[0] == '<MODEL_WORD_COUNT>':
            self.all_words_count = int(line[1])
            
        # Add unigram, n_gram[0] = word and line [1] = count
        elif line_length == 2:
            self.unigram_count[n_gram[0]] = self.unigram_count.get(n_gram[0], 0) + int(line[1])
        # Add bigram, n_gram[0] = bigram, and line [2] = count
        elif line_length == 3:
            self.bigram_count[n_gram[0]] = self.bigram_count.get(n_gram[0], 0) + int(line[2])
        # Add trigram, n_gram[0] trigram, and line [3] = count
        elif line_length == 4:
            self.trigram_count[n_gram[0]] = self.trigram_count.get(n_gram[0], 0) + int(line[3])
            
    def fix_n_gram_count(self):
        """
        Adds the "self.START_SYMBOL self.START_SYMBOL" count to the bigram count based on how many self.END_SYMBOL are in the unigram count.
        Adds "self.START_SYMBOL" count to the unigram count based on how many self.END_SYMBOL are in the unigram count.
        """
        end_symbol_count = self.unigram_count[self.END_SYMBOL]
        
        bigram_key = f'{self.START_SYMBOL} {self.START_SYMBOL}'
        self.bigram_count[bigram_key] = end_symbol_count
        
        unigram_key = f'{self.START_SYMBOL}'
        self.unigram_count[unigram_key] = end_symbol_count
