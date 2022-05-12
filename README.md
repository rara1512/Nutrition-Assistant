# Nutrition-Assistant
For this project, we have used python’s streamlit library to make a web application, making it easy for the users. It was aimed at making this project more practical and ready to use for business purposes. 

Here’s a look at the web application

![alt text](https://github.com/rara1512/Nutrition-Assistant/blob/main/Home.PNG?raw=true)

The first step is to select the dietary preference. We have included three popular dietary labels as shown below. The user can either choose his preference or skip it.

![alt text](https://github.com/rara1512/Nutrition-Assistant/blob/main/Parameters.PNG?raw=true)

After selecting the preferences, the next step is to use the three sliders corresponding to the three macronutrients, to select the minimum amount of macronutrients the user wants in his recommended dish. The slider has values between 0 to 100 which denotes the daily recommended value of the macronutrients in percentage. 
If the slider is set to 5% for carbohydrates, only dishes containing equal to, or greater than 5% daily value of carbohydrates would be recommended to the user.
After choosing the desired parameters, the next step is to click proceed as shown in the above image. 
A drop down menu with a list of dishes will appear as shown below

![alt text](https://github.com/rara1512/Nutrition-Assistant/blob/main/DropDown.PNG?raw=true)

The user then has to select a dish that he likes from the drop down menu and click View Recommendations to see a customized list of recommendations.

![alt text](https://github.com/rara1512/Nutrition-Assistant/blob/main/Recommendation.PNG?raw=true)

The user can then decide what to eat based on the nutrient values of the recommended dishes.

All the algorithms described above have been abstracted from the user this way. Based on the changes made on the web app, the python code will run and produce the results.
