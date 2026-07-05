import pandas as pd
import datetime as dt
import smtplib
import random
import os

# 1. Update the birthdays.csv
data = pd.read_csv('birthdays.csv')
now = dt.datetime.now()

# سحب البيانات السرية من GitHub Secrets بشكل صحيح
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD) # تعديل المتغيرات هنا لتطابق اللي فوق
    
    for index, row in data.iterrows():
        # 2. Check if today matches a birthday in the birthdays.csv
        if row["month"] == now.month and row["day"] == now.day:
            
            # 3. تعديل المسار ليكون نسبي (Relative Path) عشان يشتغل على سيرفر جيت هاب
            # تأكد إن فولدر letter_templates مرفوع مع الكود في جيت هاب
            file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
            
            with open(file_path, "r") as f:
                content = f.read()
                new_content = content.replace("[NAME]", f"{row['name']}")
                
            # 4. Send the letter generated in step 3 to that person's email address.
            connection.sendmail(
                from_addr=MY_EMAIL, # تعديل المتغير هنا
                to_addrs=row["email"],
                msg=f"Subject: Happy Birthday!\n\n{new_content}"
            )
