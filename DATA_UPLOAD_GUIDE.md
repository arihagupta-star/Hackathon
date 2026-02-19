# Data Upload Guide

## Preparing Safety Incident Datasets

1. **Dataset Structure**: Ensure that each dataset is structured in a tabular format, typically as a CSV or Excel file. The first row should contain headers that describe each column.

2. **Essential Fields**:
   - **Incident ID**: Unique identifier for each incident.
   - **Date of Incident**: The date on which the incident occurred. (Format: YYYY-MM-DD)
   - **Type of Incident**: Categories or types (e.g., fire, injury, theft).
   - **Location**: Specific location of the incident.
   - **Description**: Detailed description of the incident.
   - **Outcome**: Result or resolution of the incident (if applicable).

3. **Data Quality**: Remove any duplicates, check for missing values, and ensure that the data is accurate and truthful.

4. **Normalization**: Normalize the data where necessary; for example, ensure that date formats are consistent and categorical data are standardized.


## Uploading Datasets

1. **Login**: Sign in to the portal where the datasets will be uploaded.

2. **Upload Process**:
   - Navigate to the "Data Upload" section.
   - Click on "Upload" and select your prepared dataset file.
   - Follow the prompts to upload your file securely.

3. **Validating Upload**:
   - Once uploaded, validate the dataset by checking for inconsistencies or errors in the preview.
   - Correct any errors and re-upload if necessary.

4. **Confirmation**: After successful upload, a confirmation message will appear. Ensure to save any confirmation number or email for your records.


## Training the Model with Custom Data

1. **Data Preparation**: Follow the data preparation steps outlined above to ensure the data is ready for training purposes.

2. **Choosing a Model**: Select a machine learning model that is suitable for your data type and objective (classification, regression, etc.).

3. **Training Process**:
   - Load the prepared dataset into your training environment.
   - Split the dataset into training, validation, and test sets (typically a 70-20-10 split).
   - Configure your model’s parameters and hyperparameters.
   - Train the model on the training dataset and validate on the validation dataset to ensure accuracy and prevent overfitting.

4. **Evaluation**: Once training is complete, evaluate the model’s performance on the test dataset and adjust parameters if necessary.

5. **Deployment**: Deploy the trained model to your application or service, ensuring that it can handle new incident data in real-time if required.


### Notes
- Always keep a backup of your datasets before making any changes.
- Follow company guidelines on data privacy and security when handling sensitive data.
- Document any changes made to the datasets after initial preparation.