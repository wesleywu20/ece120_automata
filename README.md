# ECE 120 Automata

Currently, this repo contains tools to help automate the manual tasks on Canvas, including:

- Discussion Grade Entry: uses the Canvas API to help you enter grades and comments on a per-group basis
- More to come!

## Usage
To use the tools in this repo, simply clone this repo:
```
git clone https://github.com/wesleywu20/ece120_automata.git
```
Then `cd` into the directory corresponding to the tool you wish to use.

## Requirements

For all tools, you will need to create your own `.env` file in the root directory of this repo with the following information:
- `ECE_120_COURSE_ID`: the course ID of the ECE 120 course on Canvas; this can be found at the end of the URL when you visit the homepage of the course:
  - `https://canvas.illinois.edu/courses/courseID`
  - Specify the course ID in the .env file using the following syntax:
  ```
  ECE_120_COURSE_ID="courseID"
  ```
- `CANVAS_API_KEY`: your personal Canvas access token, which you can generate by visiting Account > Settings and using the blue "+ New Access Token" button at the bottom of the "Approved Integrations" Section. A dialog will then pop up asking you to specify the purpose, which you can simply set to "Grade Entry Automation" or the like, and don't specify any expiration dates so that the token never expires. Once created, be sure to copy the token, otherwise you will not be able to see it again after closing the dialog!
  - Specify the Canvas API key in the .env file using the following syntax, replacing `copied_api_key` with the access key you just generated:
  ```
  CANVAS_API_KEY="copied_api_key"
  ```

## Feedback
I'm always open to feedback! If you have any suggestions for what to improve or new tools to add, feel free to send me an email at `wwu70@illinois.edu`.