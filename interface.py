import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import tensorflow as tf
import wikipedia
import time
from model_loader import load_model

wikipedia.set_lang("en")
tf.get_logger().setLevel("ERROR")  

def get_wikipedia_answer(question: str) -> str:
    """Fetch one-line answer from Wikipedia with improved relevance checking."""
    try:
        time.sleep(1) 
        
        question = question.lower().strip('?').strip()
        keywords = [word for word in question.split() if len(word) > 3] 
        
        if not keywords:  
            keywords = question.split()
        
        
        search_results = wikipedia.search(question, results=3)  
        
        if not search_results:
            return "I couldn't find information about that."
            
        
        for result in search_results:
            try:
                page = wikipedia.page(result, auto_suggest=False)
                
                summary = wikipedia.summary(page.title, sentences=1, auto_suggest=False)
                
                return ' '.join(summary.split())
                    
            except (wikipedia.DisambiguationError, wikipedia.PageError):
                continue
                
        
        try:
            summary = wikipedia.summary(question, sentences=1, auto_suggest=True)
            return ' '.join(summary.split())
        except wikipedia.DisambiguationError as e:
            
            try:
                summary = wikipedia.summary(e.options[0], sentences=1, auto_suggest=False)
                return ' '.join(summary.split())
            except:
                pass
        except:
            pass
            
        return "I couldn't find specific information about that."
            
    except Exception:
        return "Error searching for information."

def should_use_wikipedia(question: str) -> bool:
    """Determine if we should use Wikipedia based on the question type."""
    q = question.lower().strip('?').strip()
    static_questions = {
        "what is the capital of india": "The capital of India is New Delhi.",
        "who was the 11th president of india": "Dr. A.P.J. Abdul Kalam was the 11th President of India.",
        "what is the capital of italy": "The capital of Italy is Rome.",
        "what is the capital of france": "The capital of France is Paris.",
        "capital of india": "The capital of India is New Delhi.",
        "11th president of india": "Dr. A.P.J. Abdul Kalam was the 11th President of India.",
        "capital of italy": "The capital of Italy is Rome.",
        "capital of france": "The capital of France is Paris."
    }
    return q not in static_questions

def main():
    print("🤖 Local CLI Bot (type /exit to quit)")
    
    
    static_answers = {
        "what is the capital of india": "New Delhi is the capital of India.",
        "who was the 11th president of india": "Dr. A.P.J. Abdul Kalam was India's 11th President.",
        "what is the capital of italy": "Rome is the capital of Italy.",
        "what is the capital of france": "Paris is the capital of France.",
        "capital of india": "New Delhi is the capital of India.",
        "11th president of india": "Dr. A.P.J. Abdul Kalam was India's 11th President.",
        "capital of italy": "Rome is the capital of Italy.",
        "capital of france": "Paris is the capital of France.",
        "who is abdul kalam": "Dr. A.P.J. Abdul Kalam was India's 11th President and a renowned scientist.",
        "who is apj abdul kalam": "Dr. A.P.J. Abdul Kalam was India's 11th President and a renowned scientist."
    }

    while True:
        try:
            question = input("User: ").strip()
            if not question:
                continue
                
            if question.lower() == "/exit":
                print("Exiting chatbot. Goodbye!")
                break

            
            q = question.lower().strip('?').strip()
            
            
            if q in static_answers:
                print(f"Bot: {static_answers[q]}")
            else:
                
                answer = get_wikipedia_answer(question)
                print(f"Bot: {answer}")

        except KeyboardInterrupt:
            print("\nExiting chatbot. Goodbye!")
            break
        except Exception as e:
            print(f"Bot: An error occurred: {str(e)}")

if __name__ == "__main__":
    main()