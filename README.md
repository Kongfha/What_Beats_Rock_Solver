# What Beats Rock?

This project automates the process of playing the "What Beats Rock?" game using Selenium WebDriver. The goal is to find the longest possible chain of words where each word beats the previous one, starting from the word "rock".

## Project Structure

- `Example.ipynb`: Jupyter notebook for experimenting with the code.
- `Extracted_Nouns.csv`: CSV file containing a list of nouns used as vocabulary for the game.
- `main.py`: Main script to run the automation.
- `requirements.txt`: List of required Python packages.
- `utils.py`: Utility functions used in the main script.

## Requirements

- Python 3.9 or higher
- Google Chrome browser

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/what-beats-rock.git
    cd what-beats-rock
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure Google Chrome is installed on your machine.

2. Run the main script:
    ```sh
    python main.py --threshold 200
    ```

    The `--threshold` argument specifies the maximum length of the word chain to build. The default value is 200.

3. The script will load the vocabulary from `Extracted_Nouns.csv`, initialize the WebDriver, and start playing the game. It will print the longest chain found and its length.

## Algorithm

The algorithm used to build the longest chain of words is as follows:

1. **Initialization**:
    - Load the vocabulary from the CSV file.
    - Initialize the WebDriver and navigate to the game website.
    - Start the chain with the word "rock".

2. **Chain Building**:
    - Randomly pick a candidate word from the vocabulary that hasn't been used.
    - Query the game to see if the current word beats the candidate word.
    - If successful, extend the chain with the candidate word and mark it as used.
    - If unsuccessful, attempt to fallback to a previous word in the chain that can beat "rock".

3. **Fallback Logic**:
    - If the chain has more than one word, move backward to find a word that can beat "rock".
    - If found, truncate the chain at that word and continue building.
    - If not found, pick a new candidate word and continue.

4. **Termination**:
    - The process continues until the chain reaches the specified threshold or no more candidates are available.
    - The longest chain found is printed along with its length.

## Time Complexity

The time complexity of the algorithm is influenced by the number of words in the vocabulary and the threshold value. In the worst case, the algorithm may need to query the game for each word in the vocabulary multiple times, leading to a time complexity of O(n * t), where n is the number of words in the vocabulary and t is the threshold value. However, due to the randomness and fallback logic, the actual time complexity may vary.

## Example Output

```
Total vocabulary loaded: 1641
Chain extended: rock -> protection
Chain extended: rock -> protection -> operation
...
Chain extended: rock -> protection -> operation -> writer -> wind -> escape -> conversation -> combination -> profit -> watch -> pollution -> creative -> sing -> ship -> walk -> bike -> heat -> software -> poet -> gold
Reached threshold of 200 with chain length 200.

=== Final Chain ===
rock -> protection -> operation -> writer -> wind -> escape -> conversation -> combination -> profit -> watch -> pollution -> creative -> sing -> ship -> walk -> bike -> heat -> software -> poet -> gold
Length: 200
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Selenium WebDriver
- WebDriver Manager for Python
- Pandas library

