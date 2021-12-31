from math import sqrt

class Cosine_Similarity:
    def __init__(self) -> None:
        pass
    
    def calculate_similarity(self, all_document_names, all_document_frequency):
        """
        Takes a document frequency matrix. Compares all the documents to the last document. Returns the document that is most similar to the last document based on all_document_names. 
        """
        if not all_document_frequency: return
        
        highest_similarity = float('-inf')
        model_with_highest = None
        
        for document in range(len(all_document_names) - 1):
            s = self.similarity(all_document_frequency, document, len(all_document_names) - 1)
            
            if s >= highest_similarity:
                highest_similarity = s
                model_with_highest = document
                
        return all_document_names[model_with_highest]
    
    def similarity(self, all_document_frequency, doc_1, doc_2):
        """
        Takes document frequency matrix. Also takes the index of 2 different documents in the document frequency matrix.
        
        Calculates the cosine similarity between the two documents and returns the result.
        """
        numerator = 0
        d1_squared = 0
        d2_squared = 0

        for _, doc_count in all_document_frequency.items():
            if len(doc_count) > doc_1:
                doc1_count = doc_count[doc_1]
            else:
                doc1_count = 0
            
            if len(doc_count) > doc_2:
                doc2_count = doc_count[doc_2]
            else:
                doc2_count = 0
            
            numerator += (doc1_count * doc2_count)
            d1_squared += doc1_count ** 2
            d2_squared += doc2_count ** 2
                    
        denominator = (sqrt(d1_squared)) * (sqrt(d2_squared))

        if numerator == 0 or denominator == 0:
            return 0
        else:
            return numerator/denominator