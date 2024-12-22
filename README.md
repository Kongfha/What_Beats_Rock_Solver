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

The algorithm builds the longest chain of words in the "What Beats Rock?" game using the following steps:

1. **Initialization**:
    - Load the vocabulary \( V \) from `Extracted_Nouns.csv`.
    - Initialize the WebDriver and navigate to the game website.
    - Set the starting chain \( C \) to \(["rock"]\) and mark "rock" as used.

2. **Chain Building**:
    - While \( |C| < \text{threshold} \):
        - Randomly select a candidate \( w \in V \) such that \( w \notin C \).
        - Query the game for \( \text{last}(C) \to w \):
            - If true: Append \( w \) to \( C \).
            - If false: Attempt fallback.

3. **Fallback Logic**:
    - Traverse \( C \) backward to find a node \( w' \) such that \( w' \to \text{"rock"} \).
    - If \( w' \) is found, truncate \( C \) to \( C[:w'] \) and continue.
    - If no fallback is found, skip to the next candidate.

4. **Termination**:
    - Stop when \( |C| = \text{threshold} \) or no more candidates are available.
    - Output \( C \) as the longest chain found.

## Time Complexity

Let \( n \) be the number of words in the vocabulary and \( t \) the threshold:

1. **Chain Extension**:
    - For each successful query, the algorithm performs \( O(1) \) work to append to \( C \).
    - Worst case: \( O(n) \) queries for all words in \( V \).

2. **Fallback Logic**:
    - On failure, up to \( O(t) \) queries are performed in the worst-case backward traversal of \( C \).
    - Worst-case fallback cost per failure: \( O(t) \).

3. **Total Cost**:
    - In the worst case, all \( n \) words are queried, and each fallback requires \( O(t) \) checks.
    - Total: \( O(n \times t) \).

**Expected Performance**:
- Random candidate selection and early successes reduce fallback costs.
- Practical complexity is closer to \( O(n) \) for moderate \( t \) (e.g., 200).

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

