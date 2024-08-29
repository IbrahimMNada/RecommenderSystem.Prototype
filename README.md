# RecommenderSystem Based on Sql server Database as a datasource
This is a simple model for Recommender System pased on sql server as a datasource.

# Schema Overview
- **Posts Table (dbo.Posts):** Contains information about each post.
   - **Id:** Unique identifier for each post.
   - **Title:** The title of the post.
   - **Category:** The category to which the post belongs (e.g., "programming").
     
- **PostViews Table (dbo.PostViews)**: Tracks user interactions with posts.
   - **UserId: **Foreign key linking to the Users table, identifying the user.
   - **PostId:** Foreign key linking to the Posts table, identifying the post.
   - **Interest:** A column indicating the level of interest a user has shown in a post, possibly represented as an integer score.
     
- Users Table (dbo.Users): Contains user information.
   - **Id:** Unique identifier for each user.
   - **FullName:** Full name of the user.
   - **Gender:** Gender of the user.

# How Does the Model Work
1- Data Collection:
   - The recommender system uses the PostViews table to gather data on user interactions with posts. Each entry in PostViews represents a specific interaction where a user (identified by UserId) viewed or engaged with a post (identified by PostId).
   - The Interest column records the level of engagement or preference. Higher values might indicate greater interest or more positive feedback, while lower values could suggest less interest.

2- User-Post Interaction Matrix:

   - The recommender model builds a user-post interaction matrix where each row represents a user and each column represents a post.
   -  The values in this matrix are derived from the Interest column in PostViews.
         For instance, if a user showed a high level of interest in a post, the corresponding cell in the matrix will have a higher value.
      
 3- Generating Recommendations:

The model utilizes this matrix to make recommendations. Common approaches include:
   - Collaborative Filtering: Recommends posts that similar users (with similar interest patterns) have liked.
   - The other approaches will be implemented soon
     
 4-Prediction of Interest Scores:
 
 The model predicts which posts a user might be interested in by estimating the Interest score for unseen posts. Posts with higher predicted scores are more likely to be recommended to the user.

# Setting Up The Database

1. Create A Database Called :  **`[post-reccomendation-model]`**
2. Execute the Script in the File **`DataBase.sql`**
3. Fix the Connection string with your own server info at the **`post-reccomendation-model.py`**
![image](https://github.com/user-attachments/assets/5b5c3992-8419-418f-8376-59dc6cd5e784)

# Setting The Project
1. After closing the project, Open the base directory containing the file **`requirements.txt`**
2. Run this Command To create Virtual Environment 
   > python -m venv env
3. Activate the Virtual Environment using the command
   > ./env/scripts/activate
4. Now in your terminal you should see this means the Virtual Environment is active.
      ![image](https://github.com/user-attachments/assets/6d0de5e3-84a7-4437-892f-e2c5ef688bf7)

5. Now Run to install the packages related to the project
   > pip install -r requirements.txt

6. Done! you can run your Project Now, Here is what the Result looks like :

      ![image](https://github.com/user-attachments/assets/1a821ffb-0b7b-4a17-8bca-4b4b74f9cd6b)


# Result anatomy
The following exmplains the result of the predection  
1. Post Title
2. The distance between the user and the post **(positive correlation)**
3. Post Id at the Database
4. Post Category at the database (this one is not yet used in the model yet, for now we are focusing only on users not content)
5. Recommended based on user based on what user the this recommendation has been generated

<!-- > [!CAUTION]
> The Intreset Data is generated Randomly, so currently there is no pattern the model can pick up, I've Personaly tried and tested it with a small dataset and it worked fine at this point. -->

# Results of cross-validation

| Metric          | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean   | Std   |
|-----------------|--------|--------|--------|--------|--------|--------|-------|
| **RMSE (testset)** | 0.9258 | 0.9153 | 0.9219 | 0.9209 | 0.9213 | 0.9211 | 0.0034 |
| **MAE (testset)**  | 0.7175 | 0.7114 | 0.7172 | 0.7116 | 0.7141 | 0.7144 | 0.0026 |
| **Fit time (s)**   | 21.63  | 22.19  | 22.65  | 22.73  | 21.42  | 22.12  | 0.53  |
| **Test time (s)**  | 0.13   | 0.11   | 0.11   | 0.14   | 0.11   | 0.12   | 0.01  |
