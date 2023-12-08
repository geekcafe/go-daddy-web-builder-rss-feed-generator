# Readme.md GoDaddy Web Builder RSS Feeds

## 🤔 Situation:
On the GoDaddy Web Builder platform, there is a limitation as it does not support RSS feeds, and the platform does not allow the placement of .XML files on the site. This creates a challenge for users who want to implement an RSS feed on their websites.

## ✅ Task:
The task at hand is to find a solution that enables the creation and hosting of an RSS feed despite the constraints imposed by the GoDaddy Web Builder platform.

## ⚡️ Action:
To overcome the limitations of GoDaddy, I developed a program capable of reading responses from the Web Builder blog feeds. This program effectively acts as a bridge, allowing the extraction of content from the Web Builder blogs to construct a functional RSS feed.

To further ensure accessibility and reliability, I implemented an AWS deployment. The RSS feed is hosted on CloudFront, providing a scalable and efficient solution. This circumvents any issues posed by GoDaddy's restrictions and ensures a seamless experience for users accessing the RSS feed.

## 🍦 Result:
The end result is a fully functional RSS feed that operates independently of GoDaddy's limitations. Users can now enjoy the benefits of an RSS feed on their websites without being hindered by the constraints of the Web Builder platform. The AWS deployment on CloudFront guarantees stability and accessibility for the hosted feed.

## 📊 Metrics:
While the solution has been successfully implemented, the determination of metrics for the RSS feed is still pending. Metrics such as user engagement, click-through rates, and overall feed performance will be assessed to gauge the effectiveness and impact of the RSS feed on the audience.

This innovative approach not only addresses the immediate challenge but also provides a robust and scalable solution that aligns with the evolving needs of the platform and its users.

## 🏛️ Architecture

### 🐍 Python Code
Python Code for "scraping" the feed.  This techincally isn't scraping since I'm reading an endpoint that has blog meta-data.

To find your blog endpoint. Use an inspection tool like Google Chome Dev Tools.  Find url like
`https://blog.apps.secureserver.net/v1/website/<some-uuid>/feed?pageItems=1000`

You can request any number of items to be loaded.  For this round, I'm lazy and I'm requesting 1000 for a site that I know last less than that.  A future version will read it until there aren't any more results.

The `app.py` orchestrates the feed build.




### ☁️ AWS Environment
I'm using an S3 bucket for the file storage and CloudFront to serve the file(s) - the `rss-feed.xml` as a CDN

You can get a free SSL Cert from AWS and bind it to CloudFront.  As long as it's in use and bound to an AWS resource (like CloudFront) it will auto-renew and there's no cost to you.

### 🗓️ Automation / Scheduling
I'll be using event bridge to schedule a daily refresh.
I'll get that working this weekend (mostlikely)



### 💰 Cost 
TBD.  I'll update this in a month or so to see the cost but I expect it to be pennies per month.

