import argparse
from utils import load_vocabulary, init_driver, build_long_chain

def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--threshold', type=int, default=200, help='Threshold value for building the long chain')
    args = parser.parse_args()

    csv_path = "Extracted_Nouns.csv"
    words = load_vocabulary(csv_path)
    print(f"Total vocabulary loaded: {len(words)}")

    driver = init_driver()

    try:
        final_chain = build_long_chain(driver, words, threshold=args.threshold)
        print("\n=== Final Chain ===")
        print(" -> ".join(final_chain))
        print(f"Length: {len(final_chain)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()