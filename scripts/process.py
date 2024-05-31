import argparse
from data_analysis.processing_pipeline import (
    load_data,
    create_corpus,
    clean_corpus_step,
    remove_stopwords_step,
    tokenize_step,
    train_model_step,
    create_bag_of_words_step,
    get_metadata,
    get_vizualition_data
)


def main(steps):
    if 'load_data' in steps:
        df = load_data()
        print(f"Número de registros: {df.shape[0]}")
        print(f"Universidades: {len(df['university'].unique())}\n{df['university'].unique()}")

    if 'create_corpus' in steps:
        create_corpus()

    if 'clean_corpus' in steps:
        clean_corpus_step()

    if 'remove_stopwords' in steps:
        remove_stopwords_step()

    if 'tokenize' in steps:
        tokenize_step()

    if 'create_bag_of_words' in steps:
        create_bag_of_words_step()

    if 'train_model' in steps:
        train_model_step()

    if 'metadata' in steps:
        get_metadata()

    if 'visualization_data' in steps:
        get_vizualition_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Selecciona las fases del proceso a ejecutar")
    parser.add_argument('--steps', nargs='+',
                        choices=['load_data', 'create_corpus', 'clean_corpus', 'remove_stopwords', 'tokenize',
                                 'create_bag_of_words', 'train_model', 'metadata', 'visualization_data'],
                        required=True,
                        help='Fases del proceso a ejecutar')
    args = parser.parse_args()
    main(args.steps)
