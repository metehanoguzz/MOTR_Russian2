from pathlib import Path
import pandas as pd
import os


class TrialDataPreprocessor:
    def __init__(self, raw_data_path: str, new_data_path: str):
        self.raw_data_path = Path(f"{raw_data_path}")
        self.new_data_path = Path(f"{new_data_path}")
        self.preprocessed_data = None  # Initialize the preprocessed_data attribute
        self.raw_data_df = pd.read_csv(self.raw_data_path, delimiter='\t', dtype={"item_id": str, "text": str,
                                                                                  "type": str, "type_id": str,
                                                                                  "condition": str,
                                                                                  # "condition_id": str,
                                                                                  "response_true": str})

    # Check if the directory for the divided files exists, if not, make one
    def _make_directory_for_divided_data(self) -> None:
        if not os.path.exists(self.new_data_path):
            os.mkdir(self.new_data_path)

    def split_sentence_into_words(self) -> None:
        self._make_directory_for_divided_data()
        temp_dfs = []
        columns_to_process = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
        for column in columns_to_process:
            # Split the text into words and explode
            temp_df = self.raw_data_df.assign(
                word=self.raw_data_df[column].astype(str).str.split()
            ).explode('word')
            # Add AOI_id column indicating the source column
            temp_df['AOI_id'] = column
            temp_dfs.append(temp_df)

        # Combine all temporary dataframes
        preprocessed_data = pd.concat(temp_dfs, ignore_index=True)
        preprocessed_data['item_id'] = preprocessed_data['item_id'].astype(int)
        preprocessed_data['word_nr'] = preprocessed_data.groupby(['list', 'item_id']).cumcount()
        preprocessed_data['word_nr'] = preprocessed_data['word_nr'].astype(int)
        # Identify the last word in each item_id group and add a period
        last_word_indices = preprocessed_data.groupby('item_id')['word_nr'].transform('max')
        preprocessed_data.loc[preprocessed_data['word_nr'] == last_word_indices, 'word'] += '.'
        # --- not sure how to deal with the filler items ---
        preprocessed_data.loc[preprocessed_data['part'] == 'filler', 'list'] = 98
        # Sort the DataFrame by item_id and then by word_nr
        preprocessed_data = preprocessed_data.sort_values(by=['list', 'item_id', 'word_nr'])
        self.preprocessed_data = preprocessed_data

        # Save the preprocessed data to a new CSV file
        preprocessed_data.to_csv(self.new_data_path / f'preprocessed_{self.raw_data_path.stem}.csv',
                                 index=False, float_format=None)

    def filtered_new_df(self) -> None:
        df_new = self.preprocessed_data[['list', 'part', 'item_id', 'condition', 'type', 'type_id', 'target_gender',
                                         'gender_match', 'orig_item_number', 'case', 'animacy', 'word_nr',
                                         'word', 'response_true']]
        df_new = df_new.rename(columns={'condition': 'cond_id'})
        df_new.to_csv(self.new_data_path / f'filtered_preprocessed_{self.raw_data_path.stem}.csv', index=False)

# if __name__ == '__main__':
#     trial_Preprocessor = TrialDataPreprocessor("../trials/Russ_MoTR_all.tsv", "../preprocessed_trialData")
#     trial_Preprocessor.split_sentence_into_words()
#     trial_Preprocessor.filtered_new_df()
