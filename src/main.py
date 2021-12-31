"""
#! TODO:
#! - Work on path_to_files.py
#! - Video Docs
#! - Upload to Github
#! - Test which files can be uploaded on v11 version

Predicts the next word in a sentence by calculating the Linear Interpolation using the Trigram-model. At the end of a sentence calculates the Cosine Similarity using the TF-IDF model to find the document that is most similar to the sentence so far.

When prompted either load either the existing models or create new models from the corpus. When prompted enter a word/words and the application will predict the next word based on the most similar document.
"""

from auto_complete_and_TF_IDF import N_Gram_And_TF_IDF_Models, Auto_Complete_And_TF_IDF

def predict_next_work(all_trigram_models, df, START_SYMBOL = "<*>", END_SYMBOL = "<STOP>", ALL_MODEL_NAME = "ALL"):
    """
    Takes all trigram models and DF models. Also takes the name of the ALL_MODEL_NAME
    Prompts the user for words and predict the next word. When a sentence ends, uses df model to calculate TF-IDF and changes models to the most similar document. For the following sentence uses the new trigram model.
    """
    auto_complete = Auto_Complete_And_TF_IDF(START_SYMBOL, END_SYMBOL, ALL_MODEL_NAME)
    
    model_name = ALL_MODEL_NAME
    sentence_string = ''
    sentence_count = 1
    
    show = 3
    
    print("\n-----------------------------------------------------------------------------------------------------------------------\n")
    
    while True:
        print('\tEnter the next "word"/"words".')
        print('\tOR Enter just ""/nothing to see the first word. OR Enter just "r" to restart. OR Enter just "c" or "n" to exit.')
        user_input = input("\t\t - Enter the next word: ")
        
        if user_input == 'c' or user_input == 'C': break
        if user_input == 'n' or user_input == 'N': break
        
        if user_input == 'r' or user_input == 'R': predict_next_work(all_trigram_models, df, START_SYMBOL, END_SYMBOL, ALL_MODEL_NAME)
        
        # If user_input is empty then show the first word of the sentence.
        if not user_input:
            auto_complete.show_first_word_in_sentence(model_name=model_name, trigram_model=all_trigram_models[model_name], show=show)
            continue
            
        # If user_input isn't a word we skip the word
        if not user_input[0].isalpha():
            continue
        
        # Add current user_input to user's sentence so far.
        sentence_string = ' '.join([sentence_string, user_input])
        
        all_user_sentences = auto_complete.get_user_sentences(sentence_string)
                
        # Finds the document that is most similar to the user's sentence. Uses that document for text autocomplete.    
        if len(all_user_sentences) != sentence_count:
            model_name = auto_complete.find_most_similar_model(all_user_sentences, df, False)
        
        # Use the current model and the last 2 words the user inputted to calculate the next word
        if model_name not in all_trigram_models:
            print(f'\n\tCant find "{model_name}" model.')
            return
        
        # If there wasn't any valid words to continue
        if not all_user_sentences: continue
        if not all_user_sentences[-1]: continue
        
        # Show the next work based on the previous two words
        auto_complete.show_next_word(model_name=model_name, trigram_model=all_trigram_models[model_name], show=show)
        
        
        if len(all_user_sentences) != sentence_count:
                df.remove_last_document()
                sentence_count += 1
                
        print("\n-----------------------------------------------------------------------------------------------------------------------\n")
        
        print("\n\tSentence so far: ", sentence_string)


def main():
    START_SYMBOL = "<*>"
    END_SYMBOL = "<STOP>"
    ALL_MODEL_NAME = "ALL"
    
    n_gram_tf_idf_models = N_Gram_And_TF_IDF_Models(START_SYMBOL=START_SYMBOL, END_SYMBOL=END_SYMBOL, ALL_MODEL_NAME=ALL_MODEL_NAME)
    all_trigram_models = None
    df = None
    
    # Check if the user wants to get older n-gram models and TF-IDF models from the "model" folder
    get_all_models_from_model = input('\n\tDo you get all models from the "model" folder? (Y/N): ')
    if get_all_models_from_model == 'Y' or get_all_models_from_model == 'y':
        all_trigram_models, df = n_gram_tf_idf_models.get_models_from_models_folder()
    
    # Check if user wants to get create new n-gram models and TF-IDF models from the corpus
    get_all_sentences_from_corpus = input('\n\tDo you want to create new models from the "corpus" folder? (Y/N): ')
    if get_all_sentences_from_corpus == 'Y' or get_all_sentences_from_corpus == 'y':
        all_trigram_models, df = n_gram_tf_idf_models.create_models_from_corpus()
        
        # Fix N-Grams models by adding "START_SYMBOL START_SYMBOL" and "START_SYMBOL" to the bigram count and unigram count based on how many END_SYMBOL are in the unigram count.
        all_trigram_models = n_gram_tf_idf_models.fix_n_grams_model()
    
     
    # If there is no n-gram and TF-IDF models than return.
    if not df or not all_trigram_models:
        print("\n\t - No n-gram and TF-IDF models found. Can't calculate TF-IDF or calculate auto-complete.")
        print('\t - Make sure there are files in the "model" or "corpus" folder and enter "y" when prompted.')
        return
    
    # Check if the user wants to save the current n-gram and TF-IDF models to the "model" folder
    if get_all_sentences_from_corpus == 'Y' or get_all_sentences_from_corpus == 'y':
        save_update_models = input('\n\tDo you want to save the updated models to the "model" folder? (Y/N): ')
        if save_update_models == 'Y' or save_update_models == 'y':
            n_gram_tf_idf_models.save_models_to_files()

    
    # Get user input and display the next word based on the most similar document.  
    predict_next_work(all_trigram_models, df, START_SYMBOL, END_SYMBOL, ALL_MODEL_NAME)
    
    
if __name__ == '__main__':
    main()
 
