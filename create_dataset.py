import pandas as pd


# Data structure
data = {
    "Broad Category": [
        "Politics", "Politics", "Politics", "Politics",
        "Crime", "Crime", "Crime", "Crime",
        "Crime", "Crime", "Crime", "Crime",
        "Crime", "Crime", "Crime", "Crime",
        "Crime", "Crime", "Crime", "Crime",
        "Corruption", "Corruption",
        "Accident", "Accident", "Accident", "Accident",
        "Accident"
    ],
    "Subcategory": [
        "Political news", "Political news", "International and internal affairs", "International and internal affairs",
        "Terrorism / Terrorist", "Terrorism / Terrorist", "Extremism / Extremist", "Extremism / Extremist",
        "Murder / Homicide", "Murder / Homicide", "Narcotics", "Narcotics",
        "Suicide", "Suicide", "Genocide", "Genocide",
        "Organized Crime and Criminal Group", "Organized Crime and Criminal Group", "Ammunition", "Ammunition",
        "Human Trafficking", "Human Trafficking",
        "Bribery", "Bribery",
        "Road accident", "Road accident", "Fire accident", "Fire accident",
        "Environmental disaster"
    ],
    "Item": [
        "মার্চ ফর ইউনিটি’ কর্মসূচি পালন",
        "দেয়ালে দেয়ালে ‘জয় বাংলা’ স্লোগান, সিসিটিভি ফুটেজে চাঞ্চল্যকর দৃশ্য",
        "মার্কিন অভিবাসন নীতির ওপর বিতর্ক, ট্রাম্প প্রশাসনের ভিন্নমত",
        "বিশ্ব দরবারে বাংলাদেশের ভাবমূর্তির ওপর ভারতীয় থাবা",
        "বান্দরবানে জঙ্গি বলে গ্রেপ্তার সেই ২৮ জনের জামিন বাতিল",
        "কারাগার থেকে পালানো ৭৯ ‘জঙ্গি’ এখনো পলাতক, তাঁদের ৯ জন সাজাপ্রাপ্ত",
        "ভোলায় আসামিকে গ্রেফতার করতে গিয়ে হামলা, পুলিশের দুই সদস্য আহত",
        "বান্দরবান জেলা পরিষদ চেয়ারম্যানকে ‘প্রাণনাশের হুমকি’",
        "মোহাম্মাদপুরে ছুরিকাঘাতে তরুণের মৃত্যু",
        "রাজধানীতে বাস মালিককে কুপিয়ে হত্যা",
        "টেকনাফের নাফ নদীতে কোস্টগার্ডের সঙ্গে ‘মাদক কারবারিদের’ গোলাগুলি, একজন নিহত",
        "খ্রিষ্টীয় বর্ষবরণের রাতে গুলশান-বনানীর হোটেলে অভিযান, মদ ও বিয়ার উদ্ধার",
        "দুর্গন্ধের উৎস খুঁজতে গিয়ে শ্বশুরবাড়িতে মিলল যুবকের লাশ",
        "মেয়েকে নিয়ে ট্রেনের নিচে ঝাঁপ দিলেন বাক্‌প্রতিবন্ধী বাবা",
        "আন্তর্জাতিক আদালতের প্রধান কৌঁসুলির সঙ্গে জুলাই-আগস্ট গণহত্যা নিয়ে আলোচনা",
        "‘গণহত্যা’র বিচারে জাতিসংঘের সহযোগিতা চেয়েছে জামায়াত",
        "কক্সবাজারে দুই তরুণীকে মারধর: জানা গেল সংঘবদ্ধ চক্রের তথ্য",
        "অটোরিকশার চালক সেজে ছিনতাই করেন তাঁরা, সংঘবদ্ধ চক্রের নাম ‌‌হামকা গ্রুপ",
        "রংপুরে পি'স্ত'ল'স'হ ৪ তরুণ-তরুণীকে আটক করেছে তাজহাট থানা পুলিশ",
        "পাবনায় সেনাবাহিনীর অভিযানে অস্ত্রসহ সন্ত্রাসী বাবু গ্রেফতার",
        "বরিশালে মানব পাচার মামলায় প্রবাসী দুই ভাই ও ভাবির বিভিন্ন মেয়াদে কারাদণ্ড",
        "মানব পাচার মামলায় চার দিনের রিমান্ডে মিল্টন সমাদ্দার",
        "৩ শিক্ষা বোর্ডে অডিটে গিয়ে ৩৯ লাখ টাকা ঘুষ নেওয়ার অভিযোগ, জমা হয় স্বজনের হিসাবে",
        "এনআইডি সংশোধনে ঘুষ লেনদেনের অভিযোগ, নির্বাচন ভবন এলাকায় দুদকের অভিযান",
        
    ]
}
# Convert to a DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = "topic_modeling_dataset.xlsx"
df.to_excel(output_file, index=False)

print(f"Dataset saved to {output_file}")
