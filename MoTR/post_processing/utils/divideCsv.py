from pathlib import Path
import pandas as pd
import os


class FileDivider:
    """
    A class that divides a raw data file containing reading data for all participants into separate files for each participant.
    """

    def __init__(self, raw_data_path, new_data_path):
        # Initialize the FileDivider object with the paths of the raw data file and the directory for the divided files.
        # self.raw_data_path = Path(f"{raw_data_path}")
        self.raw_data_path = raw_data_path
        # self.new_data_path = Path(f"{new_data_path}")
        self.new_data_path = new_data_path
        self.raw_data_df = pd.read_csv(self.raw_data_path, dtype={"Index": str, "ItemId": str,
                                                                  "Condition": str, "Experiment": str,
                                                                  "mousePositionX": str, "mousePositionY": str})

    # Check if the directory for the divided files exists, if not, make one
    def _make_directory_for_divided_data(self) -> None:
        if not os.path.exists(self.new_data_path):
            os.mkdir(self.new_data_path)

    def divide_raw_file(self) -> None:
        self._make_directory_for_divided_data()
        # Fill any NaN values in the 'response' column and preprocess other columns.
        self._fill_nan_response_column()
        # Group the data by 'submission_id' and create separate files for each group/participant.
        grouped_data = self.raw_data_df.groupby('submission_id')
        for submission_id, group in grouped_data:
            # Use factorize to assign a unique sequential ID to each unique ItemId in the order they appear
            # Adjust the starting point from 0 to -3 --> we have 4 practice trials
            group['trial_id'] = pd.factorize(group['ItemId'])[0] - 3

            for item_id, indices in group.groupby('ItemId').groups.items():
                # Check if 'List' values are all NA within this group
                if group.loc[indices, 'List'].isna().all():
                    group.loc[indices, 'List'] = 3
                else:
                    # Apply forward fill within this group
                    group.loc[indices, 'List'] = group.loc[indices, 'List'].fillna(method='ffill')

                if group.loc[indices, 'response'].isna().all():
                    group.loc[indices, 'response'] = '%2c#'
                else:
                    # Apply forward fill within this group
                    group.loc[indices, 'response'] = group.loc[indices, 'response'].fillna(method='bfill')


            group['List'] = group['List'].astype(int)
            group.to_csv(self.new_data_path / f'reader_{submission_id}.csv', index=False, float_format=None)

    def _fill_nan_response_column(self) -> None:
        # Fill NaN values in different columns and perform necessary type conversions.
        # This ensures the data is in the correct format for further processing.
        # self.raw_data_df['response'].fillna(method='bfill', inplace=True)
        self.raw_data_df['ItemId'].fillna(method='ffill', inplace=True)
        self.raw_data_df.dropna(subset=['ItemId'], inplace=True)
        self.raw_data_df['ItemId'] = self.raw_data_df['ItemId'].astype(float)
        self.raw_data_df['ItemId'] = self.raw_data_df['ItemId'].astype(int)
        self.raw_data_df['Type'].fillna(method='ffill', inplace=True)
        self.raw_data_df['Type'] = self.raw_data_df['Type'].astype(float).astype(int)
        self.raw_data_df['Condition'].fillna(method='ffill', inplace=True)
        self.raw_data_df['Condition'] = self.raw_data_df['Condition'].astype(str)
        self.raw_data_df['Index'].fillna(value=-100, inplace=True)
        self.raw_data_df['Index'] = self.raw_data_df['Index'].astype(float).astype(int)
        # self.raw_data_df['Word'].fillna(value="NULL", inplace=True)
        self.raw_data_df['mousePositionX'].fillna(value=425, inplace=True)
        self.raw_data_df['mousePositionX'] = self.raw_data_df['mousePositionX'].astype(float).astype(int)
        self.raw_data_df['mousePositionY'].fillna(value=285, inplace=True)
        self.raw_data_df['mousePositionY'] = self.raw_data_df['mousePositionY'].astype(float).astype(int)
        self.raw_data_df['device'].fillna(method='bfill', inplace=True)
        self.raw_data_df['device'] = self.raw_data_df['device'].astype(str)
        self.raw_data_df['hand'].fillna(method='bfill', inplace=True)
        self.raw_data_df['hand'] = self.raw_data_df['hand'].astype(str)
        self.raw_data_df['otherDevice'].fillna(method='bfill', inplace=True)
        self.raw_data_df['otherDevice'] = self.raw_data_df['otherDevice'].astype(str)
        self.raw_data_df['russianCountry'].fillna(method='bfill', inplace=True)
        self.raw_data_df['russianCountry'] = self.raw_data_df['russianCountry'].astype(str)
        self.raw_data_df['russianCountry2'].fillna(method='bfill', inplace=True)
        self.raw_data_df['russianCountry2'] = self.raw_data_df['russianCountry2'].astype(str)



