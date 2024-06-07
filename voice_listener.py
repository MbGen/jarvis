import speech_recognition as sr

def get_text_from_speech() -> str:
    # Initialize the recognizer 
    r = sr.Recognizer() 

    try:
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("You can speak now ... ") 
            #listens for the user's input 
            audio2 = r.listen(source2)
            
            # Using google to recognize audio
            recognized_text = r.recognize_google(audio2)
            recognized_text = recognized_text.lower()
            print("Did you say ", recognized_text)
            return recognized_text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""
    except sr.UnknownValueError:
        print("unknown error occurred")
        return ""
        