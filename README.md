# Kutiva
Kutiva is a elearning plattform based on web and mobile apps. Kutiva provides courses
developed for subscribed mentors and approved for Kutiva Team for each customer who
want to buy. Actually, the payment method is based on product model.

# API
Kutiva API is an application programming interface which provides to client application
data queried from Kutiva database. The API is permanently accessible only for Kutiva
applications, whichs means it is private.

# Basics
We cover more about Kutiva API on [], in the following sections we explain more about
the kind of requests can be performed and how can be performed with concrete code examlse

# Reading
All edges in the Kutiva API can be read by just an HTTP 'GET' request to the desired endpoint.
Be aware sometimes will need to set some args to the URL in order you can get more specific data,
example, if want to get information about a specific Kutiva Mentor just need to send a request as
follows:
'''
GET api.kutiva.co.mz/Account/Mentors/<id>
'''
# Usage

## Users
