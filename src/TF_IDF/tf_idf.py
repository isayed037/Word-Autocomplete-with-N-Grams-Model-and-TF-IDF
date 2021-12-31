from math import log

class TF_IDF:
    def __init__(self) -> None:
        pass
    
    def calculate_TF_IDF(self, all_document_frequency, total_number_of_documents, bag_of_words_and_count):
        '''
        Takes documents frequency matrix, total number of documents, and how many documents contain each word.
        
        Calculates the TF_IDF and updates the documents frequency matrix in place.
        '''
        # Loop through each word 
        for word, counts_per_doc in all_document_frequency.items():
            # Loop through all the documents
            for doc_number in range(total_number_of_documents):
                # TF calculation
                if counts_per_doc[doc_number] == 0:
                    tf_weight = 0
                else:
                    if counts_per_doc[doc_number] <= 0:
                        tf_weight = 1
                    else:
                        tf_weight = 1 + log(counts_per_doc[doc_number], 2)
                
                # IDF calculation
                idf_calculation = total_number_of_documents / bag_of_words_and_count[word]
                idf_weight = log(idf_calculation, 2)
                
                # Weight
                tf_idf_weight = tf_weight * idf_weight
                
                counts_per_doc[doc_number] = tf_idf_weight
                
    def calculate_new_TF_IDF(self, all_document_frequency, total_number_of_documents, bag_of_words_and_count):
        '''
        Takes documents frequency matrix, total number of documents, and how many documents contain each word.
        
        Calculates the TF_IDF and returns a new  documents frequency matrix with the TF_IDF values.
        '''
        tf_idf_matrix = {}
        
        # Loop through each word 
        for word, counts_per_doc in all_document_frequency.items():
            # Loop through all the documents
            tf_idf_per_doc = []
            
            for doc_number in range(total_number_of_documents):
                # TF calculation
                if counts_per_doc[doc_number] == 0:
                    tf_weight = 0
                else:
                    if counts_per_doc[doc_number] <= 0:
                        tf_weight = 1
                    else:
                        tf_weight = 1 + log(counts_per_doc[doc_number], 2)
                
                # IDF calculation
                idf_calculation = total_number_of_documents / bag_of_words_and_count[word]
                idf_weight = log(idf_calculation, 2)
                
                # Weight
                tf_idf_weight = tf_weight * idf_weight
                
                tf_idf_per_doc.append(tf_idf_weight)
            
            # Add the word and the TF_IDF values to the TF_IDF matrix model.
            tf_idf_matrix[word] = tf_idf_per_doc
        
        return tf_idf_matrix
                
                