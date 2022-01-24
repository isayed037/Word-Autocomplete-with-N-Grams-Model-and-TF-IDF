"""
Return the paths to the files in the model or corpus folder.

#! TODO: 
#!  - Make "corpus" and "model" folder names Path_To_Files class variables that the user can change. 
#!  - Instead of showing missing_folder_or_file_msg, create the folder/file for the user. 
"""

from os.path import isdir, isfile, join
from os import listdir, remove

class Path_To_Files:
    def __init__(self) -> None:
        self.all_trigram_models = None
        
        # Stores all the files path for the current document found in the "corpus" folder
        self.all_files_path_in_document = None
        
        # Keys are "document" folder which represent 1 document. Values is a list of the paths to all the files in the document.
        self.all_documents_and_paths_from_corpus = {}
        
        # Keys are the type of model it is. Values is the path to that output file.
        self.all_models_with_output_paths = {}
        
        # Keys are the type of model it is. Values is the path to file.
        self.all_models_with_paths = {}
        
    def missing_folder_or_file_msg(self, folder_name, folder_path, type_of_dir):            
        error_msg = f'\n\tMissing "{folder_name}" {type_of_dir}. \n\tMake sure {type_of_dir} is in the path "\{folder_path}" from "auto_complete_and_TF_IDF.py" file'
        
        print(error_msg)
    
    def get_all_documents_file_from_corpus(self):
        """
        Goes through the "corpus" folder and gets the file path to all the documents and it's files.
        Returns a Dict() where Keys are the document name(The folder name of the document) and the values are a list of all the files path in that document.
        """
        self.all_files_path_in_document = []
        
        corpus_directory_path = "corpus"
        if isdir(corpus_directory_path):
            self.get_documents_file_from_corpus(corpus_directory_path)
        else:
            self.missing_folder_or_file_msg("corpus", corpus_directory_path, "folder")
        
        return self.all_documents_and_paths_from_corpus
    
    def get_documents_file_from_corpus(self, corpus_directory_path):
        """
        Goes through each of the document in the corpus. Updates get_documents_file_from_corpus to store the document name and a list with all the paths for that document
        """
        all_documents_list = listdir(corpus_directory_path)
        
        if not all_documents_list: 
            print('\n\tNo documents found in the "corpus" folder.')
            return
        
        # Loops through all document's in the "corpus" folder
        for document in all_documents_list:
            document_files_path = join(corpus_directory_path, document)
            
            all_files_from_doc = listdir(document_files_path)
            
            # Iterates over all the files for the current document
            for file in all_files_from_doc:
                path_to_file = join(document_files_path, file)
                
                self.all_files_path_in_document.append(path_to_file)
            
            # Adds the document name and all files path in that document. Also reset all_files_path_in_document for the next document.
            self.all_documents_and_paths_from_corpus[document] = self.all_files_path_in_document
        
            self.all_files_path_in_document = []
            
    def get_output_file_paths_to_new_models(self, all_trigram_models, all_trigram_models_name='all_trigram_models', document_frequency_model_name='document_frequency_model.txt', bag_and_count_model_name="bag_model.txt"):
        """
        Takes a dict() with document names as the keys. Also takes optional arguments for trigram, document_frequency, and bag_and_count models folder and file names.
        
        Returns a dict() where the keys are the optional arguments and values are the outpath path to it's respective model.
        For all_trigram_models_name the values is a list with all the files output path. 
        """
        
        model_directory_path = 'model'
        if isdir(model_directory_path):
            # Updates the output file paths for all the trigram models
            self.get_new_trigram_models_output_paths(model_directory_path, all_trigram_models, all_trigram_models_name)
            
            # Updates the output files path for the TF-IDF models.
            self.get_new_TF__IDF_models_output_paths(model_directory_path, document_frequency_model_name, bag_and_count_model_name)
        else:
            self.missing_folder_or_file_msg('model', model_directory_path, "folder")

        return self.all_models_with_output_paths
    
    def get_new_trigram_models_output_paths(self, model_directory_path, all_trigram_models, all_trigram_models_name):
        """
        Takes the "model" folder's name. All the trigram_models. Also takes the trigram_models folder name.
        
        Updates self.all_models_with_output_paths with all_trigram_models_name as the keys and the values is a dict() with document name as keys and the values is the files output path.
        """
        all_trigram_models_path = join(model_directory_path, all_trigram_models_name)
            
        if isdir(all_trigram_models_path):
            all_document_txt_path = self.add_trigram_model_output_path(all_trigram_models_path, all_trigram_models)
            
            self.all_models_with_output_paths[all_trigram_models_name] = all_document_txt_path
        else:
            self.missing_folder_or_file_msg(all_trigram_models_name, all_trigram_models_path, 'folder')
    
    def add_trigram_model_output_path(self, trigram_model_path, all_trigram_models):
        """
        Takes the trigram_model_path so far and takes all_trigram_models to get the names of all trigram models.
        Loop through all trigram models and create a path to save the models as txt file.
        """
        # Removes all pre-existing models
        for file in listdir(trigram_model_path):
            remove_model_file_path = join(trigram_model_path, file)
            remove(remove_model_file_path)
        
        all_document_txt_path = {}
        
        # Goes through all the trigram models and gets the models name. Creates the outfile path.
        for document_name in all_trigram_models:
            trigram_model_file_path = join(trigram_model_path, f'{document_name}.txt')
            
            if isfile(trigram_model_file_path): remove(trigram_model_file_path)
            
            all_document_txt_path[document_name] = (trigram_model_file_path)
        
        return all_document_txt_path
            
    def get_new_TF__IDF_models_output_paths(self, model_directory_path, document_frequency_model_name, bag_and_count_model_name):
        """
        Takes the "model" folder's name. Also takes the document frequency and bag_and_count models folder name.
        
        Updates self.all_models_with_output_paths with document_frequency_model_name and bag_and_count_model_name as the keys and the values is the file outpath path for the respective models.
        """
        all_tf_idf_model_output_path = join(model_directory_path, 'tf_idf')
        
        if isdir(all_tf_idf_model_output_path):
            document_frequency_model, bag_and_count_model = self.add_new_tf_idf_model_output_path(all_tf_idf_model_output_path, document_frequency_model_name, bag_and_count_model_name)
            
            self.all_models_with_output_paths[document_frequency_model_name] = document_frequency_model
            self.all_models_with_output_paths[bag_and_count_model_name] = bag_and_count_model
        else:
            self.missing_folder_or_file_msg('tf_idf', all_tf_idf_model_output_path, 'folder')
            
    def add_new_tf_idf_model_output_path(self, all_tf_idf_model_output_path, document_frequency_model_name, bag_and_count_model_name):
        """
        Takes the all_tf_idf_model_output_path so far. Takes document_frequency_model_name and bag_and_count_model_name files's names.
        
        Creates the output paths to the 2 models. Removes any files that are there with the same names
        """
        document_frequency_model_path = join(all_tf_idf_model_output_path, document_frequency_model_name)
        
        if isfile(document_frequency_model_path):
            remove(document_frequency_model_path)
        
        bag_and_count_model = join(all_tf_idf_model_output_path, bag_and_count_model_name)
        
        if isfile(bag_and_count_model):
            remove(bag_and_count_model)
            
        return document_frequency_model_path, bag_and_count_model
    
    def get_all_models_files_from_model(self, all_trigram_models_name='all_trigram_models', document_frequency_model_name='document_frequency_model.txt', bag_and_count_model_name="bag_model.txt"):
        """
        Takes optional arguments for trigram, document_frequency, and bag_and_count models folder and file names.
        
        Goes through the "model" folder and gets the file path to all the models.
        Returns a Dict() where keys are the model name and the values are the the paths to the files.
        """
        models_directory_path = "model"     
        if isdir(models_directory_path):
            # Gets trigram models files from "model" folder
            self.add_trigram_model_from_model(models_directory_path, all_trigram_models_name)
            
            # Gets TF-IDF models files from the "model" folder
            self.add_TF_IDF_model_from_model(models_directory_path, document_frequency_model_name, bag_and_count_model_name)
        else:
            self.missing_folder_or_file_msg(models_directory_path, models_directory_path, 'folder')
        
        return self.all_models_with_paths
            
    def add_trigram_model_from_model(self, models_directory_path, all_trigram_models_name):
        """
        Takes the path so far and takes the name for the trigram model folder.
        Gets the trigram models files path from the "models" folder.
        """
        trigram_model_paths = join(models_directory_path, all_trigram_models_name)
        
        if isdir(trigram_model_paths):
            all_trigram_model_files = listdir(trigram_model_paths)
            
            all_models_file_path = self.add_trigram_model_paths(trigram_model_paths, all_trigram_model_files)
            
            # Check if there was any models
            if all_models_file_path:
                self.all_models_with_paths[all_trigram_models_name] = all_models_file_path
        else:
            self.missing_folder_or_file_msg(all_trigram_models_name, trigram_model_paths, 'folder')
    
    def add_trigram_model_paths(self, path, files):
        """
        Takes a list of files and the path up to those files. Creates a list that represents the path to all the trigram models.
        """        
        # Appends the all the new path to the models
        all_models_file_path = []
        for file in files:
            model_file_path = join(path, file)
            
            all_models_file_path.append(model_file_path)
        
        return all_models_file_path
            
    def add_TF_IDF_model_from_model(self, models_directory_path, document_frequency_model_name, bag_and_count_model_name):
        """
        Takes the path so far and takes the name for the document frequency and bag_and_count models.
        Gets the document frequency and bag_and_count models files path from the "models" folder.
        """
        tf_idf_model_paths = join(models_directory_path, "tf_idf")
        
        if isdir(tf_idf_model_paths):
            self.add_TF_IDF_models_paths( tf_idf_model_paths, document_frequency_model_name, bag_and_count_model_name)
        else:
            self.missing_folder_or_file_msg("tf_idf", tf_idf_model_paths, 'folder')

    def add_TF_IDF_models_paths(self, tf_idf_model_paths, document_frequency_model_name, bag_and_count_model_name):
        """
        Takes a list of files and the path up to those files. Creates a list that represents the path to all the trigram models.
        """   
        all_tf_idf_model_files = listdir(tf_idf_model_paths)
        
        # Check if there is any models
        if not all_tf_idf_model_files: return self.all_models_with_paths
        
        # Find the right model and create it's path
        for file_name in all_tf_idf_model_files:
            if file_name == document_frequency_model_name:
                self.all_models_with_paths[document_frequency_model_name] = join(tf_idf_model_paths, document_frequency_model_name)
            else:
                self.all_models_with_paths[bag_and_count_model_name] = join(tf_idf_model_paths, bag_and_count_model_name)
                      