# What Beats Rock? Solver
This project automates the process of playing the "What Beats Rock?" game using Selenium WebDriver. The goal is to find the longest possible chain of words where each word beats the previous one, starting from the word "rock".
## Introduction

I started this project because I was bored and thought, "Why not try to beat this ridiculous but fun game, 'What Beats Rock?'" Instead of guessing words myself, I figured I’d let some code do the work for me. And here we are.



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

The algorithm builds the longest chain of words in the "What Beats Rock?" game using the following steps:

1. **Initialization**:
    - Load the vocabulary `V` from `Extracted_Nouns.csv`.
    - Initialize the WebDriver and navigate to the game website.
    - Set the starting chain `C = ["rock"]` and mark "rock" as used.

2. **Chain Building**:
    - While the length of the chain `len(C)` is less than the threshold:
        - Randomly select a candidate word `w` from `V` such that `w` is not in `C`.
        - Query the game to check if the last word in the chain beats `w`:
            - If true, append `w` to `C`.
            - If false, attempt fallback.

3. **Fallback Logic**:
    - Traverse the chain `C` backward to find a node `w'` such that `w'` beats "rock."
    - If `w'` is found, truncate `C` to remove all words after `w'` and continue.
    - If no fallback node is found, skip to the next candidate.

4. **Termination**:
    - Stop when the chain reaches the threshold length or no more candidates are available.
    - Output the longest chain `C` found.

## Time Complexity

Let `n` be the number of words in the vocabulary and `t` be the threshold:

1. **Chain Extension**:
    - Each query to extend the chain takes constant time, `O(1)`.
    - In the worst case, the algorithm may query all `n` words in the vocabulary, resulting in `O(n)` total extension queries.

2. **Fallback Logic**:
    - On failure, the algorithm may perform up to `t` queries during a backward traversal of the chain.
    - Worst-case fallback cost per failure is `O(t)`.

3. **Total Cost**:
    - In the worst case, the algorithm makes `n` queries, with each failure incurring up to `t` additional fallback queries.
    - Total complexity: `O(n * t)`.

**Expected Performance**:
- Random candidate selection and early successes reduce the number of fallback queries.
- For moderate threshold values (e.g., `t = 200`), practical complexity is closer to `O(n)`.

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

