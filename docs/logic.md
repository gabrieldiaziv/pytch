# Business logic

## Auth

- After user login to website, a valid session is made in Auth0
- website can use the session token from authenticated requests to trpc to make requests to flask
- authenticating in flask
  - get "authorization" header from request, value is "Bearer JWT"
  - verify JWT with auth0
