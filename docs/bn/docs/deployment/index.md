# Deployment { #deployment }

একটি **FastAPI** application deploy করা তুলনামূলক সহজ।

## Deployment মানে কী { #what-does-deployment-mean }

একটি application **deploy** করা মানে সেটাকে **users-এর জন্য available** করতে দরকারি ধাপগুলো করা।

একটি **web API**-এর ক্ষেত্রে, সাধারণত এটাকে একটি **remote machine**-এ রাখা হয়, এমন একটি **server program** দিয়ে যেটা ভালো performance, stability, ইত্যাদি দেয়, যাতে আপনার **users** কোনো বাধা বা সমস্যা ছাড়া ঠিকমতো application-টা **access** করতে পারে।

এটা **development** stages-এর উল্টো, যখন আপনি সারাক্ষণ code বদলাচ্ছেন, ভাঙছেন আর ঠিক করছেন, development server বন্ধ করে আবার চালু করছেন, ইত্যাদি।

## Deployment Strategies { #deployment-strategies }

আপনার নির্দিষ্ট use case আর আপনার ব্যবহার করা tools-এর উপর নির্ভর করে এটা করার কয়েকটা উপায় আছে।

কয়েকটা tools মিলিয়ে নিজেই **একটি server deploy** করতে পারেন, এমন একটি **cloud service** ব্যবহার করতে পারেন যেটা আপনার জন্য কাজের একটা অংশ করে দেয়, বা অন্য উপায়ও আছে।

যেমন, আমরা, মানে FastAPI-এর পেছনের team, [**FastAPI Cloud**](https://fastapicloud.com) বানিয়েছি, যাতে FastAPI apps cloud-এ deploy করা যতটা সম্ভব সহজ হয়, FastAPI নিয়ে কাজ করার একই developer experience সহ।

একটি **FastAPI** application deploy করার সময় যেসব মূল concepts সম্ভবত মাথায় রাখা উচিত, তার কয়েকটা আপনাকে দেখাব (যদিও এর বেশিরভাগই অন্য যেকোনো ধরনের web application-এর ক্ষেত্রেও খাটে)।

পরের sections-গুলোতে মাথায় রাখার মতো আরও details আর এটা করার কিছু কৌশল দেখবেন। ✨
