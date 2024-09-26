import language_tool_python
from textblob import TextBlob
from spellchecker import SpellChecker

# Initialize tools
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')

# Common confused words mapping
confused_words = {
    "their": "they're",
    "there": "they're",
    "your": "you're",
    "its": "it's",
    "its'": "it's",
    "Their": "They're",
    "There": "They're",
    "Your": "You're",
    "Its": "It's",
    "Its'": "It's"
}


def autocorrect_text(text):
    # Step 1: Spell checking using SpellChecker
    words = text.split()
    corrected_words = []

    for word in words:
        # Correct spelling if needed
        corrected_word = spell.candidates(word)
        if word not in corrected_word:
            corrected_words.append(spell.candidates(word).pop())  # Use the first suggestion
        else:
            corrected_words.append(word)

    # Join corrected words into a sentence
    corrected_sentence = " ".join(corrected_words)

    # Step 2: Further correction using TextBlob
    text_blob = TextBlob(corrected_sentence)
    text_blob_corrected = str(text_blob.correct())

    # Step 3: Handle commonly confused words
    for incorrect, correct in confused_words.items():
        text_blob_corrected = text_blob_corrected.replace(incorrect, correct)

    # Step 4: Final grammar correction using LanguageTool
    matches = tool.check(text_blob_corrected)
    final_corrected_sentence = language_tool_python.utils.correct(text_blob_corrected, matches)

    return final_corrected_sentence


if __name__ == '__main__':
    # Test the enhanced autocorrect functionality
    input_text = "Their coming to the store tomoro."
    corrected_text = autocorrect_text(input_text)
    print("Original Text:", input_text)
    print("Corrected Text:", corrected_text)
