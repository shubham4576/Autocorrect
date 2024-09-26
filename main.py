import language_tool_python
from textblob import TextBlob
from spellchecker import SpellChecker
import re


class TextCorrector:
    def __init__(self):
        self.spell = SpellChecker()
        self.tool = language_tool_python.LanguageTool('en-US')

        # Common confused words mapping
        self.confused_words = {
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

    def context_based_corrections(self, text):
        """Apply regex or context-based corrections for additional rules."""
        text = re.sub(r"\byour\b (is|are|was|were|be|been|being)", "you're \\1", text)
        text = re.sub(r"\btheir\b (is|are|was|were|be|been|being)", "they're \\1", text)
        return text

    def spell_check(self, text):
        """Correct spelling in the input text."""
        words = text.split()
        corrected_words = []

        for word in words:
            corrected_word = self.spell.candidates(word)
            if word not in corrected_word:
                corrected_words.append(self.spell.candidates(word).pop())  # Use the first suggestion
            else:
                corrected_words.append(word)

        return " ".join(corrected_words)

    def grammar_check(self, text):
        """Correct grammar using LanguageTool."""
        matches = self.tool.check(text)
        return language_tool_python.utils.correct(text, matches)

    def autocorrect_text(self, text):
        """Main function to perform autocorrection."""
        # Step 1: Spell checking
        corrected_sentence = self.spell_check(text)

        # Step 2: Further correction using TextBlob
        text_blob = TextBlob(corrected_sentence)
        text_blob_corrected = str(text_blob.correct())

        # Step 3: Handle commonly confused words
        for incorrect, correct in self.confused_words.items():
            text_blob_corrected = text_blob_corrected.replace(incorrect, correct)

        # Step 4: Apply context-based corrections
        text_blob_corrected = self.context_based_corrections(text_blob_corrected)

        # Step 5: Final grammar correction using LanguageTool
        final_corrected_sentence = self.grammar_check(text_blob_corrected)

        return final_corrected_sentence


def main():
    # Example usage
    input_text = "Their coming to the store tomoro."
    corrector = TextCorrector()
    corrected_text = corrector.autocorrect_text(input_text)
    print("Original Text:", input_text)
    print("Corrected Text:", corrected_text)


if __name__ == '__main__':
    main()
