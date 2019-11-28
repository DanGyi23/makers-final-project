[![Build Status](https://travis-ci.com/DanGyi23/makers-final-project.svg?branch=master)](https://travis-ci.com/DanGyi23/makers-final-project)


# Grandmasters Slack-Based Chess Game

<kbd>
  <img src="https://github.com/DanGyi23/makers-final-project/blob/master/docs/Final_slack_version.png">
</kbd>


### Setup
- Ensure you have [Python3.7.5](https://www.python.org/downloads/release/python-375/) and [PIP](https://pypi.org/project/pip/) installed
- RUN ALL commands in Setup.md file in the root directory of this REPO
<br><br><br>



**Running the game in command line**
- open python interpreter - e.g. `python3` on Mac from the src directory
- `import ui`
- `ui = ui.UI()`
- `ui.start()`
<br><br><br>

**Running the game in Slack**
- If you want to run in slack, then ensure you have slackclient installed (`python3 -m pip install slackclient`) and the env variable passed when starting the python interpreter in src directory (e.g. `SLACK_API_TOKEN="token" python3 slack_ui.py`)

- Open up your workspace and invite Chessy! `/invite @Chessy`
<br><br><br>

**Running Tests**
- Once pytest is installed, as per Setup MD, you can run tests from your project directory in CMD using `python3 -m pytest`
- To include coverage, use `python3 -m pytest ./`
<kbd>
  <img src="https://github.com/DanGyi23/makers-final-project/blob/master/docs/pytest-coverage.png">
</kbd>

<br><br><br>

### Techstack  
-------------------


| Tech used        | What does it do?    | How we used it  |
| :----------------: |:-----------------------------:| :------------------:|
| Python 3   | Backend, (MVC)      | In MVC layers   |
| Pytest      | Python Testing Framework  | TDD, TDD, TDD!                |
| Pytest-Cov      | Measures test coverage  | Measure test coverage                |
| Slack API  | Allows you to interface with Slack   | Created an API with our Python Chess Logic |
| SlackClient           | Launches your Slack App from CMD with an AUTH token | Resurrecting Chessy the Chess Bot      |
| CairoSVG    | Converts SVG format images to other image types | Converting SVG to PNG and rendering the current board   |
| Python-Chess     | Python Chess Library | **ONLY** used for front-end board-rendering      |
| Pillow      | Python Image Library | Manipulating Images/saving files in board rendering |
| Travis           | CI Tool                    | To make sure pull requests weren't breaking our functionality     |

-------------------------  
<br><br><br>
### Our Process

- We focused on a feature lead design with a strict focus on TDD using Pytest. We made sure that we built each module so it was easily abstractable, and could be replaced easily (e.g. Rulesets, pieces etc.)
- We worked in 2 day sprints, and paired on the more technically difficult parts of the script. Working on modular design with clear separate responsibilities for each team member meant that there were barely any merge conflicts throughout  

- By the end of the second day we had arrived at our MVP:  

*Command-line version using unicode chars*
<br>
<img src="https://github.com/dangyi23/makers-final-project/blob/master/docs/MVP.gif" width=40%>
<br>

*First Slack Version*
<br>
<img src="https://github.com/dangyi23/makers-final-project/blob/master/docs/Chessy_with_AI.gif" width=40%>
<br>


- Once we had a working MVP, we moved on to creating a module for each piece type, and making sure they each inherited from a master `Piece` class   

- This is where the headaches started. Programming Check/Checkmate/Stalemate conditions proved tricky. We prevailed!  

- We extracted rules to a `StandardRules` class, from which weird and wonderful new game variants could inherit

- Next, we moved on to implementing in Slack. We set up the slack UI to accept commands and print the state of the board in a slack channel

- Finally, we wanted to compete against an AI, and see how complex we could build a chess AI using a minimax algorithm. This required a few different versions and lots of reading/understanding Python iterative methods  

- We finally arrived, by the end of the second week, with a product that:
  - Has a Python backend that can run a command line UI but also interact with the Slack API to run in slack channels
  - Adheres to all of the rules of chess (legal/illegal moves, check/checkmate/stalemate etc.)
  - Multiple games can be played in parallel by any users that invite the Chessy Bot.
  - Has many different rulesets that can be injected into the game at various points (Bishops excommunicating, Rooks being sold off etc.)
  - Has an AI option, so that you can play vs DominationBot3000
  - This AI option can be modified to increase/decrease the depth (though increasing the depth has an exponential performance trade-off)
  - Renders a PNG image of the board after each legal turn is made, so that each player can see the state of the board before they make their turn.
  - Is great fun!
<br><br><br>
## Minimax Algorithm Iterations

**Kamikaze bot**

![](https://github.com/DanGyi23/makers-final-project/blob/master/docs/kamikaze_AI.gif)



**Bot only wants to move its Knights**

![](https://github.com/DanGyi23/makers-final-project/blob/master/docs/Knight_AI.gif)



**Bot works!**

![](https://github.com/DanGyi23/makers-final-project/blob/master/docs/Working_AI.gif)
