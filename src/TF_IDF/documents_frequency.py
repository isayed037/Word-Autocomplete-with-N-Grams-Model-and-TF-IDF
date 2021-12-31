'''
#! TODO:
#! - Add stops words in the initialized_stopwords() method.
'''

class Documents_Frequency:
    def __init__(self, end_symbol="<STOP>") -> None:
        """
        Tracks of the frequency of words in each document.
        """
        # Keys are all unique words. Values is a list with the index represents one document and elements representing the number of times the words appear in that document. 
        self.all_document_frequency = dict()
        
        # Keys are all unique words and values are how many documents contain that word
        self.bag_of_words_and_document_count = dict()
        
        # Stops words are words that are not counted
        self.stop_words = set()
        self.initialized_stopwords()
        
        # Document frequency info
        self.total_number_of_documents = 0
        self.all_documents_name = list()
        self.END_SYMBOL = end_symbol
    
    def add_one_document(self, document_name, document):
        '''
        Takes the unigram count for the document and adds it to the document frequency matrix.
        '''
        if not document: return
        
        added_to_bag = set()
        
        # Iterate over all words in the document
        for word in document:
            # Add the word to the document
            self.add_word_to_model(word, added_to_bag, document)
         
        added_to_bag.clear()
        
        # Update model information
        self.total_number_of_documents += 1
        self.all_documents_name.append(document_name)
        
        return
    
    def remove_last_document(self):
        '''
        Removes the last document of the document frequency. Removes document name and decrease total number of documents by 1. 
        
        '''
        if not self.all_documents_name: return

        self.all_documents_name.pop()
        self.total_number_of_documents -= 1
        
        # Loop through all words and remove the last document's count.
        for word, count_per_doc in self.all_document_frequency.items():
            user_word_count = count_per_doc.pop()
            if user_word_count == 0: continue
            
            # If there was a word count, then we update bag_of_words_and_document_count by decreasing it by one.
            self.bag_of_words_and_document_count[word] = self.bag_of_words_and_document_count.get(word, 1) - 1
        
        # If the word count in all documents is 0, we remove it from the document frequency and bag_and_count models.
        words_to_remove = []
        for word, count in self.bag_of_words_and_document_count.items():  
            if count == 0:
                words_to_remove.append(word)
                
        for word in words_to_remove:
            self.all_document_frequency.pop(word, None)
            self.bag_of_words_and_document_count.pop(word, None)
            
    def add_word_to_model(self, word, added_to_bag, document):
        """
        Adds one word to the model if it's a valid word.
        """
        # Skip words that won't be useful for TF-IDF calculation
        if word == self.END_SYMBOL or word in self.stop_words or len(word) <= 1:
            return
        
        processed_word = word.lower()
        
        # Update bag_of_words_and_document_count.
        if processed_word not in added_to_bag:
            self.bag_of_words_and_document_count[processed_word] = self.bag_of_words_and_document_count.get(processed_word, 0) + 1
            
            added_to_bag.add(processed_word)
        
        # Update document frequency
        if processed_word in self.all_document_frequency:
            doc_word_count = self.all_document_frequency[processed_word]

            while len(doc_word_count) < self.total_number_of_documents + 1:
                doc_word_count.append(0)

            doc_word_count[self.total_number_of_documents] += document[word]
        else:
            doc_word_count = []
            
            for _ in range(self.total_number_of_documents + 1):
                doc_word_count.append(0)
            
            doc_word_count[self.total_number_of_documents] += document[word]
        
        self.all_document_frequency[processed_word] = doc_word_count
    
    def finalize_document_frequency(self):
        """
        Finalize the model by adding 0 to all_document_frequency values until len(values) < total_number_of_documents.
        """
        for word in self.all_document_frequency:
            word_count_in_doc = self.all_document_frequency[word]

            while len(word_count_in_doc) < self.total_number_of_documents:
                    word_count_in_doc.append(0)
    
    def print_document_frequency(self):
        """
        Prints the current model's information.
        """
        self.finalize_document_frequency()
        print("\n\tDocument Frequency: \t", self.all_documents_name)
        for word in self.all_document_frequency:
            print("\t\t", word, "\t\t", self.all_document_frequency[word])
    
    
    def initialized_stopwords(self):
        self.stop_words.add("is")
    
    def update_stopwords(self, word):
        if word in self.stop_words:
            return
        
        self.stop_words.add(word.lower())
        
        return self.stop_words
    
    def save_models_to_file(self, document_frequency_model_output_path, bag_and_count_model_output_path):
        """
        Saves the document frequency and bag_and_count model to their respective file paths. Also adds the total number of documents and all_documents_name to the end of the bag_and_count file.
        """
        # Create a file and save the document frequency to the document_frequency_model_output_path
        with open(document_frequency_model_output_path, 'w') as output_file:
            for word, count_per_doc in self.all_document_frequency.items():
                cpd_str = " ".join(str(c) for c in count_per_doc)
                line = word + '\t' + cpd_str + '\n'
                output_file.write(line)
        
        print(f'\t\t- Added "all_document_frequency" model to the file "{document_frequency_model_output_path}"')
        
        
        # Save bag of words and count model to the file
        with open(bag_and_count_model_output_path, 'w') as output_file:
            for word, total_count in self.bag_of_words_and_document_count.items():
                line = word + '\t' + str(total_count) + '\n'
                output_file.write(line)
            
            # Add number of documents to file 
            line = "document_number" + '\t' + str(self.total_number_of_documents) + '\n'
            output_file.write(line)
            
            # Add the names of all documents to file
            all_doc_name_string = " ".join(s for s in self.all_documents_name)
            line = "all_documents_name" + '\t' + all_doc_name_string
            output_file.write(line)
            
        print(f'\t\t- Added "bag_of_words_and_count" model to the file "{bag_and_count_model_output_path}"') 

    def get_document_frequency_from_file(self, file_path):
        """
        Gets the document frequency from the file_path. Adds the document frequency model from the file.
        """
        with open(file_path) as file:
            for line in file:
                line = line.split()
                
                all_count_per_doc = []
                
                for count_of_doc in range(1, len(line)):
                    all_count_per_doc.append(float(line[count_of_doc]))
                
                self.all_document_frequency[line[0]] = all_count_per_doc
    
    def get_bag_and_count_model_from_file(self, file_path):
        """
        Gets the bag_of_words_and_document_count model from the file_path. Adds the bag_of_words_and_document_count model, total_number_of_documents, and all_documents_name from the file.
        """
        with open(file_path) as file:
            for line in file:
                line = line.split()

                if line[0] == "document_number":
                    self.total_number_of_documents = int(line[1])
                elif line[0] == "all_documents_name":
                    for name_index in range(1, len(line)):
                        self.all_documents_name.append(line[name_index])
                else:
                    self.bag_of_words_and_document_count[line[0]] = int(line[1])
        