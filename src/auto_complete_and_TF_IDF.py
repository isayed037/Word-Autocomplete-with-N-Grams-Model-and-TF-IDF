
from path_to_files import Path_To_Files

from N_Gram_Model import Get_Sentences, Trigram_Model, Calculate_Linear_Interpolation

from TF_IDF import Documents_Frequency, TF_IDF, Cosine_Similarity

class N_Gram_And_TF_IDF_Models:
    def __init__(self, START_SYMBOL="<*>", END_SYMBOL="<STOP>", ALL_MODEL_NAME="ALL") -> None:
        # Class variables
        self.START_SYMBOL = START_SYMBOL
        self.END_SYMBOL = END_SYMBOL
        self.ALL_MODEL_NAME = ALL_MODEL_NAME
        
        # The n-gram and TF-IDF models
        self.all_trigram_models = None
        self.df = None
    
        self.path = Path_To_Files()
    
    def create_models_from_corpus(self):
        """
        Creates new n-gram and TF-IDF model based on the documents in the "corpus" folder.
        
        Returns a dict() where the keys are the document name and values are the Trigram_Gram_Model object instances. Also returns an Documents_Frequency object instance. 
        """
        # Get all paths to all document in the "corpus" folder
        all_document_paths_from_corpus = self.path.get_all_documents_file_from_corpus()
        
        # Creates all n-gram models from the documents found in the "corpus" folder
        self.all_trigram_models = self.trigram_models_from_corpus(all_document_paths_from_corpus)
        
        # Creates all document frequency models from documents in all_trigram_models except for ALL_MODEL_NAME
        self.df = self.df_model_from_corpus()
        
        return self.all_trigram_models, self.df
        
    def trigram_models_from_corpus(self, all_document_paths_from_corpus):
        """
        Takes dictionary where keys are the document name and values are all the paths to file that belong to that dictionary.
        Returns a dictionary where keys are document name and values are Trigram_Model objects for that document.
        Trigram_Model has unigram, bigram, trigrams, and all words counts.
        """
        # Get all sentences found in the files in "all_document_paths_from_corpus"
        get_sentences_per_document = Get_Sentences(self.END_SYMBOL)
        
        # Initialize Trigram_Model objects for the entire corpus.
        entire_corpus_model = Trigram_Model(model_name=self.ALL_MODEL_NAME, start_symbol=self.START_SYMBOL, end_symbol=self.END_SYMBOL)
        
        all_trigram_models = dict()

        # Loop through all documents in the "corpus" folder
        for document_name, all_paths in all_document_paths_from_corpus.items():
            documents_trigram_model = Trigram_Model(model_name=document_name, start_symbol=self.START_SYMBOL, end_symbol=self.END_SYMBOL)
            
            # Loop through all files in the current document
            for file_path in all_paths:
                # Get all sentence from this file
                all_sentences = get_sentences_per_document.get_all_sentences(file_path)
                
                # Adds sentence from this file to the current trigram model.
                documents_trigram_model.add_sentences_to_model(all_sentences)
                
            all_trigram_models[document_name] = documents_trigram_model
            
            # Adds current document's model to entire_corpus_model trigram model
            entire_corpus_model.add_all_counts(documents_trigram_model.unigram_count, documents_trigram_model.bigram_count, documents_trigram_model.trigram_count, documents_trigram_model.all_words_count)
            
            # Added one document from "corpus"
            if len(all_paths) <= 3:
                print(f'\t\t- Added "{document_name}" document model with these files {all_paths}')
            else:
                print(f'\t\t- Added "{document_name}" document model with all files in "{document_name}" folder.')
    
        all_trigram_models[self.ALL_MODEL_NAME] = entire_corpus_model
        print('\t\t- Added "ALL" model which includes all the documents\n')

        return all_trigram_models
    
    def df_model_from_corpus(self):
        """
        Uses all_trigram_models to create the document frequency models.
        Returns a Documents_Frequency object if successful otherwise returns None
        """
        if not self.all_trigram_models: return
        
        df = Documents_Frequency(end_symbol=self.END_SYMBOL)
        
        # Iterate over all trigram models and add it to the document frequency model.
        for model_name, model in self.all_trigram_models.items():
            if model_name == self.ALL_MODEL_NAME:
                continue
            
            df.add_one_document(model_name, model.unigram_count)
        
        # Finalize the model
        df.finalize_document_frequency()
        
        return df
    
    
    
    def get_models_from_models_folder(self):
        """
        Creates new n-gram and TF-IDF model based on the documents in the "model" folder.
        
        Returns a dict() where the keys are the document name and values are the Trigram_Gram_Model object instances. Also returns an Documents_Frequency object instance. 
        """
        
        # Get all paths to all models in the "model" folder
        all_models_path_from_model = self.path.get_all_models_files_from_model()
        
        if not all_models_path_from_model: 
            return self.all_trigram_models, self.df
        
        # Add all n-gram models from the "model" folder.
        self.all_trigram_models = {}
        for trigram_model_file_path in all_models_path_from_model['all_trigram_models']:
            document_trigram_model = Trigram_Model(model_name="", start_symbol=self.START_SYMBOL, end_symbol=self.END_SYMBOL)
            
            current_model_name = document_trigram_model.get_model_from_file(trigram_model_file_path)
            
            self.all_trigram_models[current_model_name] = document_trigram_model
            
            print(f'\t\t- Added "{current_model_name}" document\'s model from the file "{trigram_model_file_path}".')
        
        # Add all TF-IDF models from the "model" folder.
        self.df = Documents_Frequency(self.END_SYMBOL)
        
        document_frequency_model_file_path = all_models_path_from_model['document_frequency_model.txt']
        self.df.get_document_frequency_from_file(document_frequency_model_file_path)
        print(f'\t\t- Added "document_frequency_model" model from the file "{document_frequency_model_file_path}".')  

        bag_and_count_model_file_path = all_models_path_from_model["bag_model.txt"]
        self.df.get_bag_and_count_model_from_file(bag_and_count_model_file_path)
        print(f'\t\t- Added "bag_model" model from the file "{bag_and_count_model_file_path}".')
    
        return self.all_trigram_models, self.df
    
    
    def save_models_to_files(self):
        """
        Creates new files with the current n-gram and TF-IDF models.
        """
        # Get the output file paths.
        all_models_output_path = self.path.get_output_file_paths_to_new_models(all_trigram_models=self.all_trigram_models)
        
        # Loop through all the trigram models and save the models to the file path.
        for trigram_model in self.all_trigram_models.values():
            # Saves the current trigram model to a file.
            trigram_model.save_model_to_file(all_models_output_path['all_trigram_models'])
        
        # Add the document frequency and bag of words and number of appears in document to the files.
        self.df.save_models_to_file(all_models_output_path['document_frequency_model.txt'], all_models_output_path["bag_model.txt"])
        
    
    def fix_n_grams_model(self):
        """
        Add 2 start symbol to the bigram_count based on how many end symbols are in the unigram count. Adds 1 start symbol to the unigram_count based on how many end symbols are in the unigram count.
        """
        for trigram_model in self.all_trigram_models.values():
            trigram_model.fix_n_gram_count()
        
        return self.all_trigram_models
        
        
        
class Auto_Complete_And_TF_IDF:
    def __init__(self, START_SYMBOL="<*>", END_SYMBOL="<STOP>", ALL_MODEL_NAME="ALL") -> None:
        # Class variables
        self.START_SYMBOL = START_SYMBOL
        self.END_SYMBOL = END_SYMBOL
        self.ALL_MODEL_NAME = ALL_MODEL_NAME  
        
        self.current_model_name = None
        self.current_linear_interpolation = None 
        
        self.all_user_sentences = None
    
    def update_current_name_and_linear_interpolation(self, model_name, trigram_model):
        """
        Takes a model name and trigram model object.
        Updates self.current_model_name and self.current_linear_interpolation with the new model.
        """
        self.current_model_name = model_name
        
        trigram_model_all_info = trigram_model.get_model_information()
            
        self.current_linear_interpolation = Calculate_Linear_Interpolation(trigram_model_all_info[1], trigram_model_all_info[2], trigram_model_all_info[3], trigram_model_all_info[4], self.END_SYMBOL, self.START_SYMBOL)
        
    
    def show_first_word_in_sentence(self, model_name, trigram_model, show):
        """
        Takes a model name and trigram model object, and predicts the first word of a sentence.
        Prints the word and the probability
        """        
        if model_name != self.current_model_name:
            self.update_current_name_and_linear_interpolation(model_name, trigram_model)
        
        
        self.current_linear_interpolation.show_next_word(model_name, show, self.START_SYMBOL, self.START_SYMBOL)
        
    def get_user_sentences(self, user_sentence):
        """
        Takes a string that represents the user sentence so far. 
        Returns a 2d list of all the sentence and it's words.
        """
        user_input_sentence = Get_Sentences(END_SYMBOL=self.END_SYMBOL)
        
        self.all_user_sentences = user_input_sentence.sentences_from_user(user_sentence)
        
        return self.all_user_sentences
        
    def show_next_word(self, model_name, trigram_model, show):
        """
        Takes the model name and the trigram model object. Also takes show which is how many top probabilites should be shown.
        
        Return the next word based on the the previous two words in the last sentence in self.all_user_sentences
        """
        if model_name != self.current_model_name:
            self.update_current_name_and_linear_interpolation(model_name, trigram_model)
        
        if len(self.all_user_sentences[-1]) == 2:
            self.current_linear_interpolation.show_next_word(model_name, show, self.START_SYMBOL, self.all_user_sentences[-1][-2])
        else:
            self.current_linear_interpolation.show_next_word(model_name, show, self.all_user_sentences[-1][-3], self.all_user_sentences[-1][-2])
        
    def find_most_similar_model(self, all_user_sentences, df, in_place="True"):
        """
        Takes the user sentence and takes a Documents_Frequency object. 
        
        Adds the user sentence to the Documents_Frequency model. Converts the Documents_Frequency to TF-IDF. Uses Cosine_Similarity to find the document that is most similar to the last document(user's sentence document).
        Returns the model name of the most similar document.
        """
        # Create the trigram model for the user sentence and then add the sentences to the model.
        user_sentences_model = Trigram_Model("USER", self.START_SYMBOL, self.END_SYMBOL)
        user_sentences_model.add_sentences_to_model(all_user_sentences)

        # Add the user's trigram model to our document frequency.
        df.add_one_document(user_sentences_model.model_name, user_sentences_model.unigram_count)
        df.finalize_document_frequency()
        
        # Calculate the TF_IDF and find the most similar document
        tf_idf = TF_IDF()
        similarity = Cosine_Similarity()
        if in_place:
            tf_idf.calculate_TF_IDF(df.all_document_frequency, df.total_number_of_documents, df.bag_of_words_and_document_count)
            
            model_name = similarity.calculate_similarity(df.all_documents_name, df.all_document_frequency)
        else:
            tf_idf_matrix = tf_idf.calculate_new_TF_IDF(df.all_document_frequency, df.total_number_of_documents, df.bag_of_words_and_document_count)
            
            model_name = similarity.calculate_similarity(df.all_documents_name, tf_idf_matrix)

        return model_name
    
    
        
        