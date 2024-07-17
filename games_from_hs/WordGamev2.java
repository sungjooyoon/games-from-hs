// Importing two libraries for input and RNG
import java.util.Scanner;
import java.util.Random;

// Declaring class and reference variables
public class WordGame {
    private String[] secretWord;
    private int numGuesses;

    // Declaring number of guesses as 0
    // Initializes game and splits word into array
    public WordGame(String word) {
        numGuesses = 0;
        secretWord = new String[word.length()];
        for (int i = 0; i < word.length(); i++) {
            secretWord[i] = word.substring(i, i + 1);
        }
    }

    // Method that retrieves secret word as string
    public String getSecretWord() {
        String ans = "";
        for (int i = 0; i < secretWord.length; i++) {
            ans += secretWord[i];
        }
        return ans;
    }

    // Method that helps us discern length of word
    public int getWordLength() {
        return secretWord.length;
    }

    // Method that checks if given letter is in word
    private boolean letterOccurs(String letter) {
        for (String s : secretWord) {
            if (s.equals(letter))
                return true;
        }
        return false;
    }

    // Feedback hints for user (i.e. right letter, right place)
    private String getHint(String guess) {
        String ans = "";
        if (guess.length() != secretWord.length) {
            ans = "Your guess is the wrong length!";
        } else {
            for (int i = 0; i < guess.length(); i++) {
                String local = guess.substring(i, i + 1);
                if (letterOccurs(local) && guess.indexOf(local) == getSecretWord().indexOf(local)) {
                    ans += local;
                } else if (letterOccurs(local) && guess.indexOf(local) != getSecretWord().indexOf(local)) {
                    ans += "+";
                } else {
                    ans += "*";
                }
            }
        }
        return ans;
    }

    // Function that allows us to verify user's input against the right answer
    // Also serves to print feedback based on accuracy
    public String makeGuess(String guess) {
        String answer = "";
        if (!getSecretWord().equals(guess)) {
            answer = "Incorrect. Hint: " + getHint(guess);
            numGuesses++;
        } else {
            numGuesses++;
            answer = "Correct! It took " + numGuesses + " tries to get " + getSecretWord() + ".";
        }
        return answer;
    }

    // Method that returns binary on if game is over or not
    public boolean gameOver(String guess) {
        return guess.equals(getSecretWord());
    }

    // Initializes array of common words, RNG a word and take input
    public static void main(String[] args) {
        String[] commonWords = {
            "ability", "above", "accept", "according", "account", "across", "act", "action", "activity", "actually",
            "add", "address", "administration", "admit", "adult", "affect", "after", "again", "against", "age",
            "agency", "agent", "ago", "agree", "agreement", "ahead", "air", "all", "allow", "almost",
            "alone", "along", "already", "also", "although", "always", "American", "among", "amount", "analysis",
            "and", "animal", "another", "answer", "any", "anyone", "anything", "appear", "apply", "approach",
            "area", "argue", "arm", "around", "arrive", "art", "article", "artist", "as", "ask",
            "assume", "at", "attack", "attention", "attorney", "audience", "author", "authority", "available", "avoid",
            "away", "baby", "back", "bad", "bag", "ball", "bank", "bar", "base", "be",
            "beat", "beautiful", "because", "become", "bed", "before", "begin", "behavior", "behind", "believe"
        };
        Random random = new Random();
        Scanner scanner = new Scanner(System.in);

        String word = commonWords[random.nextInt(commonWords.length)];
        WordGame game = new WordGame(word);

        // Introduce user to game, provide first clue
        System.out.println("Welcome to the Word Guessing Game!");
        System.out.println("Guess the word! It has " + game.getWordLength() + " letters.");

        // Loop that continues to take feedback while game is still running
        // Also allows for exit condition
        while (true) {
            System.out.print("Enter your guess: ");
            String guess = scanner.nextLine();

            if (guess.equalsIgnoreCase("exit")) {
                System.out.println("Game exited. The word was: " + game.getSecretWord());
                break;
            }

            String response = game.makeGuess(guess);
            System.out.println(response);

            // Win condition is met
            if (game.gameOver(guess)) {
                System.out.println("Congratulations! You've guessed the word correctly.");
                break;
            }
        }

        scanner.close();
    }
}
