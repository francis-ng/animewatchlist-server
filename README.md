# Introduction
An experimental project for a simple tracking system for anime watchers to keep track of the shows they're watching and small details like where they're watching it from and weekly release days.

Unlike most other existing heavyweight trackers that pull from databases, maintain informational libraries and may also have a social element, this is intended to be a private to-do list-style for quick memos.

# Description
This was written as much for experimentation as for practical purposes. The constraints while writing this were:

- Must use a serverless architecture
- Must stay within any available always-free limit of the hosting platform
- Must not incur any costs across all components for reasonable personal use

From these came this 3-component project.

## Backend
The original intention was for most of the server side to be hosted on AWS Lambda, but the API Gateway which is required to send HTTP requests into AWS does not have an always-free tier. The end result is that the backend handles the database and lambda functions to be invoked by the request server.

## Request server
Born out of a necessity to split the server to handle HTTP requests from the AWS infrastructure. This server receives requests from the client and transforms the data for invocation of the lambda functions.

## Client
Currently a single-page app in Vue.js acting as the client. Multiple clients for different platforms can potentially be created.

# Component repositories
Backend - https://github.com/francis-ng/animewatchlist-aws

Request server - https://github.com/francis-ng/animewatchlist-server

Client - https://github.com/francis-ng/animewatchlist-client

# Points for improvement
Currently there are assumptions the client makes regarding understanding of the application flow. There are insufficient guides on using the application and errors during requests are not displayed in a user-friendly way.