'''
Takes a txt file and create a 2d list of all the sentences. 
self.sentence has a list for every sentence. Every sentence is a list of words. 
self.sentence example = [
                            ["This", "is", "one", "sentence"],
                            ["This", "is" "another", "sentence"]
                        ]
'''

class Get_Sentences:
    def __init__(self, END_SYMBOL) -> None:
        self.END_SYMBOL = END_SYMBOL
        
        # 2d list with all the sentences and words for the current document.
        self.sentences = list()
        
        self.current_file_path = None
        
        # List of completed files for the current document. If there are multiple same files in one document skips the duplicate files
        self.completed_files = dict()
        
        # Special words that we change manually. 
        self.special_words = dict()
        self.add_special_words()

    def get_all_sentences(self, file_path):
        '''
        Gets all sentences found in the file from "file_path" path. Returns an 2d array of sentence and every word in the sentence. Returns an empty list if no file is found.
        '''
        # Checks if it's a valid file
        if not self.check_file_path: return []
        
        # Check if we already included this file
        if file_path in self.completed_files: 
            print(f'\n\t"{file_path}" file already included. Skiping.\n')
            return self.completed_files[file_path]
        
        self.sentences = []
        self.current_file_path = file_path
        
        # Get all sentences and words and return the sentences
        self.sentences_from_file()
        
        self.completed_files[file_path] = self.sentences
        return self.sentences
    
    def check_file_path(self):
        """
        Checks if it's valid file. If it is then return True, otherwise returns False
        """
        try:
            with open(self.current_file_path):
                print(f"Opened file: {self.current_file_path}")
        except FileNotFoundError:
            print(f"File {self.current_file_path} not found!")
            return False
        except PermissionError:
            print(f"Insufficient permission to read {self.current_file_path}!")
            return False
        
        return True
    
    def sentences_from_file(self):        
        sentence = []
        with open(self.current_file_path, errors="ignore") as file:
            for line in file:
                for word in line.split():
                    self.add_and_check_word(sentence, word)
                    
        # If the last sentence of file doesn't end with '.' or ';', we still add the last sentence.
        if sentence: self.is_sentence_end(sentence)
    
    def sentences_from_user(self, user_sentence):
        """
        Works with the sentence from the user during auto-complete
        """
        sentence = []
        
        for word in user_sentence.split():
            self.add_and_check_word(sentence, word)
        
        if sentence: self.is_sentence_end(sentence)
        
        return self.sentences
    
    def add_and_check_word(self, sentence, word):
        '''
        Adds the finalized word to the sentence. Also checks if it's the end of the sentence and appends the sentence to self.sentences
        '''
        if not word or word == "<p>" or not word[0].isalpha():
            return
        
        word, sentence_end = self.get_finalized_word(word)
                        
        if word:
            sentence.append(word)
        
        if sentence_end:
            self.is_sentence_end(sentence)
    
    def get_finalized_word(self, word):
        """
        Only takes alphabet letters.
        Checks the last char in the word to see if it's '.' or ';'.
        """  
        finalized_word = ''.join(
                            word[index] for index in range(len(word)) 
                            if word[index].isalpha()
                        )
        
        finalized_word = self.check_finalized_word(finalized_word)
        
        char = word[-1]
        if char == "." or char == ";" or char == "?" or char == "!":
            sentence_end = True
        else:
            sentence_end = False
        
        return finalized_word, sentence_end

    def is_sentence_end(self, sentence):        
        if sentence:
            sentence.append(self.END_SYMBOL)
            self.sentences.append(sentence.copy())
        
        sentence.clear()
    
    def add_special_words(self, special_word = None, word = None):
        # Special words are "Im" which we want to change to "I'm". Or it could "m" which we change to "am". When we only take alphabet some words get messed up so we need to update them.
        if not self.special_words:
            self.special_words["m"] = "am"
            self.special_words["M"] = "Am"
            self.special_words["re"] = "are"
            self.special_words["Re"] = "Are"
            self.special_words["Im"] = "I'm"
            self.special_words["youre"] = "You're"
            self.special_words["Youre"] = "You're"
            self.special_words["dont"] = "don't"
            self.special_words["Don't"] = "Don't"
            self.special_words["s"] = "is"
            
        
        if special_word and word:
            self.special_words[special_word] = word
    
    def check_finalized_word(self, word):
        if word in self.special_words:
            return self.special_words[word]
        
        return word
    
